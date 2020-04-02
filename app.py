from refresh import update
from pages import (
    countrycasesgrowth,
    countryratechanges,
    credits,
    home,
    indiahelpline,
    indiatable,
    livecoronamap,
    livecoronatable,
    liveindiamap,
    liveusamap,
    liveusatable,
)
import datetime as dt
import json
import uuid

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
from apscheduler.schedulers.background import BackgroundScheduler
from dash.dependencies import Input, Output

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, routes_pathname_prefix="/data/")

app.config.suppress_callback_exceptions = True

app.server.secret_key = str(uuid.uuid4())


external_stylesheets = ["https://codepen.io/theajit/pen/vYYxVLb.css"]

# external JavaScript files
external_scripts = [
    "https://codepen.io/theajit/pen/JjdLvZE.js",
]

app.title = "Track Corona Online Live | India | USA | China"

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Title("Live Corona Track Online"),
        html.Br(),
        html.Div(
            [
                html.Ul(
                    [
                        html.Li([dcc.Link("Home ", href="/")]),
                        html.Li(
                            [
                                dcc.Link("India", href="#"),
                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "India Table ",
                                                    href="/data/live-india-table",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "India Map ",
                                                    href="/data/live-india-map",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                html.A(
                                                    "India helpline ",
                                                    href="/data/india-helpline",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="submenu",
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                dcc.Link("Live Table ", href="#"),
                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "India Table ",
                                                    href="/data/live-india-table",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "World Table ",
                                                    href="/data/live-corona-world-table",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "USA Table ",
                                                    href="/data/live-corona-usa-table",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="submenu",
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                dcc.Link("Live Map ", href="#"),
                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "World Map ",
                                                    href="/data/live-corona-world-map",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "India Map ",
                                                    href="/data/live-india-map",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "USA Map ",
                                                    href="/data/live-corona-usa-map",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="submenu",
                                ),
                            ]
                        ),
                        html.Li(
                            [
                                dcc.Link("Case Analysis ", href="#"),
                                html.Ul(
                                    [
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "Total Confirmed Cases",
                                                    href="/data/live-total-cases-growth",
                                                )
                                            ]
                                        ),
                                        html.Li(
                                            [
                                                dcc.Link(
                                                    "Day wise Confirmed Cases",
                                                    href="/data/live-cases-per-day",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="submenu",
                                ),
                            ]
                        ),
                        html.Li([html.A("Contributors", href="/data/credits")]),
                    ]
                )
            ],
            style={"textAlign": "center"},
            className="row dropdownmenu gs-header",
        ),
        # Included sniper as per suggestion
        html.Div(dash_table.DataTable(), style={"display": "none"}),
        html.Div(id="page-content"),
        html.P(
            [
                u"\u00A9"
                " Copyright 2020, Trackcorona.online | Data Sources: WHO and JHU"
            ],
            style={"textAlign": "center"},
            className="twelve columns",
        ),
        html.Div(
            [
                html.Div(
                    id="live-update-text",
                    style={"font-size": "10px", "textAlign": "center"},
                ),
                dcc.Interval(
                    id="interval-component",
                    interval=20000 * 1000,  # in milliseconds
                    n_intervals=0,
                ),
            ],
            className="twelve columns",
        ),
    ]
)

now = dt.datetime.now()
formated_date = now.strftime("%d/%m/%Y, %H:%M:%S")


@app.callback(
    Output("live-update-text", "children"), [Input("interval-component", "n_intervals")]
)
def update_date(n):
    return [html.P("Last updated " + str(formated_date))]


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return home.layout
    elif pathname == "/data/live-corona-world-map":
        return livecoronamap.layout
    elif pathname == "/data/live-corona-world-table":
        return livecoronatable.layout
    elif pathname == "/data/india-helpline":
        return indiahelpline.layout
    elif pathname == "/data/live-corona-usa-map":
        return liveusamap.layout
    elif pathname == "/data/live-corona-usa-table":
        return liveusatable.layout
    elif pathname == "/data/live-india-table":
        return indiatable.layout
    elif pathname == "/data/live-total-cases-growth":
        return countrycasesgrowth.layout
    elif pathname == "/data/live-cases-per-day":
        return countryratechanges.layout
    elif pathname == "/data/live-india-map":
        return liveindiamap.layout
    elif pathname == "/data/credits":
        return credits.layout
    else:
        return home.layout


@server.route("/")
def index():
    return flask.redirect(flask.url_for("/data/"))


@server.route("/live-corona-world-table/")
def redirect_table():
    return flask.redirect(flask.url_for("/data/"))


@server.route("/live-corona-world-map/")
def redirect_map():
    return flask.redirect(flask.url_for("/data/"))


def sensor():
    update()
    print("Scheduler is alive!")


sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor, "interval", minutes=120)
sched.start()

data_url = "/var/www/coronaApp/api/data.json"


@server.route("/api/all")
def api_index():
    with open(data_url) as f:
        d = json.load(f)
    return d


@server.route("/api/confirmed")
def confirmed():
    with open(data_url) as f:
        d = json.load(f)
    return d["confirmed"]


@server.route("/api/deaths")
def deaths():
    with open(data_url) as f:
        d = json.load(f)
    return d["deaths"]


@server.route("/api/recovered")
def recovered():
    with open(data_url) as f:
        d = json.load(f)
    return d["recovered"]


@server.route("/api/latest")
def latest():
    with open(data_url) as f:
        d = json.load(f)
    return d["latest"]


if __name__ == "__main__":
    app.run_server(debug=True)
