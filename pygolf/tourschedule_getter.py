import json
import logging

from sqlalchemy.exc import IntegrityError

from pygolf import Event, rsess, Season, Session, Tour
from .helpers import getter


TOURS = ['pga', 'lpga', 'eur', 'ntw']


def season_getter(year, session, idset):
    """ Accesses the tour schedule for supplied year and makes a record
    of each event in that season.

    Params:
        year: Integer
        session: SQLAlchemy session instance
    """
    logging.info(f'season_getter({year}, {session}, {idset})')
    season = session.query(Season).filter_by(year=year).one_or_none()
    for tour_abbr in TOURS:
        logging.debug(f'processing tour: {tour_abbr}')
        tour = session.query(Tour).filter_by(slug=tour_abbr).one_or_none()
        url = (f'http://site.api.espn.com/apis/site/v2/sports/golf/{tour_abbr}/'
               f'tourschedule?season={year}&lang=en&region=us')
        json_data = json.loads(getter(url))
        try:
            all_season_data = json_data.pop('seasons')
        except KeyError:
            logging.error(f'No season data available for {tour_abbr} {year}')
            return
        if tour is None:
            logging.debug(f'no {tour_abbr} tour.. creating..')
            del json_data['defaultSeason']
            tour = Tour(**json_data)
            session.add(tour)
        for season_data in all_season_data:
            if season_data['year'] == year:
                events = season_data.pop('events')
                if season is None:
                    logging.debug(f'no season {year}.. creating..')
                    season = Season(**season_data)
                    tour.seasons.append(season)
                for event_data in events:
                    if (event_data["id"] not in idset and
                        event_data['status'] != 'in'):
                            logging.debug('creating event: {event_data}')
                            idset.add(event_data["id"])
                            tour.events.append(
                                Event(**event_data, season=season)
                            )
    session.flush()

def main():
    logging.info('Starting')
    idset = set()
    session = Session()
    try:
        for year in range(2001, 2019):
            season_getter(year, session, idset)
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
    