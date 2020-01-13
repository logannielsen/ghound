from bs4 import BeautifulSoup
import os
import csv
import requests
import pandas as pd
import datetime

ghound_id = 142641723

url = f'https://fasttrack.grv.org.au/Dog/FormDownload/{ghound_id}'


# def request_session():
#     session = requests.Session()
#     session.header = {'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)Gecko/20100101 Firefox/34.0", "Accept-Encoding" : "gzip,deflate,sdch"}
#     return session

# def get_request(session, url):
#     request = session.get(url)
#     return request

# session = request_session()
# data = get_request(session, url)

# with open('dog_form_142641723.csv', 'w', encoding='utf8') as f:
#     cr = csv.writer(f)
#     for line in data.iter_lines():
#         cr.writerow(line.decode('utf-8').split(','))

# panda = pd.read_csv('dog_form_142641723.csv', delimiter = ',')
# print(panda)

# with open('dog_form_142641723.csv', 'r', encoding='utf8') as f:
#     fieldnames = ['Pl','Box','Wght','Dist','Trk','Race','Date','Time','BON','Mgin','1st/2nd(Time)','Split1','PIR','Comment','S/P','Grade','Hcap']
#     form = csv.DictReader(f, fieldnames=fieldnames)
#     for row in form:
#         print(row['Pl'], row['Box'])


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

class RaceStats():

    def __init__(self, raw_csv):
        global FIELD_NAMES
        self.form = csv.DictReader(raw_csv, fieldnames=FIELD_NAMES)

    def race(self): 
        for race_stats in self.form:
            yield race_stats

    
    


# class RaceHound(CSVBase):
    
#      def racehound_data(self):
#         for row in self.form:
#             self.place = row['Pl']
#             self.box = row['Box']
#             self.weight = row['Wght']
#             self.distance = row['Dist']
#             self.track = row['Trk']
#             self.race_number = row['Race']
#             self.date = row['Date']
#             self.time = row['Time']
#             self.best_on_night = row['BON']
#             self.margin = row['Mgin']
#             self.first_sec = row['1st/2nd(Time)']
#             self.split_1 = row['Split1']
#             self.pir = row['PIR']
#             self.comment = row['Comment']
#             self.sp = row['S/P']
#             self.grade = row['Grade']
#             self.hcap = row['Hcap']
#             yield self
            
    
with open(os.path.join('resources', 'dog_form_142641723.csv'), 'r', encoding='utf-8') as f:
    dog = RaceStats(f)
    for race in dog.race():
        print(race)