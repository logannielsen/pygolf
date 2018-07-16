# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 21:54:04 2018

@author: Logan Programming
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pygolf import Base

def create_db_and_session():
    engine = create_engine('sqlite:///:memory:')

    Base.metadata.create_all(bind=engine)

    return sessionmaker(bind=engine)
