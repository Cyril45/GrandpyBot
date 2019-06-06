#! /usr/bin/env python
# coding: utf-8
import parser
import maps
import requests
from io import BytesIO
import json


class Testparser:

    def setup_method(self):
        self.parser = parser.Parser()
        self.phrase_test = "wesh d'OpenClassrooms ?"

    def testparsing(self):
        parsed = self.parser.parse_the_phrase(self.phrase_test)
        print(parsed)
        assert parsed == "openclassrooms"

class TestGoogleMapsearchID:

    def setup_method(self):
        self.GoogleMap = maps.Mapsgoogle()
        self.search = "openclassrooms"

    def testsearchid(self, monkeypatch):
        results = {
            "predictions" : [{
                "place_id" : "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"
                }]
            }
        def mockreturn(request, params):
            return results

        monkeypatch.setattr(requests, 'get', mockreturn)
        idsearch = self.GoogleMap.search_id("blo")
        assert idsearch == "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"


class TestGoogleMapsearchPlace:
    def setup_method(self):
        self.GoogleMap = maps.Mapsgoogle()
        self.idsearch = "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

    def testsearchplace(self):
        name, adress, lat, lng = self.GoogleMap.search_info_id(self.idsearch)
        assert adress == "7 Cité Paradis, 75010 Paris, France"
        assert lat == 48.8748465
        assert lng == 2.3504873
        assert name == "Openclassrooms"



    