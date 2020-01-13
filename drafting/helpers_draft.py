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


def build_meeting_id_tuples(tracks_list):
    """ returns a list of tuples showing meeting_id and track_name"""
    urls = get_meeting_hrefs(tracks_list)
    for url in urls:
        code = url[0].split('/')
        meeting_id_tuple = (code[-1], url[1]) 
        yield meeting_id_tuple


def request_historical_meetings_results(tracks_list, session):
    """writes meeting results to file"""
    url_meetings_list = build_meeting_id_tuples(tracks_list)
    for meeting in url_meetings_list:
        full_path = create_file_path(meeting[1], meeting[0])
        create_directory(meeting[1])
        url = f'https://fasttrack.grv.org.au/RaceField/ViewRaces/{meeting[0]}'
        if not os.path.exists(f"{full_path}.txt"):
            page_text = get_request(session, url)
            with open(f"{full_path}.txt", "w") as f:
                f.write(page_text)

    
request_historical_meetings_results(tracks_list, session)



def get_race_linked_grey_hound_tuples(tracks_list):
    """yields greyhound ID and Name"""
    url_meetings_list = build_meeting_id_tuples(tracks_list)
    for meeting in url_meetings_list:
        full_path = create_file_path(meeting[1], meeting[0])
        race_meet_results = open_file(full_path)
        race_list = race_meet_results.find(class_ = "side-tab-container")
        print(meeting[0])
        if race_list is not None:
            race_hrefs = race_list.find_all('a', href=True)
            for race in race_hrefs:
                if not race.get_text() == "All Races":
                    race_id = race['href'].split('=')[-1]
                    yield (meeting[1], race_id , meeting[0])


def saving_all_race_to_file(tracks_list, session):
    race_meeting_info = get_race_linked_grey_hound_tuples(tracks_list)
    for race in race_meeting_info:
        print(race)
        url = f'https://fasttrack.grv.org.au/RaceField/ViewRaces/{race[2]}?raceId={race[1]}'
        print(url)
        file_path = os.path.join('race_files', f'{race[0]}', f'{race[2]}')
        file_name = race[1]
        full_path = create_file_path(file_path, file_name)
        create_directory(file_path)
        if not os.path.exists(f"{full_path}.txt"):
            page_text = get_request(session, url)
            with open(f"{full_path}.txt", "w") as f:
                f.write(page_text)


# saving_all_race_to_file(tracks_list, session)

def get_grey_hounds(tracks_list):
    """yields greyhound ID and Name"""
    race_meet_id_tuples = get_race_linked_grey_hound_tuples(tracks_list)
    for race in race_meet_id_tuples:
        file_path = os.path.join('race_files', f'{race[0]}', f'{race[2]}')
        file_name = race[1]
        full_path = create_file_path(file_path, file_name)
        race_meet_results = open_file(full_path)
        ghound_race_tables = race_meet_results.find('table', class_ = "raceResultsTable")
        # print(ghound_race_tables)
        ghound_list = get_greyhoud_hrefs(ghound_race_tables)
        print(ghound_list)
        greyhound_id_tuple = process_greyhounds_ID_and_name(ghound_list, race)
        yield (greyhound_id_tuple)


def get_greyhoud_hrefs(ghound_race_tables):
    href_lists = ghound_race_tables.find_all('a', href=True)
    return href_lists
    

def process_greyhounds_ID_and_name(ghound_list, race):
    for ghound in ghound_list:
        ghound_id = ghound['href'].split('/')[-1]
        ghound_name  = ghound.get_text()
        ghound_name_split = ghound_name.split('(late')
        if len(ghound_name_split) >= 1:
            ghound_name = ghound_name_split[-1].split(')')[0]
        yield (ghound_id, ghound_name, race[0], race[1], race[2])
            




