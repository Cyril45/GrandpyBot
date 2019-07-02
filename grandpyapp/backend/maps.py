#! /usr/bin/env python
# coding: utf-8
"""Contains objects used with api google."""

import googlemaps
import config as const


class Mapsgoogle:
    """Allows you to search maps."""

    def __init__(self):
        """Initialize api with the google API key."""
        self.gog = googlemaps.Client(key=const.API_KEY)

    def search_id(self, search):
        """Get back id of a place."""
        if search != "":
            result = self.gog.places_autocomplete_query(search)
            try:
                if "place_id" in result[0].keys():
                    return result[0]["place_id"]
                else:
                    description = result[0]["description"]
                    result = self.gog.places(description)
                    return result["results"][0]["place_id"]
            except IndexError:
                return None
        else:
            return None

    def search_info_id(self, id_adresse):
        """Retrieve the details of a place with the id."""
        result = self.gog.place(id_adresse)
        adress = {
            "num": "",
            "rue": "",
            "code_postale": "",
            "ville": ""
        }
        i = 0
        while i < len(result["result"]["address_components"]):
            if result["result"]["address_components"][i]["types"][0] \
              == "street_number":
                adress["num"] =\
                  result["result"]["address_components"][i]["long_name"]

            elif result["result"]["address_components"][i]["types"][0] \
              == "route":
                adress["rue"] =\
                  result["result"]["address_components"][i]["long_name"]

            elif result["result"]["address_components"][i]["types"][0] \
              == "locality":
                adress["ville"] =\
                  result["result"]["address_components"][i]["long_name"]

            elif result["result"]["address_components"][i]["types"][0] \
              == "postal_code":
                adress["code_postale"] =\
                  result["result"]["address_components"][i]["long_name"]

            i += 1
        name = result["result"]["name"]
        lat = result["result"]["geometry"]["location"]["lat"]
        lng = result["result"]["geometry"]["location"]["lng"]
        return name, adress, lat, lng
