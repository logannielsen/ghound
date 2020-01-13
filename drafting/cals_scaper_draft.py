import requests
import os
import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup

tracks_list = ["Bendigo", "Cranbourne", "Geelong", "Healesville",
                "Horsham", "Meadows+%28MEP%29", "Sale", "Sandown+%28SAP%29", 
                "Sandown+Park", "Shepparton", "The+Meadows",
                "Warragul", "Warrnambool"]

def construct_historical_search_tup(tracks_list):
    """ goes through month by month and searches the calendar
    to build search tuples for race meets"""
    months = range(1,datetime.datetime.now().month+1)
    for track in tracks_list:
        for month in months:
            if not month == datetime.datetime.now().month:
                if month <= 11:
                    start_month = "{0:02d}".format(month)
                    end_month = "{0:02d}".format(month+1)
                    start_year = datetime.datetime.now().year
                    end_year = datetime.datetime.now().year
                if month == 12:
                    start_month = "{0:02d}".format(month)
                    end_month = "01"
                    end_year = start_year + 1
                    start_year = datetime.datetime.now().year
                    end_year = datetime.datetime.now().year + 1
                yield (track, start_month, end_month, start_year, end_year)


def build_calendar_search_url(info_tuple):
    return f"https://fasttrack.grv.org.au/Meeting/Search?MeetingDateFrom=01%2F{info_tuple[1]}%2F{info_tuple[3]}&MeetingDateTo=01%2F{info_tuple[2]}%2F{info_tuple[4]}&DisplayAdvertisedEvents=false&AllTracks=False&SelectedTracks={info_tuple[0]}&searchbutton=Search"

def request_session():
    session = requests.Session()
    session.header = {'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)Gecko/20100101 Firefox/34.0", "Accept-Encoding" : "gzip,deflate,sdch"}
    return session

session = request_session()

def get_request(session, url):
    request = session.get(url)
    return request.text

def construct_calendar_file_path(info_tuple):
    """" saves historical greyhound data to the greys calendar file """
    file_path = f"greys_cal/{info_tuple[0]}"
    file_name = f"{info_tuple[3]}_{info_tuple[1]}"
    return file_path, file_name


def create_file_path(file_path, file_name, root=None):
    if root is None:
        full_path = os.path.join(file_path, file_name)
    else:
        full_path = os.path.join(root, file_path, file_name)
    return full_path

def create_directory(file_path, root=None):
    if root is None:
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    else:
        path = os.path.join(root, file_path)
        if not os.path.exists(path):
            os.makedirs(path)
 


def scrape_historical_greyhound_calendars(tracks_list, session):
    urls = construct_historical_search_tup(tracks_list)
    construction_tuples = construct_historical_search_tup(tracks_list)
    for tup in construction_tuples: 
        url = build_calendar_search_url(tup)
        file_path, file_name = construct_calendar_file_path(tup)
        full_path = create_file_path(file_path, file_name)
        create_directory(file_path)
        if not os.path.exists(f"{full_path}.txt"):
            page_text = get_request(session, url)
            with open(f"{full_path}.txt", "w") as f:
                f.write(page_text)

def open_file(full_path):
    with open(f"{full_path}.txt") as f:
        return BeautifulSoup(f, 'html.parser')

def find_all_tbody(soup_page):
    tbody = soup_page.find('tbody')
    return tbody

def find_href(tbody):
    for href in tbody.find_all('a', href=True):
        yield href


def get_meeting_hrefs(tracks_list):
    """ pulls meeting ids from calendar of meeting
    yields: meeting_id and track_name"""
    construction_tuples = construct_historical_search_tup(tracks_list)
    for tup in construction_tuples:
        url = build_calendar_search_url(tup)
        file_path, file_name = construct_calendar_file_path(tup)
        full_path = create_file_path(file_path, file_name)
        soup_page = open_file(full_path)
        tbody = find_all_tbody(soup_page)
        hrefs = find_href(tbody)
        for ref in hrefs:
            yield ref['href'], tup[0]

scrape_historical_greyhound_calendars(tracks_list, session)

class HTMLBase():

    def __init__(self, raw_html):
        self.soup = BeautifulSoup(raw_html, 'html.parser')

class Calendar(HTMLBase):
    
    def race_meets(self):
        """returns a list meeting objects
        each meeting has a meeting_id, track and is_finalised attribute"""
        return [Meet(meet) for meet in self.soup.find('tbody').find_all('tr')]
    

class Meet:

    def __init__(self, race_meets):
        self.race_meet = race_meets
        super().__init__()

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

# with open(os.path.join('resources', '2019_01.txt'), 'r', encoding='utf-8') as f:
#     meet = Calendar(f.read())
#     for meeting in meet.race_meets():
#         print(meeting.track, meeting.meeting_id, meeting.is_meet_final, meeting.href)

with open(os.path.join('resources', 'page_0_races.txt'), 'r', encoding='utf-8') as f:
    races = MeetRaces(f.read())
    print(races.races_id_list)