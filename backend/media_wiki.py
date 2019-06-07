#! /usr/bin/env python
# coding: utf-8

"""Contains objects used with api mediawiki."""
import mediawiki


class Wiki:
    """Allows you to search info in mediawiki."""

    def __init__(self):
        """Initialize api mediawiki and language."""
        self.wikipedia = mediawiki.MediaWiki()
        self.wikipedia.language = "fr"

    def search_wiki(self, data):
        """Search establishment in mediawiki."""
        search = self.wikipedia.search(data["rue"] + " " + data["ville"])
        if search:
            return search[0]
        else:
            return None

    def search_history(self, search):
        """Search details of establishment in mediawiki."""
        history_search = self.wikipedia.page(search)
        if history_search:
            returned = ""
            if history_search.section("Origine du nom"):
                returned += "Origine du nom :\n" \
                    + history_search.section("Origine du nom") \
                    + "\n\n\n"

            if history_search.section("Situation et accès"):
                returned += "Situation et accès :\n" \
                    + history_search.section("Situation et accès")

            return returned
        else:
            return None
