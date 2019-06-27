#! /usr/bin/env python
# coding: utf-8

"""Enables user-requested URL routing."""

from flask import Flask, request, render_template, jsonify
from grandpyapp.backend import maps, parser, media_wiki
import config
from random import randint

app = Flask(__name__)
# app.config.from_object('config')


@app.route('/')
@app.route('/index/')
def index():
    """Leads to site index."""
    return render_template('index.html', API_KEY=config.API_KEY)


@app.route('/search', methods=['post'])
def search():
    """Leads to search page."""
    if request.method == 'POST':
        par = parser.Parser()
        gmap = maps.Mapsgoogle()
        wiki = media_wiki.Wiki()
        phrase = request.form['search']
        search = par.parse_the_phrase(phrase)
        info_id = gmap.search_id(search)
        if info_id is None:
            phrase_adresse = config.ADRESS_NOT_RETRIEVED[
                randint(0, len(config.ADRESS_NOT_RETRIEVED)-1)
                ]
            return jsonify(
                phBotAdre=phrase_adresse,
                existAdress=False
            )
        else:
            index_aleat_adress = randint(0, len(config.ADRESS_RETRIEVED)-1)
            phrase_adresse = config.ADRESS_RETRIEVED[index_aleat_adress]

            name, adress, lat, lng = gmap.search_info_id(info_id)
            search_detail_wiki = wiki.search_history(name, adress)
            if search_detail_wiki is None:
                index_aleat_wiki = randint(0, len(config.WIKI_NOT_RETRIEVED)-1)
                phrase_wiki = config.WIKI_NOT_RETRIEVED[index_aleat_wiki]
                phBotWik = phrase_wiki
                extWiki = False
            else:
                index_aleat_wiki = randint(0, len(config.WIKI_RETRIEVED)-1)
                phrase_wiki = config.WIKI_RETRIEVED[index_aleat_wiki]
                phBotWik = phrase_wiki
                extWiki = True

            return jsonify(
                existAdress=True,
                phBotAdre=phrase_adresse,
                existWiki=extWiki,
                phBotWik=phBotWik,
                name=name,
                adress=adress,
                lat=lat,
                lng=lng,
                search_detail_wiki=search_detail_wiki
                )
