#! /usr/bin/env python
# coding: utf-8

from grandpyApp.static.backend import maps
import googlemaps


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
