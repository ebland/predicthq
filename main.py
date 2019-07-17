from predicthq import Client
from collections import OrderedDict
# from client import Client
import client
import config
import requests
import urllib
import csv
import json
import argparse
import app
import pandas
import pandas as pd
import predicthq
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

# from config import MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE_URL, ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET

application = "ebland_predicthq_interview_research"
description = "Interview_Research_Learning_API"
CLIENT_ID = "phq.1Z1h0t0oJTkiMFepPrShLd1VpFoI2UTpkpPZ3oZ4"
CLIENT_SECRET = "VkO78PNWtMVYyXRbriX5GgpqMDYDvnzXZA6m2iKk"
ACCESS_TOKEN = "oxBn3ImPUNkyqpNkukXF4vFQwTDFQD"
endpoint_url = "https://api.predicthq.com"
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZWxpemFiZXRoYmxhbmQiLCJhIjoiY2p5M3lxcG5wMDBhbTNobWt6cWo2NHBlNCJ9.vQVHhQNS7bUalBDv8u_iXw'
MAPBOX_STYLE_URL = "mapbox://styles/elizabethbland/cjy3z4qkc357y1cp96obggltm"
predicthq="predicthq-0.2.0-py2.py3-none-any.whl"


offset = 0
results = []
# search_id='xryjn0ZQzzaDa'

__author__ = 'ebland'
 
df = pd.read_csv(r'predicthq.csv')
df.drop_duplicates(inplace=True)

phq = Client(access_token='oxBn3ImPUNkyqpNkukXF4vFQwTDFQD')

response = requests.get(
    url='https://api.predicthq.com/v1/events/',
    headers={
      'Authorization': 'Bearer oxBn3ImPUNkyqpNkukXF4vFQwTDFQD',
      'Accept': 'application/json'
    },
    params={
        'id': 'xryjn0ZQzzaDa'
    }
)
print(response.json())

for event in phq.events.search(q='storm', rank_level=[1, 2, 3, 4, 5], country='US'):
    print(event.labels, event.id, event.category, event.country, event.description, event.rank, event.start, event.timezone, event.title, event.location, event.start.strftime('%Y-%m-%d'), event.first_seen)

data = pd.read_csv('predicthq.csv')
data.head()
data=data.rename(columns={'id': 'id',
             'event_title': 'title',
             'category': 'category',
             'country': 'country',
             'description': 'description',
             'title': 'title',
             'latitude': 'lat',
             'longitude': 'lon',
             'offset': 'offset',
             'venue_formatted_address': 'rank',
             'start': 'start',
             'end': 'end',
             'duration': 'duration',            
             'labels': 'labels',
             'timezone': 'timezone',
             'location': 'location',
             'scope': 'scope',
             'rank': 'rank',
             'state': 'state'})

data.to_csv('predicthq.csv')
 