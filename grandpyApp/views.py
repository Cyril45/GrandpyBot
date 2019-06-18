
#! /usr/bin/env python
# coding: utf-8

from flask import Flask, request, render_template

app = Flask(__name__)
# app.config.from_object('config')

@app.route('/')
@app.route('/index/')
def index():
    return render_template('index.html')
