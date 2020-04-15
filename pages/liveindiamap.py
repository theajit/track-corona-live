import json
from urllib.request import urlopen
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from apscheduler.schedulers.background import BackgroundScheduler


from app import app
from .functions import indiadata

token = open("/var/www/coronaApp/liveapp/pages/.mapbox_token").read()

india_url = "https://www.mohfw.gov.in/"
india_pos = 0
india_strip = 3


def india_map_sensor():
    print("India Map Page Sensor Working!")
    return indiadata.return_india_map_df(india_url, india_pos, india_strip)


sched = BackgroundScheduler(daemon=True)
sched.add_job(india_map_sensor, "interval", minutes=92)
sched.start()

df_india = india_map_sensor()

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
