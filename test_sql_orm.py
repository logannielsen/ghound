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
    dogs = sess.query(GreyhoundTable).join(RaceStatsTable, GreyhoundTable.id==RaceStatsTable.greyhound_id).join(RaceTable, RaceTable.id==RaceStatsTable.race).\
                join(TrackTable, RaceTable.id==TrackTable.id).\
                filter(RaceTable.date==datetime.strptime("15/12/2019", '%d/%m/%Y')).\
                filter(TrackTable.track_name=='SAP').\
                filter(RaceTable.race_number==1)
    print(dogs.all())
    print('done')

def test_b():
    for race in sess.query(RaceStatsTable).join(GreyhoundTable).join(RaceTable).join(TrackTable).filter(GreyhoundTable.name=="ASTON SPINEL").all():
        print(race.id, race.distance)
        print('done')

test_a()
datetime.strptime("15/12/2019", '%d/%m/%Y')