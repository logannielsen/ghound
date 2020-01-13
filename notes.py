"""https://fasttrack.grv.org.au/
Meeting/
Search?
MeetingDateFrom=01%2F08%2F2007& ### scrape year by year to get clean result
MeetingDateTo=01%2F08%2F2019& 
Status=&
TimeSlot=&
DayOfWeek=&
DisplayAdvertisedEvents=false&
AllTracks=False&S
electedTracks=Ballarat& ## TRack Iterable
searchbutton=Search"""

tracks_list = [Bendigo, Cranbourne, Geelong, Healesville,
                Horsham, Meadows (MEP), Sale, Sandown (SAP), 
                Sandown Park, Shepparton, The Meadows, Traralgon,
                Warragul, Warrnambool]


def construct_search_url(tracks_list):
    url ="https://fasttrack.grv.org.au/Meeting/"
    "Search?MeetingDateFrom=01%2F01%2Ff'{start_year}'"
    "&MeetingDateTo=01%2F08%2Ff'{end_year}'"
    "&DisplayAdvertisedEvents=false&AllTracks=False"
    "&SelectedTracks=f'{track}'&searchbutton=Search&page=3"
    start_year = 2018
    end_year = 2019