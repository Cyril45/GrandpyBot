#! /usr/bin/env python
# coding: utf-8

"""Contains the parser class which allows to cut a sentence."""

import unicodedata
from config import constant as const
from fuzzywuzzy import fuzz


class Parser:
    """The objects in this class are used to cut and clean sentences."""

    def __init__(self):
        """Initialise the words to delete."""
        self.stop_words = const.stop_words_genrique + const.stop_word_added
        self.stop_words = self.normalizer(self.stop_words)

    def normalizer(self, receive):
        """Clean word so they follow the same structure."""
        if isinstance(receive, list):
            receive = " ".join(receive)
        receive = unicodedata.normalize(
            'NFKD', receive
            ).encode(
                'ASCII', 'ignore'
                ).decode()
        receive = receive.lower()
        receive = ''.join(
          [x if x.isalpha() or x.isnumeric() else " " for x in receive]
          ).split()
        clean_list = list()
        for word in receive:
            if word not in clean_list:
                clean_list.append(word)
        return clean_list

    def percent_correspondence(self, mot_user):
        """Return percentage of correspondence with the stop words list."""
        purcent_return = 0
        for word in self.stop_words:
            purcent_match = fuzz.ratio(word, mot_user)
            if purcent_match > purcent_return:
                purcent_return = purcent_match
        return purcent_return

    def parse_the_phrase(self, phrase):
        """
        1.

        Allow to cut sentences and keep only
        the words to use for searches.
        """
        phrase = self.normalizer(phrase)
        phrase_finally = list()
        for mot_user in phrase:
            percent_of_corresp = self.percent_correspondence(mot_user)
            if percent_of_corresp < 90 and mot_user not in phrase_finally:
                if len(mot_user) >= 3 or (mot_user.isnumeric()):
                    phrase_finally.append(mot_user)
        phrase_finally = " ".join(phrase_finally)
        return phrase_finally
