#! /usr/bin/env python
# coding: utf-8

"""This module contains all tests for the programm."""

from backend import parser
from backend import maps
from backend import media_wiki

import mediawiki
import googlemaps


class Testparser:
    """This class allow test parser."""

    def setup_method(self):
        """Initialize the parser to each new method used."""
        self.parser = parser.Parser()
        self.phrase_test = "Salut GrandPy ! Est-ce que tu connais l'adresse \
            d'OpenClassrooms ?"

    def testparsing(self):
        """Allows to use and verify the correct functioning of the parser."""
        parsed = self.parser.parse_the_phrase(self.phrase_test)
        assert parsed == "openclassrooms"

    def testnormalizer(self):
        normalised = self.parser.normalizer(self.phrase_test)
        assert normalised == [
            'salut',
            'grandpy',
            'est',
            'ce',
            'que',
            'tu',
            'connais',
            'l',
            'adresse',
            'd',
            'openclassrooms']

    def testpercentcorrespondence(self):
        percentcorrespondence = self.parser.percent_correspondence("grandy")
        assert percentcorrespondence == 92


class TestGoogleMapsearchID:
    """This class allow test the searche ID with api map place."""

    def setup_method(self):
        """Initialize Api google map and the name for search."""
        self.GoogleMap = maps.Mapsgoogle()
        self.name_search = "openclassrooms"

    def testsearchid(self, monkeypatch):
        """Using monkeypatch for create mock."""
        results = [{
            "place_id": "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"
            }]

        def mockreturn(request, params):
            """Contain return for mock setattr."""
            return results

        monkeypatch.setattr(
            googlemaps.Client,
            'places_autocomplete_query',
            mockreturn
            )
        idsearch = self.GoogleMap.search_id(self.name_search)
        assert idsearch == "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"


class TestGoogleMapsearchPlace:
    """This class allow test the search detail place with api map place."""

    def setup_method(self):
        """Initialize Api google map and id place for search."""
        self.GoogleMap = maps.Mapsgoogle()
        self.idsearch = "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

    def testsearchplace(self, monkeypatch):
        """Using monkeypatch for create mock."""
        results = {
            "result": {
                "name": "Openclassrooms",
                "address_components": {
                    0: {
                        "long_name": 7,
                        "types": {
                            0: "street_number"
                        }
                    },
                    1: {
                        "long_name": "Cité Paradis",
                        "types": {
                            0: "route"
                        }
                    },
                    2: {
                        "long_name": "75010",
                        "types": {
                            0: "postal_code"
                        }
                    },
                    3: {
                        "long_name": "Paris",
                        "types": {
                            0: "locality"
                        }
                    }
                },
                "geometry": {
                    "location": {
                        "lat": 48.8748465,
                        "lng": 2.3504873
                    }
                }
            }
        }

        def mockreturn(request, params):
            return results

        monkeypatch.setattr(
            googlemaps.Client,
            'place',
            mockreturn
            )

        name, adress, lat, lng = self.GoogleMap.search_info_id(self.idsearch)
        assert adress == {
            'num': 7,
            'code_postale': '75010',
            'rue': 'Cité Paradis',
            'ville': 'Paris'
            }
        assert lat == 48.8748465
        assert lng == 2.3504873
        assert name == "Openclassrooms"


class Testsearchwiki:
    """This class allow test the search wiki."""

    def setup_method(self):
        """Initialize Api media_wiki and fake adress for search."""
        self.wiki = media_wiki.Wiki()
        self.adress = {
            'num': 7,
            'rue': 'Cité Paradis',
            'code_postale': '75010',
            'ville': 'paris'
        }

    def testsearchwik(self, monkeypatch):
        """Using monkeypatch for create mock."""
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
    """This class allow test the search wiki history of place."""

    def setup_method(self):
        """Initialize Api media_wiki and name place for search history."""
        self.wiki = media_wiki.Wiki()
        self.name = "Cité Paradis"

    def testsearchhistory(self, monkeypatch):
        """Using monkeypatch for create mock."""
        class obj:
            def section(self, data):
                if data == "Origine du nom":
                    return "Elle porte ce nom en raison"
                elif data == "Situation et accès":
                    return "La cité Paradis est une ...."
        results = obj()

        def mockreturn(request, data):
            return results

        monkeypatch.setattr(mediawiki.MediaWiki, 'page', mockreturn)
        search_wiki = self.wiki.search_history(self.name)
        assert search_wiki == "Origine du nom :\n\
Elle porte ce nom en raison\
\n\n\nSituation et accès :\n\
La cité Paradis est une ...."
