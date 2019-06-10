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


class TestGoogleMap:
    """This class allow test the searche ID with api map place."""

    def setup_method(self):
        """Initialize Api google map and the name for search."""
        self.GoogleMap = maps.Mapsgoogle()
        self.name = "Openclassrooms"
        self.idsearch = "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

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
        idsearch = self.GoogleMap.search_id(self.name)
        assert idsearch == "ChIJIZX8lhRu5kcRGwYk8Ce3Vc8"

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
        assert name == self.name


class Testsearchwiki:
    """This class allow test the search wiki."""

    def setup_method(self):
        """Initialize Api media_wiki and fake adress for search."""
        self.wiki = media_wiki.Wiki()
        self.name = "Openclassrooms"
        self.adress = {
            'num': '7',
            'rue': 'Cité Paradis',
            'code_postale': '75010',
            'ville': 'Paris'
            }

    def testsearchwikname(self, monkeypatch):
        """Using monkeypatch for create mock."""
        results = [
            'OpenClassrooms',
            'Massive Open Online Course',
            'Zeste de Savoir',
            'École polytechnique (France)'
            ]

        def mockreturn(request, data):
            return results

        monkeypatch.setattr(mediawiki.MediaWiki, 'search', mockreturn)

        search_wiki = self.wiki.search_wiki_name(
            self.name,
            self.adress["ville"]
            )
        assert search_wiki == results

    def testsearchwikadress(self, monkeypatch):
        """Using monkeypatch for create mock."""
        results = [
            'Cité Paradis',
            'Vanessa Paradis',
            'Paris',
            'Paradis',
            'Les Enfants du paradis'
        ]

        def mockreturn(request, data):
            return results

        monkeypatch.setattr(mediawiki.MediaWiki, 'search', mockreturn)

        search_wiki = self.wiki.search_wiki_adress(
            self.adress["rue"],
            self.adress["ville"]
            )
        assert search_wiki == results

    def testsearchwikdetail(self, monkeypatch):
        """Using monkeypatch for create mock."""
        class obj:
            def section(self, data):
                if data == "Origine du nom":
                    return "Elle porte ce nom en raison"
                elif data == "Situation et accès":
                    return "La cité Paradis est une ...."

            @property
            def categories(self):
                return [
                    'Catégorie:Plate-forme pédagogique',
                    'Catégorie:Site web en français',
                    'Catégorie:Site web français',
                    'Catégorie:Site web sur les sciences'
                    ]

        search_result = """Origine du nom :\nElle porte ce nom en raison\n\n\n\
Situation et accès :\nLa cité Paradis est une ...."""
        results1 = [
            'OpenClassrooms',
            'Massive Open Online Course',
            'Zeste de Savoir',
            'École polytechnique (France)'
            ]

        results2 = [
            'Cité Paradis',
            'Vanessa Paradis',
            'Paris',
            'Paradis',
            'Les Enfants du paradis'
        ]
        results3 = obj()

        def mockreturn1(request, name, adress):
            return results1

        def mockreturn2(request, name, adress):
            return results2

        def mockreturn3(request, x):
            return results3

        monkeypatch.setattr(media_wiki.Wiki, 'search_wiki_name', mockreturn1)
        monkeypatch.setattr(media_wiki.Wiki, 'search_wiki_adress', mockreturn2)
        monkeypatch.setattr(mediawiki.MediaWiki, 'page', mockreturn3)

        search_wiki = self.wiki.search_history(self.name, self.adress)
        assert search_wiki == search_result
