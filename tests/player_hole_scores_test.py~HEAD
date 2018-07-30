# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:07:50 2018

@author: Logan Programming
"""

from datetime import datetime
import json
from os import path
import pytest

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats, Round)

from helpers import create_db_and_session

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'rmac.txt'), 'r') as f:
    course_data = json.load(f)


@pytest.fixture
def playerprofile():
    return Player.profile_information(course_data)

@pytest.fixture
def playerround():
    return Round.round_instantiation(course_data)

@pytest.fixture
def test_holescores_instantiation():
    return HoleScore.hole_score_instantiation(course_data)


def test_player_profile_instantiation(playerprofile):
    assert isinstance(playerprofile, Player)
    assert playerprofile.dateOfBirth == '1989-05-04T07:00Z'
    assert playerprofile.hand == 'R'
    assert playerprofile.link == 'http://www.espn.com/golf/player/_/id/3470/rory-mcilroy'
    assert playerprofile.birthPlace == 'Holywood, Northern Ireland'

def test_round_instantiation(playerround):
    # round_1 = {"value":69.0,"displayValue":"-3","period":1,"inScore":37,"outScore":32,"courseId":18,"hasStream":false,"startPosition":13,"currentPosition":13,"movement":0,"teeTime":"2018-03-15T20:08Z"},
    # round_2 = {"value":70.0,"displayValue":"-2","period":2, "inScore":34,"outScore":36,"courseId":18,"hasStream":false,"startPosition":13,"currentPosition":11,"movement":-2,"teeTime":"2018-03-16T15:23Z"},
    # round_3 = {"value":67.0,"displayValue":"-5","period":3, "inScore":33,"outScore":34,"courseId":18,"hasStream":false,"startPosition":11,"currentPosition":3,"movement":-8,"teeTime":"2018-03-17T20:05Z"}
    # round_4 = {"value":64.0,"displayValue":"-8","period":4, "inScore":31,"outScore":33,"courseId":18,"hasStream":false,"startPosition":3,"currentPosition":1,"movement":-2,"teeTime":"2018-03-18T21:10Z"}]
    
    for i, p in enumerate(playerround):
        if i <= 0:
            assert isinstance(p, Round)
            assert p.value == 69.0
            assert p.displayValue == '-3'
            assert p.period == 1
            assert p.inScore == 37
            assert p.outScore == 32
            assert p.startPosition == 13
            assert p.currentPosition == 13
            assert p.movement == 0
            assert p.teeTime == '2018-03-15T20:08Z'

def test_holescores_instantiation():
    