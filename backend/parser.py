#! /usr/bin/env python
# coding: utf-8

"""Contains the parser class which allows to cut a sentence."""

import unicodedata
from config import constant as const


class Parser:
    """The objects in this class are used to cut and clean sentences."""

    def __init__(self):
        """Initialise the words to delete."""
        self.stop_words = const.stop_words_genrique + const.stop_word_added

    def parse_the_phrase(self, phrase):
        """
        1.
        
        Allow to cut sentences and keep only
        the words to use for searches.
        """
        phrase = unicodedata.normalize(
            'NFKD', phrase
            ).encode(
                'ASCII', 'ignore'
                ).decode()
        phrase = phrase.lower()
        phrase = ''.join(
          [x if x.isalpha() or x.isnumeric() else " " for x in phrase]
          ).split()
        phrase_finally = list()
        for mot in phrase:
            if mot not in self.stop_words and mot not in phrase_finally:
                if len(mot) >= 3 or (mot.isnumeric()):
                    phrase_finally.append(mot)
        phrase_finally = str(" ".join(phrase_finally))
        return phrase_finally
