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

    def get_weekly_schedule(self, id, week):
        query = {"id": id, "week": week}
        return self._get_soup(self.url, params=query)


def main():
    with open("data/room_ids.txt") as infile:
        room_ids = json.load(infile)

    tts = TimetableScraper()
    print(tts.get_weekly_schedule("0208_00_G.8", 1))


if __name__ == "__main__":
    main()
