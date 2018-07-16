from os import path

from fake_useragent import UserAgent
import requests
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

here = path.abspath(path.dirname(__file__))
loc = path.join(here, 'golf.db')

engine = create_engine(f'sqlite:///{loc}', echo=False)

Session = sessionmaker(bind=engine, autoflush=False)

Base = declarative_base()


UA = UserAgent()

headers = {'Host': 'site.api.espn.com', 'Connection': 'keep-alive',
           'Accept': '*/*', 'Origin': 'http://www.espn.com',
           'User-Agent': UA.chrome,
           'Referer': 'http://www.espn.com/golf/leaderboard/_/tour/eur',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'en-US,en;q=0.9'}

rsess = requests.Session()
rsess.headers.update(headers)

from .tourschedule import *
from .coursedata import *
from .players import *
from .player_hole_scores import *

#Base.metadata.create_all(bind=engine)