from apscheduler.schedulers.background import BackgroundScheduler
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html

from app import app

from .functions import worlddata

url_world = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"
world_start = 7
world_strip = 1


def world_table_sensor():
    print("World Table Page Sensor Working!")
    return worlddata.return_world_table_df(url_world, world_start, world_strip)


world_sched = BackgroundScheduler(daemon=True)
world_sched.add_job(world_table_sensor, "interval", minutes=55)
world_sched.start()

df_country = world_table_sensor()

layout = html.Div(
    [
        dcc.Dropdown(
            id="dropdown",
            options=[{"label": i, "value": i} for i in df_country.Country.unique()],
            multi=True,
            placeholder="Search by Country ...",
        ),
        dash_table.DataTable(
            id="country_table",
            columns=[{"name": i, "id": i} for i in df_country.columns],
            data=df_country.to_dict("records"),
            page_action="native",
            page_current=0,
            page_size=15,
            sort_action="native",
            style_cell={
                "backgroundColor": "#445175",
                "fontWeight": "bold",
                "color": "white",
            },
            style_data_conditional=[
                {"if": {"column_id": "Confirmed"}, "color": "rgb(101, 221, 155)"},
                {"if": {"column_id": "Deaths"}, "color": "#F65164"},
                {"if": {"column_id": "Serious"}, "color": "rgb(248, 245, 64)"},
                {"if": {"column_id": "Critical"}, "color": "rgb(248, 245, 64)"},
                {"if": {"column_id": "Recovered"}, "color": "rgb(68, 155, 226)"},
            ],
        ),
    ]
)


@app.callback(
    [dash.dependencies.Output("country_table", "data")],
    [dash.dependencies.Input("dropdown", "value")],
)
def display_table(dropdown_value):
    if dropdown_value is None:
        return [df_country.to_dict("records")]

    dff = df_country[df_country.Country.str.contains("|".join(dropdown_value))]
    return [dff.to_dict("records")]
