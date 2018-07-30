import logging

from pygolf import rsess

from pygolf import (Event, rsess, Season, Session, Tour, Course, HoleData,
                    Player, PlayerEvent, PlayerEventStats)

def getter(url):
    logging.info(f'Getting: {url}')
    retries = 3
    for i in range(retries):
        try:
            r = rsess.get(url)
        except Exception as e:
            logging.exception(f'Failed getting: {url} (attempt: {i})')
            if i == retries - 1:
                raise
        else:
            return r.text