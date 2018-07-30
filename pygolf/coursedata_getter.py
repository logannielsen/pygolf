import json
import logging

from sqlalchemy.exc import IntegrityError

from pygolf import Event, rsess, Season, Session, Tour, Course, HoleData
from .helpers import getter

TOURS = ['pga', 'lpga', 'eur', 'ntw']

def course_data_getter(event, session): 
    logging.debug(f'processing: {event.label}')
    url = (f'http://site.api.espn.com/apis/site/v2/sports/golf/{event.tour.slug}/leaderboard/course?event={event.id}&lang=en&region=us')
    json_data = json.loads(getter(url))
    course_info = json_data.get('courses', [])
    for course_dict in course_info:
        hole_data_dict = course_dict.pop('holes', [])
        course_obj = session.query(Course).\
            filter_by(courseId=course_dict['courseId']).one_or_none()
        if course_obj is None:
            course_obj = Course(**course_dict)
        event.courses.append(course_obj)
        if not event.hole_data:
            for hole_dict in hole_data_dict:
                del hole_dict['holeStatistics']
                hole_obj = HoleData(**hole_dict)
                event.hole_data.append(hole_obj)
                course_obj.hole_data.append(hole_obj)
    session.flush()
    
          
def main():
    logging.info('Starting')
    idset = set()
    session = Session()
    try:
        all_events = session.query(Event).all()
        for i, event in enumerate(all_events):
            course_data_getter(event, session)
    except Exception as e:
        logging.exception(str(e))
        session.rollback()
        raise
    else:
        logging.info('All good!')
        session.commit()
    finally:
        session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
