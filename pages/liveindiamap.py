import json
from urllib.request import urlopen

# from bs4 import BeautifulSoup
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

from app import app

token = open("/var/www/coronaApp/liveapp/pages/.mapbox_token").read()


def return_df(url, pos):
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    dfs = pd.DataFrame(df_list, dtype=str)
    return dfs


url = "https://www.mohfw.gov.in/"
df_india = return_df(url, 0)

df_india.columns = ["S. No.", "State", "Confirmed", "Recovered", "Deaths"]


df_india = df_india[:-1]

df_india["Confirmed"] = df_india["Confirmed"].astype(float)
df_india["Recovered"] = df_india["Recovered"].astype(float)
df_india["Deaths"] = df_india["Deaths"].astype(float)

df_india = df_india.set_index("S. No.", inplace=False)

with urlopen(
    "https://raw.githubusercontent.com/theajit/track-corona-live/master/assets/india.json"
) as response:
    states = json.load(response)

color5 = "#FF0000"
color4 = "#F5B78A"
color3 = "#F3A671"
color2 = "#FCEBDE"
color1 = "#ffe8d6"

colormap = [
    [0.0, color1],
    [0.20, color2],
    [0.40, color3],
    [0.65, color4],
    [1.0, color5],
]


layout = html.Div(
    [
        html.Div(
            [html.H2("India Live Map")],
            style={"textAlign": "center", "padding-bottom": "30"},
        ),
        html.Div(
            [
                html.Span(
                    "Different cases to display : ",
                    className="six columns",
                    style={"text-align": "right", "width": "40%", "padding-top": 10},
                ),
                dcc.Dropdown(
                    id="state-selected",
                    value="Confirmed",
                    options=[
                        {"label": "Confirmed", "value": "Confirmed"},
                        {"label": "Deaths ", "value": "Deaths"},
                        {"label": "Recovered ", "value": "Recovered"},
                    ],
                    style={
                        "display": "block",
                        "margin-left": "auto",
                        "margin-right": "auto",
                        "width": "70%",
                    },
                    className="six columns",
                ),
            ],
            className="row",
        ),
        dcc.Graph(id="india-live-map", config={"responsive": True}),
    ],
    className="container",
)


@app.callback(
    dash.dependencies.Output("india-live-map", "figure"),
    [dash.dependencies.Input("state-selected", "value")],
)
def update_figure(selected):
    dff = (
        df_india.groupby(["State", "Confirmed", "Recovered", "Deaths"])
        .max()
        .reset_index()
    )

    def title(text):
        if text == "Confirmed":
            return "Confirmed Cases"
        elif text == "Deaths":
            return "Deaths Cases"
        elif text == "Recovered":
            return "Recovered Cases"
        else:
            return "Recovered"

    trace = go.Choroplethmapbox(
        geojson=states,
        featureidkey="properties.State",
        locations=dff.State,
        z=dff[selected],
        colorscale=colormap,
        marker_line_width=1,
    )
    return {
        "data": [trace],
        "layout": go.Layout(
            mapbox_style="mapbox://styles/cocktailsguy/ck8edouiv02lv1io9quvrr36i",
            mapbox_accesstoken=token,
            mapbox_zoom=3.1,
            mapbox_center={"lat": 21, "lon": 78},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
        ),
    }
