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
from greyhound_object_model import RaceStatsTable, GreyhoundTable, RaceTable, TrackTable, sess
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


if __name__ == "__main__":
    req_session = request_session()
    with open(os.path.join('resources', 'tomorrow_cal.txt'), 'r', encoding='utf-8') as f:
        calendar = Calendar(f.read())
        calendar.save_meets(req_session)
        meets = calendar.race_meets()
        for meeting in meets:
            if meeting.is_meet_final:
                race_card_list = MeetRaces(read_file(meeting.file_path())).races_id_list
                for race_id in race_card_list:
                    if race_id != "0":
                        race_path = build_and_check_path(race_id, 
                                            meeting.track,
                                            root="sample_races")
                        race_url = f"https://fasttrack.grv.org.au/RaceField/ViewRaces/{meeting.meeting_id}?raceId={race_id}"
                        request_and_write_if_non_existing_file(race_path, race_url, req_session)
                        races = Race(read_file(race_path))
                        # print(race_id, races.number, races.time, races.date, races.first_prize,
                        # races.second_prize, races.third_prize, races.distance, races.race_type,
                        # races.quinella_price, races.exacta_price, races.trifecta_price, races.first4_price)
                        print("*"*100)
                        greyhounds = races.get_greys()
                        print(greyhounds)
                        for hound in greyhounds:
                            hound.save_and_return_greyhound_form(req_session)
                            q = sess.query(GreyhoundTable.id).filter(GreyhoundTable.id==hound.id).one_or_none()
                            print(hound.name, hound.id)
                            if not q:
                                ghound = GreyhoundTable(id=hound.id, name=hound.name)
                                sess.add(ghound)
                                sess.flush()
                                print(hound.name, hound.id)
                            with open(f"{hound.csv_path()}.csv", "r", encoding='utf-8') as f:
                                form = GreyhoundForm(f)
                                for race in form.race():
                                    if race['Pl'].isdigit():
                                        print(race['Pl'])
                                        print(race['Trk'])
                                        print(hound.id)
                                        q2 = sess.query(TrackTable).filter(TrackTable.track_name==race['Trk'].strip()).one_or_none()
                                        print(q2)
                                        if not q2:
                                            new_track = TrackTable(track_name=race['Trk'])
                                            sess.add(new_track)
                                            sess.flush()
                                        xy = sess.query(TrackTable).filter(TrackTable.track_name==race['Trk'].strip()).one_or_none()
                                        if xy.id:
                                            print(f'here {xy.id}')
                                            q3 = sess.query(RaceTable, TrackTable).filter(TrackTable.id==xy.id).\
                                                                            filter(RaceTable.date==datetime.strptime(race['Date'], '%d/%m/%Y')).\
                                                                            filter(RaceTable.race_number == int(search(r'\d+', race['Race']).group(0))).one_or_none()
                                            if not q3:
                                                print(f'here now {xy.id}')
                                                new_race = RaceTable(track_id=xy.id, date=datetime.strptime(race['Date'], '%d/%m/%Y'), race_number=int(search(r'\d+', race['Race']).group(0)))
                                                sess.add(new_race)
                                                sess.flush()
                                                sess.commit()
                                                print(xy.id)
                                                gq = sess.query(RaceTable).filter(RaceTable.track_id==xy.id).\
                                                                            filter(RaceTable.date==datetime.strptime(race['Date'], '%d/%m/%Y')).\
                                                                            filter(RaceTable.race_number == int(search(r'\d+', race['Race']).group(0))).one_or_none()
                                                print(gq)
                                                race_stats = RaceStatsTable(greyhound_id=hound.id,
                                                                race = gq.id,
                                                                distance = int(race['Dist']),
                                                                weight = race['Wght'],
                                                                time = race['Time'],
                                                                bon = race['BON'],
                                                                margin = race['Mgin'],
                                                                split_1 = race['Split1'],
                                                                pir = race['PIR'],
                                                                Comment = race['Comment'],
                                                                grade = race['Grade'],
                                                                sp = race['S/P'],
                                                                hcap = race['Hcap']
                                    )
                                                sess.add(race_stats)
                                                sess.flush()
                                                sess.commit()
    
                            
                            
                            
                        