import re
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


class RoomIdScraper(object):
    def __init__(self):
        self.base_url = "https://www.ed.ac.uk/"
        self.campuses_url = (
            self.base_url
            + "timetabling-examinations/timetabling/room-bookings/bookable-rooms3"
        )
        self.session = requests.Session()

    def _get_soup(self, url):
        res = self.session.get(url)
        return BeautifulSoup(res.text, "lxml")

    def get_campuses(self):
        """Method to return campus tag objects for further parsing.
        
        Returns:
            A list of all campus tag objects.

        Example:
            >>> RoomIdScraper().get_campuses()
            [<a href="/link/to/campus1">Campus 1</a>, <a href="/link/to/campus2">Campus 2</a>]

        """
        soup = self._get_soup(self.campuses_url)
        return soup.find("div", class_="content").find_all("a")

    def get_buildings(self, campus):
        """Method to return all building soup objects in a given campus for further parsing.
        
        Args:
            campus (bs4.element.Tag): campus whose buildings we are interested in.
        
        Returns:
            A list of all building tag objects.

        Example:
            >>> RoomIdScraper().get_buildings(campus1)
            [<div class="item-list"> <h3>Building 1</h3>
             <ul><li class="views-row views-row-1 views-row-odd views-row-first views-row-last">
             <a href="/room/room_id_1">Room 1</a>
             <span class="views-field views-field-field-capacity">Capacity: 64</span>
             <span class="views-field views-field-field-allocated">1. Centrally Allocated Space</span></li>
             </ul></div>]
             
        """
        campus_url = campus.get("href")
        soup = self._get_soup(self.base_url + campus_url)
        return soup.find_all("div", class_="item-list")

    def get_rooms(self, building):
        """Method to return all room names and ids in a given building.
        
        Args:
            building (bs4.element.Tag): building whose rooms we are interested in.
        
        Returns:
            A tuple of building name (str) and a dictionary of room id-name pairs.

        Example:
            >>> RoomIdScraper().get_rooms(building1)
            ("Building 1", {"room_id_1": "Room 1", "room_id_2": "Room 2"})
        """

        name = building.find("h3").string
        rooms = {
            room.get("href").replace("/room/", ""): room.string
            for room in building.find_all("a")
        }
        return name, rooms


def main():
    ris = RoomIdScraper()
    room_infos = [
        ris.get_rooms(building)
        for campus in ris.get_campuses()
        for building in ris.get_buildings(campus)
    ]

    from pprint import pprint

    pprint(room_infos)


if __name__ == "__main__":
    main()
