#! /usr/bin/env python
# coding: utf-8

#mock => webinaire de thierry

import requests
import json
class Mapsgoogle:
    def __init__(self):
        self.API_KEY = "AIzaSyBygna5eJyviC7F27gMxtOs_Xs2Bt4bL8k"
    
    def search_id(self, search):
        params_get = {
                    "key": self.API_KEY,
                    "input": search
                    }
        read = requests.get('https://maps.googleapis.com/maps/api/place/queryautocomplete/json',params=params_get)
        if isinstance(read, requests.models.Response):
            data = read.json()
        else:
            data = read
        return data["predictions"][0]["place_id"]

    def search_info_id(self, id_adresse):
        params_get = {
                    "key": self.API_KEY,
                    "placeid": id_adresse,
                    "fields": "name,geometry,formatted_address"
                    }

        read = requests.get('https://maps.googleapis.com/maps/api/place/details/json',params=params_get)
        data = read.json()

        name = data["result"]["name"]
        adress = data["result"]["formatted_address"]
        lat = data["result"]["geometry"]["location"]["lat"]
        lng = data["result"]["geometry"]["location"]["lng"]
        return name, adress, lat, lng

if __name__ == "__main__":
    print("pouloulou")
    objmap = Mapsgoogle()
    search = "openclassrooms"
    print(objmap.search_id(search))