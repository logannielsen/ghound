import datetime

tom = datetime.date.today() + datetime.timedelta(days=1)
print("{0:02d}".format(tom.day))
print(f"https://fasttrack.grv.org.au/Meeting/Search?"
    f"MeetingDateFrom={'{0:02d}'.format(tom.day)}"
    f"%2F{'{0:02d}'.format(tom.month)}%2F{'{0:02d}'.format(tom.year)}"
    f"&MeetingDateTo={'{0:02d}'.format(tom.day)}%2F{'{0:02d}'.format(tom.month)}"
    f"%2F{'{0:02d}'.format(tom.year)}&Status=&"
    f"TimeSlot=&DayOfWeek=&DisplayAdvertisedEvents=false&AllTracks=True"
    f"&SelectedTracks=AllTracks&searchbutton=Search")