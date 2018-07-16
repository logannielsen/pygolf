from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum, ForeignKey,
                        Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"

class Tour(Base):

    __tablename__ = 'tbl_tour'

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    shortName = Column(String)
    slug = Column(String)
    seasons = relationship('Season', back_populates="tours",
                           secondary='tbl_season_tour')
    events = relationship('Event', back_populates='tour')


class SeasonTour(Base):

    __tablename__ = 'tbl_season_tour'

    season_id = Column(Integer, ForeignKey('tbl_season.year'),
                       primary_key=True)
    tour_id = Column(Integer, ForeignKey('tbl_tour.id'), primary_key=True)


class Season(Base):

    __tablename__ = 'tbl_season'

    year = Column(Integer, primary_key=True, autoincrement=False)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    displayName = Column(String)
    tours = relationship('Tour', secondary='tbl_season_tour',
                        back_populates='seasons')
    events = relationship('Event', back_populates='season')
    UniqueConstraint('tour_id', 'year', name='ux_tbl_season_tour_id_year')

    def __init__(self, startDate, endDate, **kwargs):
        startDate = datetime.strptime(startDate, DT_FMT)
        endDate = datetime.strptime(endDate, DT_FMT)
        super().__init__(startDate=startDate, endDate=endDate, **kwargs)
        
        
class EventCourse(Base):
    
    __tablename__ = 'tbl_eventcourse'
    
    event_id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True)
    course_id = Column(Integer, ForeignKey('tbl_course.courseId'), primary_key=True )

class Event(Base):

    __tablename__ = 'tbl_event'

    id = Column(Integer, primary_key=True)
    tour_id = Column(Integer, ForeignKey('tbl_tour.id'))
    season_id = Column(Integer, ForeignKey('tbl_season.year'))
    label = Column(String)
    detail = Column(String)
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    status = Column(Enum("post", "pre"))
    link = Column(String)
    season = relationship('Season', uselist=False, back_populates='events')
    hole_data = relationship('HoleData', back_populates='event')
    tour = relationship('Tour', back_populates='events', uselist=False)
    courses = relationship('Course', secondary='tbl_eventcourse',
                           back_populates='events')
    players = relationship('PlayerEvent', back_populates='event')
    
    def __init__(self, startDate, endDate, **kwargs):
        startDate = datetime.strptime(startDate, DT_FMT)
        endDate = datetime.strptime(endDate, DT_FMT)
        super().__init__(startDate=startDate, endDate=endDate, **kwargs)
