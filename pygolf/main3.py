import json
import logging

from sqlalchemy.exc import IntegrityError

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats)

def getter(url):
    logging.info(f'Getting: {url}')
    r = rsess.get(url)
    return r.text

def player_data_getter(event, session): 
    logging.debug(f'processing: {event.label}')
    url = (f'http://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard/players?event={event.id}&lang=en&region=us')
    json_data = json.loads(getter(url))
    leaderboard = json_data.get('leaderboard', [])
    for player_dict in leaderboard:
        player_obj = session.query(Player).filter_by(player_id=player_dict['id']).one_or_none()
        if player_obj is None:
            player_obj = Player(player_id=player_dict['id'], fullName=player_dict['fullName'])
        player_event_obj = session.query(PlayerEvent).filter_by(player_id=player_obj.player_id, event_id=event.id).one_or_none()  
        if player_event_obj is None:
            player_event_obj = PlayerEvent(player=player_obj, event=event)
        if not player_event_obj.event_stats:
            for stat_dict in player_dict.get('stats', []):
                player_event_obj.event_stats.append(PlayerEventStats(**stat_dict))
    session.flush()

#        player_info = player_dict.update(player_id = player['id'], fullName = player['fullName'])
#        print(player_info)
#        player_obj = Player(**player_info)
#        session.add(player_obj)

def main():
    logging.info('Starting')
    idset = set()
    session = Session()
    try:
        all_events = session.query(Event).all()
        for i, event in enumerate(all_events):
            try:
                player_data_getter(event, session)
            except Exception as e:
                logging.exception(f'{event.id}: {event.label}. {e}')
    except Exception as e:
        logging.exception(str(e))
        session.rollback()
        raise
    else:
        logging.info('All good!')
        session.commit()
    finally:
        session.close()


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s\n\n\n\n', filename='error.log', level=logging.ERROR)
    main()
    

# python main3.py