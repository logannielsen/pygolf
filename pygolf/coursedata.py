from sqlalchemy import (Column, ForeignKey, ForeignKeyConstraint, Integer,
                        String)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"


class Course(Base):
    
    __tablename__ = 'tbl_course'
    
    courseId = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String)
    events = relationship('Event', back_populates='courses',
                          secondary='tbl_eventcourse')
    hole_data = relationship('HoleData', back_populates='course')
   
class HoleData(Base):
    
    __tablename__ = 'tbl_hole_data'
    
    course_id = Column(Integer, ForeignKey('tbl_course.courseId'), primary_key=True)
    event_id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True)
    holeNumber = Column(Integer, primary_key=True)
    holePar = Column(Integer)
    holeYards = Column(Integer)
    course = relationship('Course', back_populates='hole_data', uselist=False)
    event = relationship('Event', back_populates='hole_data', uselist=False)
    hole_scores = relationship('HoleScore', back_populates='hole_data')
    
    
# python coursedata.py
#class HoleStats(Base):
#    
#    __tablename__ = 'tbl_hole_stats'
#    
#    holeNumber = Column(Integer, ForeignKey('tbl_hole_data.holeNumber'))
#    course_id = Column(Integer, ForeignKey('tbl_event_course_data.course_id'), primary_key=True)
#    tournament_id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True)                         
#    name = Column(String)
#    displayName = Column(String)
#    description = Column(String)
#    abbreviation = Column(String)
#    value = Column(Integer)
#    displayValue = Column(Integer)
#    
#    hole = relationship('HoleData', back_populates='holestats') 
#    course = relationship('EventCourse', back_populates='event')
#    event = relationship('Event', back_populates=('event_course'))
#    
#    __table_args__ = (ForeignKeyConstraint(['course_id', 'tournament_id'],
#                                           ['tbl_hole_data.course_id',
#                                            'tbl_hole_data.tournament_id']), )

# http://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard/players?event=3750&lang=en&region=us

#class Tournament(Base):
#
#    __tablename__ = 'tbl_tournament'
#
#    id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True)
#    name = Column(String)
#    year = Column(Integer)
#    leaderboard = relationship('Leaderboard', back_populates="players")
#
#class Leaderboard(Base):
#
#    __tablename__ = 'tbl_tournament_players'
#
#    player_id = Column(Integer, primary_key=True)
#    tournament_id = Column(Integer, ForeignKey('tbl_tournament.id'),
#                           primary_key=True)
#    displayName = Column(String)
#    fullName = Column(String)
#    stats = relationship('RoundStats', back_populates="player_stat")
#    players = relationship("Tournament", uselist=False, 
#                           back_populates="leaderboard")
#
#class RoundStats(Base):
#
#    __tablename__ = 'tbl_player_round_stats'
#
#    name = Column(String)
#    player_id = Column(Integer, ForeignKey('tbl_tournament_players.player_id'), 
#                       primary_key=True)
#    tournament_id = Column(Integer, ForeignKey('tbl_tournament.id'),
#                           primary_key=True)                      
#    displayName = Column(String)
#    abbreviation = Column(String)
#    value = Column(Integer)
#    displayValue = Column(Integer)
#    player_stat = relationship("Leaderboard", uselist=False, 
#                               back_populates="stats")
#
##http://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard/3750/playersummary?player=3470&season=2018&lang=en&region=us
#
#class Profile(Base):
#
#    __tablename__ = 'tbl_player_profile'
#    
#    event_id = Column(Integer, primary_key=True)
#    player_id = Column(Integer, ForeignKey('tbl_tournament_players.player_id'), primary_key=True)
#    displayName = Column(String)
#    age = Column(Integer)
#    dateOfBirth = Column(DateTime)
#    hand = Column(String)
#    link = Column(String)
#    birthPlace = Column(String)
#    rank = Column(String)
#    earning = Column(Integer)
#    rounds = relationship('Rounds')
#    tournament_stats = relationship('TournamentStats')
#    player = relationship('Leaderboard')
#    event = relationship('Event')

#class Rounds(Base):
#
#    __tablename__ = 'tbl_player_round_data'
#
#    displayValue = Column(Integer)
#    value = Column(Integer)
#    period = Column(Integer)
#    inScore = Column(Integer)
#    outScore = Column(Integer)
#    courseId = Column(Integer)
#    startPosition = Column(Integer)
#    currentPosition = Column(Integer)
#    movement = Column(Integer)
#    teetime = Column(DateTime)
#    linescores = relationship("Hole_by_Hole_Data")
#
#class HoleByHoleData(Base):
#
#    __tablename__ = 'tbl_player_hole_data'
#
#    value = Column(Integer)
#    displayValue = Column(Integer)
#    period = Column(Integer)          ##hole number##
#    scoreType = relationship
#    par = Column(String)
#
#
#class Scoring(Base):
#
#    __tablename__ = 'tbl_score_types'
#
#    name = Column(String)
#    displayName = Column(String)
#    displayValue = Column(Integer)
#
#class TournamentStats(Base):
#
#    __tablename__ = 'tbl_player_tournament_stats'
#
#    player_id = Column(Integer, ForeignKey('tbl_player_profile.player_id'))
#    name = Column(String)
#    displayName = Column(String)
#    displayValue = Column(Integer)
#    player_info('Profile', back_populates='tbl_player_profile')