"""course information tables - includes hole distance, hole number, hole yards
 and hole statistics (score to par, average score, eagles, birdies, bogeys, 
 double bogeys, double bogey +, difficulty ranking)  """

from datetime import datetime

from sqlalchemy import (Column, DateTime, Enum, ForeignKey,
                        Integer, String, UniqueConstraint)
from sqlalchemy.orm import relationship
from pygolf import Base

DT_FMT = "%Y-%m-%dT%H:%MZ"

class HoleDescription(Base):
    
    __tablename__ = 'tbl_course'

    courseId = Column(Integer, primary_key=True) 
    event_id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True) 
    holeNumber = Column(Integer)
    holeYards = Column(Integer)
    HolePar = Column(Integer)
    holestats = relationship('HoleStatistics', back_populates="holedescription")
    
    
class HoleStatistics(Base):
    
    event_id = Column(Integer, ForeignKey('tbl_event.id'), primary_key=True)
    holeNumber = Column(Integer, ForeignKey('tbl_hole_meta_data.holeNumber'), primary_key=True)
    name = Column(String)
    displayName = Column(String)
    description = Column(String)
    value = Column(Integer)
    displayValue = Column(Integer)
    holedescription = relationship('HoleDescription', back_populates="holestats")
    