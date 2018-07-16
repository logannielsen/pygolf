""" Grab info from http://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard/3750/playersummary?player=3470&season=2018&lang=en&region=us getting the score per hole per player for a specified event as well as the overall event statistics """ 


import json
import logging

from sqlalchemy.exc import IntegrityError

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats)

def getter(url):
    logging.info(f'Getting: {url}')
    r = rsess.get(url)
    return r.text

def player_data_getter(event_id, player_id, session): 
    url = (f'http://site.api.espn.com/apis/site/v2/sports/golf/pga/leaderboard/{event_id}/playersummary?player={player_id}&season=2018&lang=en&region=us')
    json_data = json.loads(getter(url))
    print(json_data)


def main():
    logging.info('Starting')
    session = Session()
    logging.debug(f'Session established {session}')
    try:
        for event in session.query(Event).all():
            logging.debug(f'{event}')
            if event.players:
                for player in event.players:
                    logging.debug(f'player: {player.player}')
                    try:
                        player_data_getter(event.id, player.player_id, session)
                    except Exception as e:
                        logging.exception(f'{event.id}: {player.fullname}. {e}')
                    break
                break
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
    logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    logging.basicConfig(format='%(levelname)s:%(message)s\n\n\n\n', level=logging.DEBUG)
    main()
    
    # python main4.py