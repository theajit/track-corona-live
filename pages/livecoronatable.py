import dash
import dash_table
import pandas as pd
import country_converter as coco
from app import app

url = "https://docs.google.com/spreadsheets/u/0/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?headers=false&gid=0"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)
df.set_index('Unnamed: 0', inplace=True)


df_final = df.drop(columns=["Unnamed: 7","Unnamed: 8"])

df_total = df_final.loc[3:4, :]

df_country = df_final.loc[7:, :]
df_country.columns = ['Country', 'Confirmed', 'Deaths','Serious','Critical','Recovered']
df_country['iso_alpha'] = df_country['Country'].apply(lambda x: coco.convert(names=x, src='regex', to='ISO3', not_found = None))


df_country = df_country[:-1]


layout = dash_table.DataTable(
    id='country_table',
    columns=[{"name": i, "id": i} for i in df_country.columns],
    data=df_country.to_dict('records'),
    page_action="native",
    page_current= 0,
    page_size= 19,
    sort_action="native",

     style_cell={
        'backgroundColor': '#445175',
        'fontWeight': 'bold',
        'color': 'white',
        'textAlign': 'left',
        'width': '5%'
    },

    style_data_conditional=[
        {
        'if': {'column_id': 'Confirmed'},
        'color': 'rgb(101, 221, 155)',
        'width': '5%'
        },
        {
        'if': {'column_id': 'Deaths'},
        'color': '#F65164',
        'width': '5%'
        },
        {
        'if': {'column_id': 'Serious'},
        'color': 'rgb(248, 245, 64)',
        'width': '5%'
        },
        {
        'if': {'column_id': 'Critical'},
        'color': 'rgb(248, 245, 64)',
        'width': '5%'
        },
        {
        'if': {'column_id': 'Recovered'},
        'color': 'rgb(68, 155, 226)',
        'width': '5%'
        }
    ]
)