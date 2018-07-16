from sqlalchemy import (Column, ForeignKey, ForeignKeyConstraint, Integer,
                        String, UniqueConstraint)
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
    hole_data_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey('tbl_course.courseId'))
    event_id = Column(Integer, ForeignKey('tbl_event.id'))
    holeNumber = Column(Integer)
    holePar = Column(Integer)
    holeYards = Column(Integer)
    course = relationship('Course', back_populates='hole_data', uselist=False)
    event = relationship('Event', back_populates='hole_data', uselist=False)
    hole_scores = relationship('HoleScore', back_populates='hole_data')

    __table_args__ = (
        UniqueConstraint('course_id', 'event_id', 'holeNumber'), 
    )