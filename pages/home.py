from app import app
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import json
from urllib.request import urlopen
import dash_daq as daq
from dash.dependencies import Input, Output


token = open("/var/www/coronaApp/liveapp/pages/.mapbox_token").read()


url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)
# print (df)

# df_final = df.drop(columns=["Unnamed: 0","Unnamed: 7","Unnamed: 8"])
# df_final = df.drop(columns=["Unnamed: 0","Unnamed: 7"])
df_final = df.drop(
    columns=[
        "Unnamed: 0",
        "Unnamed: 3",
        "Unnamed: 5",
        "Unnamed: 6",
        "Unnamed: 9",
        "Unnamed: 10",
        "Unnamed: 11",
        "Unnamed: 12",
        "Unnamed: 13",
        "Unnamed: 14",
        "Unnamed: 15",
        "Unnamed: 16",
    ]
)
df_final.columns = ["Country", "Confirmed", "Deaths", "Serious & Critical", "Recovered"]
# df_final.columns = ['Country', 'Confirmed', 'Deaths','Serious','Critical','Recovered']

df_country = df_final.set_index("Country", inplace=False)
df_country = df_country.iloc[7:]


df_total = df_country.iloc[[-2]]
# df_total = df_total.replace(np.nan, value =0)
df_total = df_total.replace("-", 0, regex=True)
df_total = df_total.fillna(0)


df_total["Confirmed"] = df_total["Confirmed"].astype(int)
df_total["Deaths"] = df_total["Deaths"].astype(int)
df_total["Serious & Critical"] = df_total["Serious & Critical"].astype(int)
df_total["Recovered"] = df_total["Recovered"].astype(int)

df_country = df_country[:-2]

confirmed = df_total["Confirmed"].values[0]
deaths = df_total["Deaths"].values[0]
serious = df_total["Serious & Critical"].values[0]
recovered = df_total["Recovered"].values[0]

pie_labels = ["Confirmed", "Deaths", "Serious & Critical", "Recovered"]
pie_values = [confirmed, deaths, serious, recovered]

# total = df_total['Confirmed']+df_total['Deaths']+df_total['Serious']+df_total['Critical']+df_total['Recovered']

fig = go.Figure(
    data=[go.Pie(labels=pie_labels, values=pie_values, pull=[0.3, 0, 0, 0])]
)
fig.update_traces(hole=0, hoverinfo="label+percent")

fig.update_layout(
    title_text="The World Corona Pie",
    # Add annotations in the center of the donut pies.
    # annotations=[dict(text='Corona', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# World Map
world_color1 = "#ffe8d6"
world_color2 = "#FCEBDE"
world_color3 = "#F3A671"
world_color4 = "#F5B78A"
world_color5 = "#FF0000"


world_colormap = [
    [0.0, world_color1],
    [0.20, world_color2],
    [0.40, world_color3],
    [0.65, world_color4],
    [1.0, world_color5],
]

world_trace = go.Choropleth(
    locations=df_country.index,
    locationmode='country names',
    z=df_country["Confirmed"],
    text=df_country.index,
    autocolorscale=False,
    colorscale=world_colormap,
    reversescale=False,
    marker={"line": {"color": "rgb(180,180,180)", "width": 1.5}},
    colorbar={
        "thickness": 10,
        "len": 0.3,
        "x": 0.9,
        "y": 0.7,
        "title": {"side": "bottom"},
        "titleside": "top",
        "ticks": "outside",
    },
)

world_layout = go.Layout(
    geo={
        "showframe": False,
        "showcoastlines": True,
        "showlakes": False,
        "coastlinecolor": "RebeccaPurple",
        "showland": True,
        "landcolor": "White",
        "showocean": True,
        "oceancolor": "#72e7f3",
        "showcountries": True,
        "countrycolor": "RebeccaPurple",
        "projection": {"type": "orthographic"},
    },
)
world_fig = go.Figure(data=[world_trace], layout=world_layout)

# India Confirmed Map on Home Page


def return_df(url, pos):
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[pos]
    dfs = pd.DataFrame(df_list, dtype=str)
    return dfs


url = "https://www.mohfw.gov.in/"
df_india = return_df(url, 0)

df_india.columns = ["S. No.", "State", "Confirmed", "Recovered", "Deaths"]

df_india_total = df_india.iloc[[-1]]
df_india = df_india[:-1]
df_india["Confirmed"] = df_india["Confirmed"].astype(float)
df_india["Deaths"] = df_india["Deaths"].astype(float)
df_india["Recovered"] = df_india["Recovered"].astype(float)

df_india = df_india.set_index("S. No.", inplace=False)

india_confirmed = df_india_total["Confirmed"].values[0]
india_deaths = df_india_total["Deaths"].values[0]
india_recovered = df_india_total["Recovered"].values[0]

india_pie_labels = ["Confirmed", "Deaths", "Recovered"]
india_pie_values = [india_confirmed, india_deaths, india_recovered]

india_pie = go.Figure(
    data=[go.Pie(labels=india_pie_labels, values=india_pie_values, pull=[0.3, 0, 0, 0])]
)
india_pie.update_traces(hole=0, hoverinfo="label+percent")

india_pie.update_layout(
    title_text="The India Corona Pie",
    # Add annotations in the center of the donut pies.
    # annotations=[dict(text='Corona', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

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

india_fig = go.Figure(
    go.Choroplethmapbox(
        geojson=states,
        featureidkey="properties.State",
        locations=df_india.State,
        z=df_india["Confirmed"],
        colorscale=colormap,
        marker_line_width=1,
    )
)
india_fig.update_layout(
    mapbox_style="mapbox://styles/cocktailsguy/ck8edouiv02lv1io9quvrr36i",
    mapbox_accesstoken=token,
    mapbox_zoom=3.1,
    mapbox_center={"lat": 21, "lon": 78},
)
india_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


layout = html.Div(
    [
        dcc.Tabs(
            id="home-tabs-with-classes",
            value="world",
            parent_className="home-custom-tabs",
            className="custom-tabs-container",
            children=[
                dcc.Tab(
                    label="World",
                    value="world",
                    className="home-custom-tab",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="India",
                    value="india",
                    className="home-custom-tab",
                    selected_className="custom-tab--selected",
                ),
            ],
        ),
        html.Div(id="home-tabs-content"),
    ],
    style={"textAlign": "center"},
    className="row tweleve columns",
)


@app.callback(
    Output("home-tabs-content", "children"), [Input("home-tabs-with-classes", "value")]
)
def render_content(tab):
    if tab == "world":
        return html.Div(
            [
                html.Div([
                    html.Div(
                        [daq.LEDDisplay(
                            label="Confirmed",
                            value=confirmed,
                            color="#a5c9fd",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row three columns",
                    ),
                    html.Div(
                        [daq.LEDDisplay(
                            label="Deaths",
                            value=deaths,
                            color="#ff8582",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row three columns",
                    ),
                    html.Div(
                        [daq.LEDDisplay(
                            label="Serious",
                            value=serious,
                            color="#f5ce67",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row three columns",
                    ),
                    html.Div(
                        [daq.LEDDisplay(
                            label="Recovered",
                            value=recovered,
                            color="#9ae69c",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row three columns",
                    )
                ], className="row twelve columns"),
                html.Div([
                    html.Div(
                        [dcc.Graph(id="world-map", figure=world_fig, config={"responsive": True, 'displayModeBar': False})],
                        style={"textAlign": "center"},
                        className="row six columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="pie-chart", figure=fig, config={"responsive": True, 'displayModeBar': False})],
                        style={"textAlign": "center"},
                        className="row six columns",
                    ),
                ], className="row twelve columns")
            ]
        )
    elif tab == "india":
        return html.Div(
            [
                html.Br(),
                html.Div([
                    html.Div(
                        [daq.LEDDisplay(
                            label="Confirmed",
                            value=india_confirmed,
                            color="#a5c9fd",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row four columns",
                    ),
                    html.Div(
                        [daq.LEDDisplay(
                            label="Deaths",
                            value=india_deaths,
                            color="#ff8582",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row four columns",
                    ),
                    html.Div(
                        [daq.LEDDisplay(
                            label="Recovered",
                            value=india_recovered,
                            color="#9ae69c",
                            backgroundColor="#445175"
                        )],
                        style={"textAlign": "center"},
                        className="row four columns",
                    )
                ], className="row twelve columns"),
                html.Div([
                    html.Div(
                        [
                            dcc.Graph(
                                id="india-map", figure=india_fig, config={"responsive": True, 'displayModeBar': False}
                            )
                        ],
                        style={"textAlign": "center"},
                        className="row six columns",
                    ),
                    html.Div(
                        [dcc.Graph(id="india-pie-chart", figure=india_pie, config={"responsive": True, 'displayModeBar': False})],
                        style={"textAlign": "center"},
                        className="row six columns",
                    ),
                ], className="row twelve columns"),

                html.Br(),
            ]
        )
