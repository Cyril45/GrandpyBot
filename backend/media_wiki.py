#! /usr/bin/env python
# coding: utf-8

import mediawiki

class wiki:
    def __init__(self):
        self.wikipedia = mediawiki.MediaWiki()
        self.wikipedia.language = "fr"

    def search_wiki(self, data):
        search = self.wikipedia.search(data["rue"] + " " + data["ville"])
        if search:
            return search[0]
        else: 
            return None

    def search_history(self, search):
        history_search = self.wikipedia.page(search)
        if history_search:
            returned = ""
            if history_search.section("Origine du nom"):
                returned += "Origine du nom :\n" + history_search.section("Origine du nom") + "\n\n\n"

            if history_search.section("Situation et accès"):
                returned += "Situation et accès :\n" + history_search.section("Situation et accès")

            return returned
        else:
            return None