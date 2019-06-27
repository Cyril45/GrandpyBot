#! /usr/bin/env python
# coding: utf-8

"""This module contains all tests for the programm."""


from grandpyapp.backend import media_wiki

import mediawiki


class Testsearchwiki:
    """This class allow test the search wiki."""

    def setup_method(self, monkeypatch):
        """Initialize Api media_wiki and fake adress for search."""

        self.name = "Openclassrooms"
        self.adress = {
            'num': '7',
            'rue': 'Cité Paradis',
            'code_postale': '75010',
            'ville': 'Paris'
            }

    def testsearchwikname(self, monkeypatch):
        """Using monkeypatch for create mock."""

        class obj:

            def search(self, data):
                return [
                    'OpenClassrooms',
                    'Massive Open Online Course',
                    'Zeste de Savoir',
                    'École polytechnique (France)'
                    ]

        results = [
            'OpenClassrooms',
            'Massive Open Online Course',
            'Zeste de Savoir',
            'École polytechnique (France)'
            ]

        results2 = obj()

        def mockreturn():
            return results2

        monkeypatch.setattr(mediawiki, 'MediaWiki', mockreturn)
        self.wiki = media_wiki.Wiki()

        search_wiki = self.wiki.search_wiki_name(
            self.name,
            self.adress["ville"]
            )
        assert search_wiki == results

    def testsearchwikadress(self, monkeypatch):
        """Using monkeypatch for create mock."""

        class obj:
            def search(self, data):
                return [
                    'Cité Paradis',
                    'Vanessa Paradis',
                    'Paris',
                    'Paradis',
                    'Les Enfants du paradis'
                ]

        results = [
                    'Cité Paradis',
                    'Vanessa Paradis',
                    'Paris',
                    'Paradis',
                    'Les Enfants du paradis'
                ]

        results2 = obj()

        def mockreturn():
            return results2

        monkeypatch.setattr(mediawiki, 'MediaWiki', mockreturn2)

        self.wiki = media_wiki.Wiki()
        search_wiki = self.wiki.search_wiki_adress(
            self.adress["rue"],
            self.adress["ville"]
            )
        assert search_wiki == results

    def testsearchwikdetail(self, monkeypatch):
        """Using monkeypatch for create mock."""
        class objB:
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

        class obj:
            def page(self, data):
                return objB()

            def search(self, data):
                return [
                    'OpenClassrooms',
                    'Massive Open Online Course',
                    'Zeste de Savoir',
                    'École polytechnique (France)'
                ]

        search_result = "Origine du nom de la rue :<br />\
Elle porte ce nom en raison<br /><br />Situation et accès :\
                \
                <br />La cité Paradis est une ...."

        results3 = obj()

        def mockreturn3():
            return results3

        monkeypatch.setattr(mediawiki, 'MediaWiki', mockreturn3)

        self.wiki = media_wiki.Wiki()
        search_wiki = self.wiki.search_history(self.name, self.adress)
        assert search_wiki == search_result
