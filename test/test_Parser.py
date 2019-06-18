#! /usr/bin/env python
# coding: utf-8

from grandpyApp.backend import parser


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
