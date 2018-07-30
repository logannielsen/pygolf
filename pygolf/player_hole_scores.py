from datetime import datetime

from sqlalchemy import (Column, DateTime, ForeignKey,
                        ForeignKeyConstraint, Integer, String)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"


class Round(Base):

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
    teeTime = Column(DateTime)
    course = relationship('Course', uselist=False)
    player_event = relationship('PlayerEvent', uselist=False)
    holes = relationship('HoleScore', back_populates='round')
    ForeignKeyConstraint(
        [player_id, event_id],
        ['tbl_tournament_players.player_id',
         'tbl_tournament_players.event_id']
    )
    
    @classmethod
    def round_instantiation(cls, course_data):
        rounds = course_data['rounds']
        l = []
        skipkeys = {'linescores', 'hasStream'}
        for r in rounds:
            instin = cls(
                **{k:v for k, v in r.items() if k not in skipkeys}
            )
            l.append(instin)
        return l 
            
        

class HoleScore(Base):

    __tablename__ = 'tbl_player_hole_data'

    player_id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey('tbl_event.id'),
                           primary_key=True)
    round_number = Column(Integer, primary_key=True)
    period = Column(Integer, primary_key=True)
    courseId = Column(Integer)
    value = Column(Integer)
    displayValue = Column(Integer)
    par = Column(String)
    hole_data_id = Column(Integer,
                          ForeignKey('tbl_hole_data.hole_data_id'))
    hole_data = relationship('HoleData', back_populates='hole_scores')
    round = relationship('Round', back_populates='holes')

    ForeignKeyConstraint([player_id, event_id, period],
                         ['tbl_player_round_data.player_id',
                          'tbl_player_round_data.event_id',
                          'tbl_player_round_data.period'])                     

    
    @classmethod
    def hole_score_instantiation(cls, course_data):
        rounds = course_data['rounds']
        l = []
        skipkeys = {'value', 'displayValue', 'hasStream', 'period', 'outScore', 'inScore', 'startPosition', 'currentPosition', 'movement', 'teeTime'}
        for r in rounds:
            instin = cls(
                **{k:v for k, v in r.items() if k not in skipkeys}
            )
            l.append(instin)
        return l 