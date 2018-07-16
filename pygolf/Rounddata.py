from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey, ForeignKeyConstraint,
                        Integer, String)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"


class Rounds(Base):

    __tablename__ = 'tbl_player_round_data'

    player_id = Column(Integer, ForeignKey('tbl_player.player_id'), 
                       primary_key=True)
    event_id = Column(Integer, ForeignKey('tbl_event.id'),
                           primary_key=True)
    period = Column(Integer, primary_key=True)
    displayValue = Column(Integer)
    value = Column(Integer)
    inScore = Column(Integer)
    outScore = Column(Integer)
    courseId = Column(Integer, ForeignKey('tbl_course.courseId'))
    startPosition = Column(Integer)
    currentPosition = Column(Integer)
    movement = Column(Integer)
    teetime = Column(DateTime)
    course = relationship('Course', uselist=False)
    

class HoleScore(Base):

    __tablename__ = 'tbl_player_hole_data'

    player_id = Column(Integer, ForeignKey('tbl_player.player_id'), 
                       primary_key=True)
    event_id = Column(Integer, ForeignKey('tbl_event.id'),
                           primary_key=True)
    round_number = Column(Integer, ForeignKey('tbl_player_round_data.period'),
                          primary_key=True)
    period = Column(Integer, primary_key=True)
    courseId = Column(Integer, ForeignKey('tbl_course.courseId'))
    value = Column(Integer)
    displayValue = Column(Integer)
    par = Column(String)
    player = relationship('Player', back_populates='hole_scores')
    hole_data = relationship('HoleData', back_populates='hole_scores')
    course = relationship('Course', uselist=False)
    
    ForeignKeyConstraint([courseId, event_id, period],
                         ['tbl_hole_data.course_id', 'tbl_hole_data.event_id',
                          'tbl_hole_data.holeNumber'])

    
