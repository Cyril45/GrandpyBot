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

    def search_wiki_name(self, name, city):
        """Allow you to search by name and city."""
        try:
            search = self.wikipedia.search(name + " " + city)
            if search != []:
                return search
            else:
                return None
        except ValueError:
            return None

    def search_wiki_adress(self, street, city):
        """Allow you to search by street and city."""
        try:
            search = self.wikipedia.search(street + " " + city)
            if search != []:
                return search
            else:
                return None
        except ValueError:
            return None

    def search_history(self, name, adress):
        """Search details of establishment in mediawiki."""
        search_by_name = self.search_wiki_name(name, adress["ville"])
        search_by_adress = self.search_wiki_adress(
            adress["rue"],
            adress["ville"]
            )

        if search_by_name:
            for x in search_by_name:
                try:
                    history_search = self.wikipedia.page(x)
                    cat = history_search.categories
                    if any(
                        "monument" in i
                        or "Montagne" in i
                        or "Désert" in i
                            for i in cat):
                        return history_search.summary
                except mediawiki.exceptions.PageError:
                    pass
                except mediawiki.exceptions.DisambiguationError:
                    pass

        if search_by_adress:
            for x in search_by_adress:
                try:
                    history_search = self.wikipedia.page(x)
                    if history_search:
                        returned = ""
                        if history_search.section("Origine du nom"):
                            returned += "Origine du nom de la rue :<br />" \
                                + history_search.section("Origine du nom")

                        if history_search.section("Situation et accès"):
                            returned += "<br /><br />Situation et accès :\
                                <br />" + history_search.section(
                                    "Situation et accès"
                                    )
                        return returned
                except mediawiki.exceptions.PageError:
                    return None
        return None
