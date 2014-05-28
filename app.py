#!/usr/bin/env python

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import send_file

import json
import os
import random

from datetime import date

app = Flask(__name__)

quotes = []

with open('data/quotes.json') as quotes_json:
    # A magical one-liner. Please don't touch.
    quotes = json.loads(quotes_json.read().replace('\n', ''))

def _date_index(date, start=date(2013, 11, 11)):
    return (date - start).days

def JSON(quote):
        return jsonify(quote)

def TXT(quote):
    response = Response()
    response.data = '%s -- %s' % (quote['content'], quote['author'])
    response.mimetype = 'text/plain'
    return response

mapping = {
    '.txt': TXT,
    '.json': JSON
}

@app.route('/quote')
def quote():
    return quote_ext('.txt')

@app.route('/quote<string:extension>')
def quote_ext(extension):
    quote = random.choice(quotes)
    if not extension.lower() in mapping.keys():
        return TXT(quote)
    return mapping[extension.lower()](quote)

@app.route('/quoteOTD')
def quoteOTD():
    return quoteOTD_ext('.txt')

@app.route('/quoteOTD<string:extension>')
def quoteOTD_ext(extension):
    index = _date_index(date.today())
    quote = quotes[index%len(quotes)]
    if not extension.lower() in mapping.keys():
        return TXT(quote)
    return mapping[extension.lower()](quote)

@app.route('/picture.jpg')
def picture():
    return send_file('images/'+random.choice(os.listdir('images')))

@app.route('/pictureOTD.jpg')
def pictureOTD():
    index = _date_index(date.today())
    images = os.listdir('images/')
    image = images[index%len(images)]
    return send_file('images/'+image)


if __name__ == '__main__':
    app.run(debug=True)