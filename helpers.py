import requests
import os
import csv
from datetime import datetime
from decimal import Decimal
from re import sub, search
from urllib.parse import urlparse
from bs4 import BeautifulSoup

def request_session():
    session = requests.Session()
    session.header = {'User-Agent' : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0)Gecko/20100101 Firefox/34.0", "Accept-Encoding" : "gzip,deflate,sdch"}
    return session

def get_request(session, url):
    request = session.get(url)
    return request.text

def form_request(session, url):
    request = session.get(url)
    return request

def request_and_write_if_non_existing_file(full_path, url, session):
        # checks if a given file path exists: 
        # if yes(file does exist): do nothing
        # if no(fiel does not exist): hit endpoint and write the file"""

    if not os.path.exists(f"{full_path}.txt"):
        page_text = get_request(session, url)
        with open(f"{full_path}.txt", "w") as f:
            f.write(page_text)

def request_and_write_csv_if_non_existing_file(full_path, url, session):
    if not os.path.exists(f"{full_path}.csv"):
        page_text = form_request(session, url)
        with open(f"{full_path}.csv", "w", encoding='utf8') as f:
            cr = csv.writer(f)
            for line in page_text.iter_lines():
                cr.writerow(line.decode('utf-8').split(','))

def build_and_check_path(file_name, *args, root=None):
    if root:
        args = (root,) + args
        file_path = os.path.join(*args)
        if not os.path.exists(file_path):
            os.makedirs(file_path)
    return os.path.join(file_path, file_name)

def read_file(full_path):
    with open(f"{full_path}.txt", "r") as f:
        return f.read()
    
def read_csv_file(full_path):
    with open(f"{full_path}.csv", "r", encoding='utf-8') as f:
        return f.read()

def race_or_trial(race_string):
    return int(search(r'\d+', race_string).group(0))

