import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from apscheduler.schedulers.background import BackgroundScheduler

from app import app
from .functions import indiadata

india_url = "https://www.mohfw.gov.in/"
india_pos = 0
india_strip = 2


def india_sensor():
    print("India Table Page Sensor Working!")
    return indiadata.return_india_table_df(india_url, india_pos, india_strip)


df_india = india_sensor()

sched = BackgroundScheduler(daemon=True)
sched.add_job(india_sensor, "interval", minutes=90)
sched.start()

layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": i, "value": i} for i in df_india["State/UT"].unique()],
            multi=True,
            placeholder="Search by Indian States ...",
        ),
        dash_table.DataTable(
            id="india_state_table",
            columns=[{"name": i, "id": i} for i in df_india.columns],
            data=df_india.to_dict("records"),
            page_action="native",
            page_current=0,
            page_size=30,
            sort_action="native",
            style_cell={
                "backgroundColor": "#445175",
                "fontWeight": "bold",
                "color": "white",
                "textAlign": "left",
            },
            style_data_conditional=[
                {"if": {"column_id": "Confirmed"}, "color": "rgb(101, 221, 155)", },
                {"if": {"column_id": "Deaths"}, "color": "#F65164", },
                {
                    "if": {"column_id": "Confirmed(Foreign)"},
                    "color": "rgb(248, 245, 64)",
                },
                {"if": {"column_id": "Critical"}, "color": "rgb(248, 245, 64)", },
                {"if": {"column_id": "Recovered"}, "color": "rgb(68, 155, 226)", },
            ],
        ),
    ]
)


@app.callback(
    [dash.dependencies.Output("india_state_table", "data")],
    [dash.dependencies.Input("dropdown", "value")],
)
def display_table(dropdown_value):
    if dropdown_value is None:
        return [df_india.to_dict("records")]

    dff = df_india[df_india["State/UT"].str.contains("|".join(dropdown_value))]
    return [dff.to_dict("records")]
