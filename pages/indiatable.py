import pandas as pd

# from bs4 import BeautifulSoup
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from app import app


def return_df(url):
    url = url
    # Create a handle, page, to handle the contents of the website
    df_list = pd.read_html(url)[0]
    dfs = pd.DataFrame(df_list)
    return dfs


df_india = return_df("https://www.mohfw.gov.in/")
# print (df_india)
df_india = df_india.drop(columns=["S. No."])
df_india = df_india[:]
df_india.columns = ["State/UT", "Confirmed", "Recovered", "Deaths"]

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
                {"if": {"column_id": "Confirmed"}, "color": "rgb(101, 221, 155)",},
                {"if": {"column_id": "Deaths"}, "color": "#F65164",},
                {
                    "if": {"column_id": "Confirmed(Foreign)"},
                    "color": "rgb(248, 245, 64)",
                },
                {"if": {"column_id": "Critical"}, "color": "rgb(248, 245, 64)",},
                {"if": {"column_id": "Recovered"}, "color": "rgb(68, 155, 226)",},
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
