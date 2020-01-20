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
    for a in sess.query(GreyhoundTable).filter(TrackTable.id==6).all():
        print(a.id, a.name)
        print('done')
    
def test_a():
    for dog, track in sess.query(GreyhoundTable, TrackTable).join(RaceStatsTable).join(RaceTable).join(TrackTable).filter(TrackTable.id=='9').all():
        print(dog.id, dog.name, track.track_name)
        print('done')

test_a()
