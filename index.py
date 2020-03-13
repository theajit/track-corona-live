import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import base64

from app import app
from pages import home,livecoronamap, livecoronatable



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Br(),
    html.Div([

        html.Div([
             dcc.Link('Home ', href='/')
        ], className="four columns tab first page-view no-print"),

        html.Div([
             dcc.Link('Live Table View ', href='/live-corona-world-table')
        ], className="four columns tab page-view no-print"),

        html.Div([
             dcc.Link('Live Map View ', href='/live-corona-world-map')
        ], className="four columns tab page-view no-print")


    ], style={'textAlign': 'center'}, className="row gs-header"),
    # Included sniper as per suggestion
    html.Div(dash_table.DataTable(), style={'display': 'none'}),

    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    elif pathname == '/live-corona-world-map':
        return livecoronamap.layout
    elif pathname == '/live-corona-world-table':
        return livecoronatable.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)