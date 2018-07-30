from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum, ForeignKey,
                        Integer, String, UniqueConstraint, ForeignKeyConstraint)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"


class Player(Base):
    """ This class represents an individual golfer.
    
    This is a long docstring over multiple lines.
    
    """
    
    __tablename__ = 'tbl_player'
    
    player_id = Column(Integer, primary_key=True)
    fullName = Column(String)
    displayName = Column(String)
    dateOfBirth = Column(String)
    hand = Column(String)
    link = Column(String)
    birthPlace = Column(String)
    player_tournaments = relationship("PlayerEvent",
                                      back_populates="player")
    events = relationship("PlayerEvent", back_populates="player")
    
    def __repr__(self):
        return f"<Player(player_id={self.player_id}, fullname={self.fullName}"\
               f", displayName={self.displayName}, "\
               f"dateOfBirth={self.dateOfBirth}, hand={self.hand}, "\
               f"link={self.link}, birthPlace={self.birthPlace})>"

    @classmethod
    def new_from_leaderboard(cls, data):
        skipkeys = {'countryFlag', 'rank', 'stats', 'id'}
        return cls(player_id=data['id'],
                   **{k: v for k, v in data.items() if k not in skipkeys})

    @classmethod
    def profile_information(cls, course_data):
        profile = course_data['profile']
        skipkeys = {'age', 'headshot', 'rank', 'earnings', 'displayName'}
        return cls(**{k: v for k, v in profile.items() if k not in skipkeys})

class PlayerEvent(Base):

    __tablename__ = 'tbl_tournament_players'

    player_id = Column(Integer, ForeignKey('tbl_player.player_id'),
                       primary_key=True,)
    event_id = Column(Integer, ForeignKey('tbl_event.id'),
                           primary_key=True)
    rank = Column(String)
    earnings = Column(String)
    
    event_stats = relationship('PlayerEventStats',
                               back_populates="player_event")
    event = relationship('Event', back_populates='players', uselist=False)
    player = relationship('Player', back_populates='events', uselist=False)
    rounds = relationship('Round', back_populates='player_event')

    @classmethod
    def leaderboard_player(cls, data):
        skipkeys = {'countryFlag', 'stats', 'id', 'displayName', 'fullName'}
        return cls(player_id=data['id'],
                   **{k: v for k, v in data.items() if k not in skipkeys})


    

class PlayerEventStats(Base):

    __tablename__ = 'tbl_player_tournament_stats'

    name = Column(String, primary_key=True)
    player_id = Column(Integer, ForeignKey('tbl_player.player_id'), 
                       primary_key=True)
    event_id = Column(Integer, ForeignKey('tbl_event.id'),
                           primary_key=True)                      
    displayName = Column(String)
    abbreviation = Column(String)
    value = Column(Integer)
    displayValue = Column(Integer)
    player_event = relationship("PlayerEvent", uselist=False, 
                               back_populates="event_stats")

    __table_args__ = (
        ForeignKeyConstraint(
            ["player_id", "event_id"],
            ["tbl_tournament_players.player_id",
             "tbl_tournament_players.event_id"],
            name="fk player_tournament"
        ),)  

    @classmethod
    def leaderboard_player_stats(cls, data):
        stat = data['stats']
        return [cls(**s) for s in stat]

                   
    