import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from app import app

url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)

df_final = df.drop(
    columns=[
        "Unnamed: 0",
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
df_final.columns = [
    "Country",
    "Confirmed",
    "New Confirmed",
    "Deaths",
    "New Deaths",
    "Serious & Critical",
    "Recovered",
]
# df_country = df_final.loc[3:4, :]

df_country = df_final.loc[7:, :]
df_country = df_country[:-1]
# print (df_country)
# df_country = df_country.set_index("Country", inplace = True)

df_country = df_country.replace(np.nan, value=0)
# df_country = df_country.replace('-',0, regex=True)
# print (df_country)

# df_country.columns = ['Country', 'Confirmed', 'Deaths','Serious','Critical','Recovered']

df_country["Confirmed"] = df_country["Confirmed"].astype(int)
df_country["New Confirmed"] = df_country["New Confirmed"].astype(int)
df_country["Deaths"] = df_country["Deaths"].astype(int)
df_country["Deaths"] = df_country["Deaths"].astype(int)
df_country["Serious & Critical"] = df_country["Serious & Critical"].astype(int)
# df_country['Percentage of Deaths'] = pd.to_numeric(df_country['Percentage of Deaths'],errors='coerce')
# df_country['Percentage of Deaths'] = df_country['Percentage of Deaths'].astype(float)
df_country["Recovered"] = df_country["Recovered"].astype(int)
# df_country['iso_alpha'] = df_country['Country'].apply(lambda x: coco.convert(names=x, src='regex', to='ISO3', not_found = None))


# df_country = df_country[:-1]


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
