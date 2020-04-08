import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import country_converter as coco
import numpy as np

from app import app

us_state_abbrev = {
    "American Samoa": "AS",
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Palau": "PW",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

usa_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?gid=1902046093&single=true&widget=true&headers=false"

df_list = pd.read_html(usa_url)[0]

df = pd.DataFrame(df_list)
df = df.drop(
    columns=[
        "Unnamed: 0",
        "Unnamed: 6",
        "Unnamed: 9",
        "Unnamed: 10",
        "Unnamed: 11",
        "Unnamed: 12",
        "Unnamed: 13",
        # "Unnamed: 14",
        # "Unnamed: 15",
        # "Unnamed: 16",
        # "Unnamed: 17",
        # "Unnamed: 18",
        # "Unnamed: 19",
        # "Unnamed: 20"
    ]
)

df_states = df.loc[5:, :]
df_states.columns = [
    "United_States",
    "Confirmed",
    "New Confirmed",
    "Deaths",
    "New Deaths",
    "Serious & Critical",
    "Recovered",
]
df_states = df_states[:-3]

df_states["iso_alpha"] = df_states["United_States"].apply(
    lambda x: coco.convert(names=x, src="regex", to="ISO2", not_found=None)
)

labels = df_states["United_States"].unique()
df_states = df_states.replace({"iso_alpha": us_state_abbrev})

df_states = df_states.replace(to_replace=np.nan, value=0)


layout = html.Div(
    [
        html.Div(
            [html.H2("USA Live Corona Cases")],
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
                    id="value-selected",
                    value="Confirmed",
                    options=[
                        {"label": "Confirmed Cases ", "value": "Confirmed"},
                        {"label": "Deaths ", "value": "Deaths"},
                        {"label": "Serious ", "value": "Serious & Critical"},
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
        dcc.Graph(id="usa-live-graph", config={"responsive": True}),
    ],
    className="container",
)
color5 = "#FF0000"
color4 = "#F5B78A"
color3 = "#F3A671"
color2 = "#FCEBDE"
color1 = "#ffe8d6"

colormap = [
    [0.0, color1],
    [0.05, color2],
    [0.45, color3],
    [0.65, color4],
    [1.0, color5],
]


@app.callback(
    dash.dependencies.Output("usa-live-graph", "figure"),
    [dash.dependencies.Input("value-selected", "value")],
)
def update_figure(selected):
    dff = (
        df_states.groupby(
            [
                "iso_alpha",
                "United_States",
                "Confirmed",
                "Deaths",
                "Serious & Critical",
                "Recovered",
            ]
        )
        .max()
        .reset_index()
    )

    def title(text):
        if text == "Confirmed":
            return "Confirmed Cases"
        elif text == "Deaths":
            return "Deaths Cases"
        elif text == "Critical" or "Serious":
            return "Critical/Serious Cases"
        else:
            return "Recovered"

    trace = go.Choropleth(
        locations=dff["iso_alpha"],
        z=dff[selected],
        text=dff["United_States"],
        autocolorscale=False,
        locationmode="USA-states",
        colorscale=colormap,
        marker={"line": {"color": "rgb(180,180,180)", "width": 1.5}},
        colorbar={
            "thickness": 10,
            "len": 0.3,
            "x": 0.9,
            "y": 0.7,
            "title": {"text": title(selected), "side": "bottom"},
            "titleside": "top",
            "ticks": "outside",
        },
    )
    return {
        "data": [trace],
        "layout": go.Layout(
            title=title(selected),
            height=800,
            geo={
                "scope": "usa",
                "showframe": False,
                "showcoastlines": True,
                "coastlinecolor": "RebeccaPurple",
                "projection": {"type": "albers usa"},
            },
        ),
    }
