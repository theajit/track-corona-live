import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import base64
import pandas as pd
import dash
import plotly.graph_objs as go
import dash_daq as daq
import numpy as np
import requests
import io
import lxml.html as lh
import json
from urllib.request import urlopen

token = open("/var/www/coronaApp/liveapp/pages/.mapbox_token").read()

from app import app

url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)
#print (df)

#df_final = df.drop(columns=["Unnamed: 0","Unnamed: 7","Unnamed: 8"])
#df_final = df.drop(columns=["Unnamed: 0","Unnamed: 7"])
df_final = df.drop(columns=["Unnamed: 0","Unnamed: 9","Unnamed: 10","Unnamed: 11", "Unnamed: 12", "Unnamed: 13","Unnamed: 14", "Unnamed: 15", "Unnamed: 16"])
df_final.columns = ['Country', 'Confirmed','New Confirmed','Deaths', 'New Deaths','Percentage of Deaths','Serious & Critical','Recovered']
#df_final.columns = ['Country', 'Confirmed', 'Deaths','Serious','Critical','Recovered']

df_country = df_final.iloc[6:]

df_country = df_country.set_index("Country", inplace = False) 

df_total = df_country.iloc[[-2]]

#df_total = df_total.replace(np.nan, value =0) 
df_total = df_total.replace('-',0, regex=True)
df_total = df_total.fillna(0)


df_total['Confirmed'] = df_total['Confirmed'].astype(int)
df_total['Deaths'] = df_total['Deaths'].astype(int)
df_total['Serious & Critical'] = df_total['Serious & Critical'].astype(int)
df_total['Recovered'] = df_total['Recovered'].astype(int)


confirmed = df_total['Confirmed'].values[0]
deaths = df_total['Deaths'].values[0]
serious = df_total['Serious & Critical'].values[0]
recovered = df_total['Recovered'].values[0]

pie_labels = ['Confirmed', 'Deaths','Serious & Critical','Recovered']
pie_values = [confirmed,deaths,serious,recovered]

#total = df_total['Confirmed']+df_total['Deaths']+df_total['Serious']+df_total['Critical']+df_total['Recovered']

fig = go.Figure(data=[go.Pie(labels=pie_labels, values=pie_values,pull=[0.3, 0, 0, 0])])  
fig.update_traces(hole=0, hoverinfo="label+percent")

fig.update_layout(
    title_text="The Corona Pie",
    # Add annotations in the center of the donut pies.
    #annotations=[dict(text='Corona', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

#India Confirmed Map on Home Page

def return_df(url,pos):
    #Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    dfs = pd.DataFrame(df_list,dtype=str)
    return dfs

url = 'https://www.mohfw.gov.in/'
df_india = return_df(url,9)

df_india.columns = ['S. No.','State', 'Confirmed','Recovered','Deaths']


df_india = df_india[:-2]
df_india['Confirmed'] = df_india['Confirmed'].astype(float)
df_india['Deaths'] = df_india['Deaths'].astype(float)
df_india = df_india.set_index("S. No.", inplace = False)

with urlopen('https://raw.githubusercontent.com/theajit/track-corona-live/master/assets/india.json') as response:
    states = json.load(response)

color5 = '#FF0000'
color4 = '#F5B78A'
color3 = '#F3A671'
color2 = '#FCEBDE'
color1 = '#ffe8d6'

colormap = [[0.0, color1], [0.20, color2], [0.40, color3],
        [0.65, color4], [1.0, color5]]

india_fig = go.Figure(go.Choroplethmapbox(geojson=states, featureidkey= "properties.State",locations=df_india.State, z=df_india['Confirmed'],
                                    colorscale=colormap, marker_line_width=1))
india_fig.update_layout(mapbox_style='mapbox://styles/cocktailsguy/ck8edouiv02lv1io9quvrr36i', mapbox_accesstoken=token,
                  mapbox_zoom=3.1, mapbox_center = {"lat": 21, "lon": 78})
india_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


layout = html.Div([
            html.Div([
                 dcc.Graph(id='pie-chart',figure=fig,config= {'responsive': True})
            ],style={'textAlign': 'center'}, className="row six columns"),
            html.Div([
                 dcc.Graph(id='india-chart',figure=india_fig,config= {'responsive': True})
            ],style={'textAlign': 'center'}, className="row six columns"),
            html.Br()
        ], style={'textAlign': 'center'}, className="row tweleve columns")
