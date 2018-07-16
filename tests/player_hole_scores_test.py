# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 18:07:50 2018

@author: Logan Programming
"""

from datetime import datetime
import json
from os import path

from pygolf import coursedata, Event

from helpers import create_db_and_session

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'rmac.txt'), 'r') as f:
    course_data = json.load(f)
    
