import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import country_converter as coco
import numpy as np

from app import app


url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)
df.set_index('Unnamed: 0', inplace=True)


df_final = df.drop(columns=["Unnamed: 7","Unnamed: 8"])

df_total = df_final.loc[3:4, :]

df_country = df_final.loc[7:, :]
df_country.columns = ['Country', 'Confirmed', 'Deaths','Serious','Critical','Recovered']

df_country[df_country.Country != 'Diamond Princess']
df_country.Country.replace(to_replace ="Diamond Princess", 
                 value ="Japan") 

df_country = df_country[:-2]

df_country['iso_alpha'] = df_country['Country'].apply(lambda x: coco.convert(names=x, src='regex', to='ISO3', not_found = None))



df_country.replace(to_replace = np.nan, value =0) 



layout = html.Div([html.Div([html.H2("Live Corona Map")],
                                style={'textAlign': "center", "padding-bottom": "30"}),
                       html.Div([html.Span("Different cases to display : ", className="six columns",
                                           style={"text-align": "right", "width": "40%", "padding-top": 10}),
                                 dcc.Dropdown(id="value-selected", value='Confirmed',
                                              options=[{'label': "Confirmed Cases ", 'value': 'Confirmed'},
                                                       {'label': "Deaths ", 'value': 'Deaths'},
                                                       {'label': "Serious ", 'value': 'Serious'},
                                                       {'label': "Critical ", 'value': 'Critical'},
                                                       {'label': "Recovered ", 'value': 'Recovered'}],
                                              style={"display": "block", "margin-left": "auto", "margin-right": "auto",
                                                     "width": "70%"},
                                              className="six columns")], className="row"),
                       dcc.Graph(id="my-graph")
                       ], className="container")
color1 = 'rgb(91, 192, 235)'
color2 = 'rgb(253, 231, 76)'
color3 = 'rgb(155, 197, 61)'
color4 = 'rgb(229, 89, 52)'
color5 = 'rgb(250, 121, 33)'

colormap = [[0.0, color1], [0.25, color2], [0.50, color3],
        [0.75, color4], [1.0, color5]]
        
@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")]
)

def update_figure(selected):
    dff = df_country.groupby(['iso_alpha','Country','Confirmed', 'Deaths','Serious','Critical','Recovered']).max().reset_index()
    def title(text):
        if text == "Confirmed":
            return "Confirmed Cases"
        elif text == "Deaths":
            return "Deaths Cases"
        elif text == "Critical" or "Serious":
            return "Critical/Serious Cases"
        else:
            return "Recovered"
    trace = go.Choropleth(locations=dff['iso_alpha'],z=dff[selected],text=dff['Country'],autocolorscale=False,
                          colorscale=colormap,marker={'line': {'color': 'rgb(180,180,180)','width': 1.5}},
                          colorbar={"thickness": 10,"len": 0.3,"x": 0.9,"y": 0.7,
                                    'title': {"text": title(selected), "side": "bottom"},
                                    'titleside' : 'top',
                                    'ticks' : 'outside'})
    return {"data": [trace],
            "layout": go.Layout(title=title(selected),height=800,geo={'showframe': False,
                                                                    'showcoastlines': True, 'coastlinecolor':"RebeccaPurple",
                                                                    'showland':True, 'landcolor': "White",
                                                                    'showocean': True, 'oceancolor'  : "LightBlue",
                                                                    'showcountries' :True, 'countrycolor' :"RebeccaPurple",
                                                                    'projection': {'type': "miller"}})}
