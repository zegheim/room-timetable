import re
import requests
from bs4 import BeautifulSoup


class RoomIdScraper(object):
    def __init__(self):
        self.url = "https://www.ed.ac.uk/timetabling-examinations/timetabling/room-bookings/bookable-rooms3"
        self.session = requests.Session()
        self.room_ids = []

    def get_soup(self, url):
        res = self.session.get(url)
        return BeautifulSoup(res.text, "lxml")

    def get_campuses(self):
        res = self.session.get(self.url)
        soup = BeautifulSoup(res.text, "lxml")
