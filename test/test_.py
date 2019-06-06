#! /usr/bin/env python
# coding: utf-8

from backend import parser
from backend import maps
import googlemaps

class Testparser:
    def setup_method(self):
        self.parser = parser.Parser()
        self.phrase_test = "Salut GrandPy ! Est-ce que tu connais l'adresse d'OpenClassrooms ?"

    def testparsing(self):
        parsed = self.parser.parse_the_phrase(self.phrase_test)
        print(parsed)
        assert parsed == "openclassrooms"

class TestGoogleMapsearchID:
    def setup_method(self):
        self.GoogleMap = maps.Mapsgoogle()
        self.name_search = "openclassrooms"

    def testsearchid(self, monkeypatch):
        results = [{
            "place_id" : "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"
            }]
        def mockreturn(request, params):
            return results

        monkeypatch.setattr(googlemaps.Client, 'places_autocomplete_query', mockreturn)
        idsearch = self.GoogleMap.search_id(self.name_search)
        assert idsearch == "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

class TestGoogleMapsearchPlace:
    def setup_method(self):
        self.GoogleMap = maps.Mapsgoogle()
        self.idsearch = "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

    def testsearchplace(self, monkeypatch):
        results = {
            "result":{
                "name": "Openclassrooms",
                "formatted_address":"7 Cité Paradis, 75010 Paris, France",
                "geometry":{
                    "location":{
                        "lat":48.8748465,
                        "lng":2.3504873
                    }
                }
            }
        }
        def mockreturn2(request, params):
            return results

        monkeypatch.setattr(googlemaps.Client, 'place', mockreturn2)

        name, adress, lat, lng = self.GoogleMap.search_info_id(self.idsearch)
        assert adress == "7 Cité Paradis, 75010 Paris, France"
        assert lat == 48.8748465
        assert lng == 2.3504873
        assert name == "Openclassrooms"



    