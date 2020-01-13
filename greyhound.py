import requests
import os
import csv
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from re import sub, search
from decimal import Decimal
from helpers import *

FIELD_NAMES = ['Pl',
            'Box',
            'Wght',
            'Dist',
            'Trk',
            'Race',
            'Date',
            'Time',
            'BON',
            'Mgin',
            '1st/2nd(Time)',
            'Split1',
            'PIR',
            'Comment',
            'S/P',
            'Grade',
            'Hcap']

class HTMLBase():

    def __init__(self, raw_html):
        self.soup = BeautifulSoup(raw_html, 'html.parser')
        
class Calendar(HTMLBase):
    
    def race_meets(self):
        """returns a list meeting objects
        each meeting has a meeting_id, track and is_finalised attribute"""
        return [Meet(meet) for meet in self.soup.find('tbody').find_all('tr')]
    
    def save_meets(self, session):
        for meetings in self.race_meets():
            # print(meetings.meeting_id,
            #         meetings.href, 
            #         meetings.is_meet_final, 
            #         meetings.track,
            #         meetings.file_path(),
            #         meetings.race_card_url
            #         )
            if meetings.is_meet_final: #change back once finished doing playing around
                request_and_write_if_non_existing_file(meetings.file_path(), meetings.race_card_url, session)
    

class Meet:

    def __init__(self, race_meets):
        self.race_meet = race_meets
        super().__init__()
    

    def file_path(self, root='sample_race_cards'):
        return build_and_check_path(
                                    self.meeting_id,
                                    self.track,
                                    root="sample_race_cards"
                                    )
    
    @property
    def race_card_url(self):
        return f"https://fasttrack.grv.org.au/RaceField/ViewRaces/{self.meeting_id}?raceId=0"

    @property
    def is_meet_final(self):
        return self.race_meet.find_all('td')[-2].get_text() == "Results Finalised"
    
    
    @property
    def meeting_id(self):
        return self.race_meet.find('a', href=True)['href'].rsplit("/", 1)[-1]

    @property
    def href(self):
        return self.race_meet.find('a', href=True)['href']

    @property
    def track(self):
        return self.race_meet.find('a', href=True).get_text()
     
    

class MeetRaces(HTMLBase):
    """returns an iterable of races"""

    @property
    def races_id_list(self):
        return [race['href'].rsplit('=', 1)[1]
        for race in self.soup.find(class_='side-tab-container').find_all('a')]

    


class Race(HTMLBase):

    @property
    def number(self):
        return self.soup.find(class_='race-number').get_text().strip()

    @property
    def time(self):
        return self.soup.find(class_='race-time').get_text().strip()
    
    @property
    def date(self):
        return datetime.strptime(self.soup.find(
            id='mainContentHeader').h1.get_text(
            ).rsplit(" ",1)[-1], '%d/%m/%Y').date()
    
    @property
    def first_prize(self):
        return Decimal(search(r'\d+', self.soup.find_all(
            class_='display-value-race-results'
            )[-1].get_text().split("-")[0]).group(0))


    @property
    def second_prize(self):
        return Decimal(search(r'\d+', self.soup.find_all(
            class_='display-value-race-results'
            )[-1].get_text().split("-")[1]).group(0))
    
    @property
    def third_prize(self):
        return Decimal(search(r'\d+', self.soup.find_all(
            class_='display-value-race-results'
            )[-1].get_text().split("-")[2]).group(0))


#     s = "tim email is tim@somehost.com"
# match = re.search('([\w.-]+)@([\w.-]+)', s)
# if match:
#     print(match.group()) ## tim@somehost.com (the whole match)
#     print(match.group(1)) ## tim (the username, group 1)
#     print(match.group(2)) ## somehost (the host, group 2)

    @property
    def distance(self):
        return Decimal(sub(r'[^\d.]', '', self.soup.find_all(
            class_='display-value-race-results'
            )[-2].get_text()))

    @property
    def race_type(self):
        return self.soup.find_all(
            class_='display-value-race-results'
            )[-3].get_text().strip()
    
    def get_greys(self):
        return [Greyhound(dog) for dog in self.soup.find(
            class_="raceResultsTable").tbody.find_all('tr')]

    @property
    def quinella_price(self):
        try:
            quinella = self.soup.find(id="raceExoticDividends"
            ).tbody.find_all('tr')[0]
            if quinella.find_all('td')[0].get_text().split()[0] == 'Quinella':
                return float(quinella.find_all('td')[-1].get_text())
        except IndexError:
            return None

    @property
    def exacta_price(self):
        try:
            exacta = self.soup.find(id="raceExoticDividends"
            ).tbody.find_all('tr')[1]
            if exacta.find_all('td')[0].get_text().split()[0] == 'Exacta':
                return float(exacta.find_all('td')[-1].get_text())
        except IndexError:
            return None

    @property
    def trifecta_price(self):
        try:
            trifecta = self.soup.find(id="raceExoticDividends"
            ).tbody.find_all('tr')[2]
            if trifecta.find_all('td')[0].get_text().split()[0] == 'Trifecta':
                return float(trifecta.find_all('td')[-1].get_text())
        except IndexError:
            return None

    @property
    def first4_price(self):
        try:
            first4 = self.soup.find(id="raceExoticDividends"
            ).tbody.find_all('tr')[3]
            if first4.find_all('td')[0].get_text().split()[0] == 'First':
                return float(first4.find_all('td')[-1].get_text())
        except IndexError:
            return None  
    

class Greyhound:

    def __init__(self, greyhound_data):
        self.greyhound = greyhound_data
        super().__init__()
    
    @property
    def name(self):
        name = self.greyhound.find_all(
            'td')[1].get_text().strip()
        split_name = name.split('(late')
        if len(split_name) > 1:
            name = split_name[-1].split(')')[0].strip()
        return name

    @property
    def id(self):
        return int(self.greyhound.find_all(
            'td')[1].a['href'].split('/')[-1])
    
    @property
    def trainer(self):
        return self.greyhound.find_all(
            'td')[2].get_text().strip()
    
    @property
    def place(self):
        return self.greyhound.find_all(
            'td')[0].get_text().strip()
    
    @property
    def rug(self):
        return self.greyhound.find_all(
            'td')[4].get_text().strip()

    def save_and_return_greyhound_form(self, session):
        download_url = f'https://fasttrack.grv.org.au/Dog/FormDownload/{self.id}'
        greyhound_path = build_and_check_path(str(self.id), root='greyhound_form_csv')
        request_and_write_csv_if_non_existing_file(greyhound_path, download_url, session)
        
    def csv_path(self):
        return build_and_check_path(str(self.id), root='greyhound_form_csv')
    

        
class GreyhoundForm:

    def __init__(self, raw_csv):
        self.form = csv.DictReader(raw_csv)
    
    def race(self): 
        return self.form
            
    