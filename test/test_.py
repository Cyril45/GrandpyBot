#! /usr/bin/env python
# coding: utf-8

from backend import parser
from backend import maps
from backend import media_wiki

import mediawiki
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
                "address_components":{
                    0:{
                        "long_name":7,
                        "types":{
                            0:"street_number"
                        }
                    },
                    1:{
                        "long_name":"Cité Paradis",
                        "types":{
                            0:"route"
                        }
                    },
                    2:{
                        "long_name":"75010",
                        "types":{
                            0:"postal_code"
                        }
                    },
                    3:{
                        "long_name":"Paris",
                        "types":{
                            0:"locality"
                        }
                    }
                },
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
        assert adress == {'num': 7, 'code_postale': '75010', 'rue': 'Cité Paradis', 'ville': 'Paris'}
        assert lat == 48.8748465
        assert lng == 2.3504873
        assert name == "Openclassrooms"

class Testsearchwiki:
    def setup_method(self):
        self.wiki = media_wiki.wiki()
        self.adress = {
        'num': 7, 
        'rue': 'Cité Paradis', 
        'code_postale': '75010', 
        'ville': 'paris'
        }

    def testsearchwik(self, monkeypatch):
        results = [
            'Cité Paradis',
            'Vanessa Paradis',
            'Paris',
            'Paradis',
            'Paradis fiscal',
            'Les Enfants du paradis'
            ]
        def mockreturn(request, data):
            return results

        monkeypatch.setattr(mediawiki.MediaWiki, 'search', mockreturn)

        search_wiki = self.wiki.search_wiki(self.adress)
        assert search_wiki == "Cité Paradis"

class Testsearchhistory:
    def setup_method(self):
        self.wiki = media_wiki.wiki()
        self.name = "Cité Paradis"

    def testsearchhistory(self, monkeypatch):
        class obj:
            def section(self, data):
                if data == "Origine du nom":
                    return "Elle porte ce nom en raison de sa proximité avec la rue éponyme."
                elif data == "Situation et accès":
                    return "La cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43..."
        results = obj()

        def mockreturn(request, data):
            return results

        monkeypatch.setattr(mediawiki.MediaWiki, 'page', mockreturn)
        search_wiki = self.wiki.search_history(self.name)
        assert search_wiki == "Origine du nom :\nElle porte ce nom en raison de sa proximité avec la rue éponyme.\n\n\nSituation et accès :\nLa cité Paradis est une voie publique située dans le 10e arrondissement de Paris. Elle est en forme de té, une branche débouche au 43..."