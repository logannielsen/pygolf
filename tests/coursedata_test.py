# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 21:53:03 2018

@author: Logan Programming
"""
from datetime import datetime
import json
from os import path

from pygolf import coursedata, Event

from helpers import create_db_and_session

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'coursedata.txt'), 'r') as f:
    course_data = json.load(f)
    
course = course_data.get('courses')[0]
hole_data = course.pop('holes')


def test_course_instantiation():
    c = coursedata.Course(**course)
    assert isinstance(c, coursedata.Course)
    assert c.courseId == '18'
    assert c.name == "Bay Hill Club & Lodge"

def test_instantiate_hole_data():
    e = Event(startDate="2002-08-18T07:00Z", endDate="2002-08-18T07:00Z",
              label='an event')
    c = coursedata.Course(**course)
    e.courses.append(c)
    for hole in hole_data:
        del hole['holeStatistics']
        h = coursedata.HoleData(**hole)
        h.event = e
        assert isinstance(h, coursedata.HoleData)
        c.hole_data.append(h)
    assert len(c.hole_data) == 18
    assert h.course is c
    assert c in e.courses
    assert e in c.events
    assert h.event is e
