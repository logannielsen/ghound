import requests
import os
import csv
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from re import sub, search
from decimal import Decimal
from helpers import *
from greyhound import *
from greyhound_object_model import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, joinedload


def test():
    for a in sess.query(TrackTable).all():
        print(a.track_name, a.id)
        print('done')
    
def test_a():
    for race in sess.query(TrackTable).filter(TrackTable.track_name=='SLE'):
        print(race.id, race.track_name)
        print('done')

test()