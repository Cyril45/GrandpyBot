#! /usr/bin/env python
# coding: utf-8

import googlemaps
from config import constant as const

class Mapsgoogle:
    def __init__(self):
        self.gog = googlemaps.Client(key=const.api_key)
    
    def search_id(self, search):
        result = self.gog.places_autocomplete_query(search)
        print(result[0]["place_id"])
        return result[0]["place_id"]

    def search_info_id(self, id_adresse):
        result = self.gog.place(id_adresse)
        adress ={
            "num" : "",
            "rue" : "",
            "code_postale" : "",
            "ville" : ""
        }
        i=0
        while i < len(result["result"]["address_components"]):
            if result["result"]["address_components"][i]["types"][0] == "street_number":
                adress["num"] = result["result"]["address_components"][i]["long_name"]
            elif result["result"]["address_components"][i]["types"][0] == "route":
                adress["rue"] = result["result"]["address_components"][i]["long_name"]
            elif  result["result"]["address_components"][i]["types"][0] == "locality":
                adress["ville"] = result["result"]["address_components"][i]["long_name"]
            elif result["result"]["address_components"][i]["types"][0] == "postal_code":
                adress["code_postale"] = result["result"]["address_components"][i]["long_name"]
            i += 1
        name = result["result"]["name"]
        lat = result["result"]["geometry"]["location"]["lat"]
        lng = result["result"]["geometry"]["location"]["lng"]
        return name, adress, lat, lng