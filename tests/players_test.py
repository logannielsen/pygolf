# -*- coding: utf-8 -*-
from datetime import datetime
import json
from os import path

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats)

from helpers import create_db_and_session
from player_resources import player_dict
import pytest

here = path.abspath(path.dirname(__file__))
data = dict(**player_dict)

@pytest.fixture
def player():
    return Player.new_from_leaderboard(data)

@pytest.fixture
def playerevent():
    return PlayerEvent.leaderboard_player(data)

@pytest.fixture
def playerstatlist():
    return PlayerEventStats.leaderboard_player_stats(data)


def test_players_instantiation(player):
    assert isinstance(player, Player)
    assert player.player_id == data['id']
    assert player.displayName == data['displayName']
    assert data == player_dict

def test_players_stats_instantiation(playerevent):
    assert isinstance(playerevent, PlayerEvent)
    assert playerevent.player_id == data['id']
    assert playerevent.rank == data['rank']

def test_player_event_stats_instantiaton(playerstatlist):
    names = ['regScore', 'scoreToPar', 'driveDistAvg', 'driveAccuracyPct']
    displaynames = ['Total', 'Score To Par', 'Driving Distance', 'Driving Accuracy']
    abbreviations = ['TOT', 'TO PAR', 'YDS/DRV', 'DRV ACC']
    values = [270.0, -18.0, 316.70001220703125, 64.29000091552734]
    displayvalues = ['270', '-18', '316.7', '64.3']
    for i, playerstat in enumerate(playerstatlist):
        if i <= 3:
            assert isinstance(playerstat, PlayerEventStats)
            assert playerstat.name == names[i]
            assert playerstat.displayName == displaynames[i] 
            assert playerstat.value == values[i] 
            assert playerstat.abbreviation == abbreviations[i]
            assert playerstat.displayValue == displayvalues[i]

# pytest players_test.py
