#! /usr/bin/env python
# coding: utf-8

"""This module contains all tests for the programm."""


from grandpyApp.backend import media_wiki

import mediawiki


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
