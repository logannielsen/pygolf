# -*- coding: utf-8 -*- py.test schedule_test.py
"""
Created on Mon Apr 23 18:45:28 2018

@author: Logan Programming
"""
from datetime import datetime
import json
from os import path

from pygolf import tourschedule

from helpers import create_db_and_session

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'tour_data.txt'), 'r') as f:
    tour_data = json.load(f)

seasons = tour_data.pop('seasons')
del tour_data['defaultSeason']

for season in seasons:
    if 'events' in season:
        our_season = season
        year = season['year']
        events = our_season.pop('events')

def test_season():
    s = tourschedule.Season(**our_season)
    assert s.year == 2002
    assert isinstance(s.startDate, datetime)
    assert s.startDate.year == 2002
    assert s.endDate.month == 11
    assert s.displayName == 'PGA Tour 2002'
    assert s.events == s.tours == []


def test_instantiate_tour():
    tour = tourschedule.Tour(**tour_data)
    assert isinstance(tour, tourschedule.Tour)
    assert tour.id == '1106'
    assert tour.name == "Pro Golfer's Association"
    assert tour.shortName  == 'PGA Tour'


def test_instantiate_events():
    for event in events:
        e = tourschedule.Event(**event)
        assert isinstance(e.label, str)
        assert isinstance(e.detail, str)
        assert isinstance(e.startDate, datetime)
        assert isinstance(e.endDate, datetime)
        assert isinstance(e.status, str)
        assert isinstance(e.link, str)
        assert e.season is None


def test_tour_seasons_relationship():
    tour = tourschedule.Tour(**tour_data)
    tour.seasons = [tourschedule.Season(**s) for s in seasons]
    assert issubclass(type(tour.seasons), list)
    assert all([isinstance(s, tourschedule.Season) for s in tour.seasons])
    assert len(tour.seasons) == len(seasons)


def test_season_events_relationship():
    tour = tourschedule.Tour(**tour_data)
    tour.seasons = [tourschedule.Season(**s) for s in seasons]
    season = [s for s in tour.seasons if s.year == 2002][0]
    season.events = [tourschedule.Event(**e) for e in events]
    assert issubclass(type(season.events), list)
    assert all([isinstance(e, tourschedule.Event) for e in season.events])
    assert len(season.events) == len(events)


def test_year_tour_id_added_to_events():
    tour = tourschedule.Tour(**tour_data)
    tour.seasons = [tourschedule.Season(**s) for s in seasons]
    for season in tour.seasons:
        if season.year == 2002:
            season.events = [tourschedule.Event(**e) for e in events]
    Session = create_db_and_session()
    sess = Session()
    sess.add(tour)
    sess.commit()
    sess.expire_all()
    try:
        test_tour = sess.query(tourschedule.Tour).filter_by(id=tour.id).one()
        for s in test_tour.seasons:
            if s.year == 2002:
                for e in season.events:
                    assert e.tour_id == tour.id
                    assert e.season_id == s.year
    finally:
        sess.close()
