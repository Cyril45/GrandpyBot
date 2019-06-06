#! /usr/bin/env python
# coding: utf-8


import requests

S = requests.Session()

URL = "https://fr.wikipedia.org/w/api.php"

SEARCHPAGE = "OpenClassrooms"

PARAMS = {
    'action':"query",
    'list':"search",
    'srsearch': SEARCHPAGE,
    'format':"json"
}

R = S.get(url=URL, params=PARAMS)
DATA = R.json()

result = DATA['query']['search'][0]

for x in result:
    print(x,":", result[x])
