import dash
import dash_table
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html

from app import app

url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR30F8lYP3jG7YOq8es0PBpJIE5yvRVZffOyaqC0GgMBN6yt0Q-NI8pxS7hd1F9dYXnowSC6zpZmW9D/pubhtml/sheet?gid=1902046093&single=true&widget=true&headers=false"

df_list = pd.read_html(url)[0]

df = pd.DataFrame(df_list)

#df = df.drop(columns=["Unnamed: 0","Unnamed: 7","Unnamed: 8"])
#df = df.drop(columns=["Unnamed: 0","Unnamed: 7"])
df = df.drop(columns=["Unnamed: 0","Unnamed: 6","Unnamed: 9","Unnamed: 10","Unnamed: 11","Unnamed: 12","Unnamed: 13"])
#df_states.columns = ['United States', 'Confirmed','New Confirmed','Deaths', 'New Deaths','Serious & Critical','Recovered']

df_states = df.loc[5:, :]
#df_states.columns = ['United States', 'Confirmed', 'Deaths','Serious','Critical','Recovered']
df_states.columns = ['United States', 'Confirmed','New Confirmed','Deaths', 'New Deaths','Serious & Critical','Recovered']
df_states = df_states[:-3]

df_states = df_states.replace(to_replace = np.nan, value =0)

layout = html.Div([
    dcc.Dropdown(id='dropdown', options=[
        {'label': i, 'value': i} for i in df_states['United States'].unique()
    ], multi=True, placeholder='Search by State ...'),
    dash_table.DataTable(
    id='usa_state_table',
    columns=[{"name": i, "id": i} for i in df_states.columns],
    data=df_states.to_dict('records'),
    page_action="native",
    page_current= 0,
    page_size= 20,
    sort_action="native",

     style_cell={
        'backgroundColor': '#445175',
        'fontWeight': 'bold',
        'color': 'white'
    },

    style_data_conditional=[
        {
        'if': {'column_id': 'Confirmed'},
        'color': 'rgb(101, 221, 155)'
        },
        {
        'if': {'column_id': 'Deaths'},
        'color': '#F65164'
        },
        {
        'if': {'column_id': 'Serious & Critical'},
        'color': 'rgb(248, 245, 64)'
        },
        {
        'if': {'column_id': 'Critical'},
        'color': 'rgb(248, 245, 64)'
        },
        {
        'if': {'column_id': 'Recovered'},
        'color': 'rgb(68, 155, 226)'
        }
    ]
)
])


@app.callback(
    [dash.dependencies.Output('usa_state_table', 'data')],
    [dash.dependencies.Input('dropdown', 'value')])

def display_table(dropdown_value):
    if dropdown_value is None:
        return [df_states.to_dict('records')]

    dff = df_states[df_states['United States'].str.contains('|'.join(dropdown_value))]
    return [dff.to_dict('records')]
