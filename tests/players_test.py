# -*- coding: utf-8 -*-
from datetime import datetime
import json
from os import path

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats)

from helpers import create_db_and_session
from player_resources import player_dict

here = path.abspath(path.dirname(__file__))

def test_players_instantiation():
    data = dict(**player_dict)
    p = Player.new_from_leaderboard(data)
    assert isinstance(p, Player)
    assert p.player_id == data['id']
    assert p.displayName == data['displayName']
    assert data == player_dict

def test_players_stats_instantiation():
    data = dict(**player_dict)
    p = PlayerEvent.leaderboard_player(data)
    assert isinstance(p, PlayerEvent)
    assert p.player_id == data['id']
    assert p.rank == data['rank']
