import json
import requests
from bs4 import BeautifulSoup


class TimetableScraper(object):
    def __init__(self):
        self.url = "https://www.ted.is.ed.ac.uk/UOE1920_SWS/roomtimetable.asp"
        self.session = requests.Session()

    def _get_soup(self, url, **kwargs):
        res = self.session.get(url, **kwargs)
        return BeautifulSoup(res.text, "lxml")
