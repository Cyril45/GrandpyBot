#! /usr/bin/env python
# coding: utf-8

import googlemaps
from config import constant as const

class Mapsgoogle:
    def __init__(self):
        self.gog = googlemaps.Client(key=const.api_key)
    
    def search_id(self, search):
        result = self.gog.places_autocomplete_query(search)
        return result[0]["place_id"]

    def search_info_id(self, id_adresse):
        result = self.gog.place(id_adresse)
        name = result["result"]["name"]
        adress = result["result"]["formatted_address"]
        lat = result["result"]["geometry"]["location"]["lat"]
        lng = result["result"]["geometry"]["location"]["lng"]
        return name, adress, lat, lng


if __name__ == "__main__":
    objmap = Mapsgoogle()
    search = "openclassrrom's"
    test= objmap.search_id(search)
    name, adress, lat, lng = objmap.search_info_id(test)
    print(name, adress, lat, lng)
