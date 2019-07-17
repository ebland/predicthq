from collections import OrderedDict

import os
import csv
import sys
import dash
import predicthq
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

# from config import MAPBOX_ACCESS_TOKEN, MAPBOX_STYLE_URL, ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET

#plotly output css that links our predicthq "data exporter" csv data to mapbox
MAPBOX_ACCESS_TOKEN = 'pk.eyJ1IjoiZWxpemFiZXRoYmxhbmQiLCJhIjoiY2p5M3lxcG5wMDBhbTNobWt6cWo2NHBlNCJ9.vQVHhQNS7bUalBDv8u_iXw'
MAPBOX_STYLE_URL = "mapbox://styles/elizabethbland/cjy3z4qkc357y1cp96obggltm"
predicthq="predicthq-0.2.0-py2.py3-none-any.whl"

df = pd.read_csv(r'predicthq.csv')
df.drop_duplicates(inplace=True)

gt_90 = df['rank'] >= 90
gt_80 = (df['rank'] >= 80) & (df['rank'] < 90)
gt_70 = (df['rank'] >= 70) & (df['rank'] < 80)
gt_60 = (df['rank'] >= 60) & (df['rank'] < 70)

df['marker_size'] = 10

df.loc[gt_90, 'marker_size'] = 60
df.loc[gt_80, 'marker_size'] = 30
df.loc[gt_70, 'marker_size'] = 10
df.loc[gt_60, 'marker_size'] = 5

# Create an ordered dictionary of sorted labels mapped to respective DataFrame
label_df_map = OrderedDict()
for lbl in sorted(set(df.label.values)):
    label_df_map[lbl] = df.loc[df.label == lbl]

data = []
for lbl, ndf in label_df_map.items():
    data.append(
        go.Scattermapbox(
            lat=ndf.lat,
            lon=ndf.lon,
            mode='markers',
            textposition='middle left',
            marker=dict(
                size=ndf.marker_size,
                cauto=True,
                opacity=0.7,
                cmin=5,
                cmax=90,
                sizemin=6,
                sizeref=0.1,
                symbol='circle',
                sizemode='area',
                showscale=True,
                autocolorscale=False,
                color=ndf['rank'],
                colorscale=[
                    [0, 'rgb(5, 10, 172)'],
                    [0.35, 'rgb(106,137,247)'],
                    [0.5, 'rgb(190,190,190)'],
                    [0.6, 'rgb(220,170,132)'],
                    [0.7, 'rgb(230,145,90)'],
                    [1, 'rgb(178,10,28)']
                ],
                colorbar=dict(
                    lenmode='fraction',
                    title='Severity',
                    ticks='inside',
                    titlefont=dict(
                        family='Roboto, Open Sans, Sans Serif',
                        size=16,
                        color='#f2f5fa'
                    ),
                    tickfont=dict(
                        family='Roboto, Open Sans, Sans Serif',
                        size=16,
                        color='#f2f5fa'
                    ),
                    tickmode='auto',
                    nticks=0,
                    titleside='top',
                    outlinecolor='rgb(0,0,0)',
                    thickness=15,
                    thicknessmode='pixels',
                    showticklabels=True,
                    showexponent='all',
                    exponentformat='B',
                    bordercolor='#444',
                    bgcolor='rgba(0,0,0,0)',
                    outlinewidth=1,
                    ticklen=15,
                    len=1,
                    x=0.97,
                    y=0.4800000000000004,
                    xpad=10,
                    ypad=48,
                    xanchor='center',
                    yanchor='middle',
                    tickwidth=1,
                    dtick=10,
                )
            ),
            text=ndf.title,
            name=lbl
        )
    )

layout = go.Layout(
    paper_bgcolor='rgb(0, 0, 0)',
    title="All Events Involving Threats Mapped Using Data from Predict HQ",
    autosize=True,
    height=800,
    hovermode='closest',
    dragmode='turntable',
    showlegend=True,
    mapbox=dict(
        accesstoken=MAPBOX_ACCESS_TOKEN,
        bearing=0,
        center=dict(
            lat=45,
            lon=-73
        ),
        pitch=0,
        zoom=5,
        style=MAPBOX_STYLE_URL,
    ),
)

external_stylesheets = ['https://predicthqeblandtestcss--elizabethbland.repl.co']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='EBland Interview Research API', style={'color': '#35a700',
                                                    'fontSize': 30,
                                                    'textAlign': 'center',
                                                    'family': 'Open Sans'}),

    html.Div(children='''
        Experimenting with API PredicHQ data mapping events
    ''', style={'color': '#35a700', 'fontSize': 15, 'textAlign': 'center'}),

    dcc.Graph(
        id='map-graph',
        figure={
            'data': data,
            'layout': layout,
        }
    ),
    html.Div([
        html.Pre(id='restyle-data')])
])

if __name__ == '__main__':
    app.run_server(debug=True)