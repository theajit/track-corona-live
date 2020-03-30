import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import base64
import dash

from pages import home, livecoronamap, livecoronatable

external_stylesheets = ['https://codepen.io/theajit/pen/vYYxVLb.css']

#external JavaScript files
external_scripts = [
    'https://codepen.io/theajit/pen/JjdLvZE.js',
]
from app import app
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=external_scripts)
#server = app.server
#app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Title('Live Corona Track Online'),
    html.Br(),
    html.Div([

        html.Div([
             dcc.Link('Home ', href='/')
        ], className="two columns tab first page-view no-print"),

        html.Div([
             dcc.Link('Live Table ', href='/live-corona-world-table')
        ], className="two columns tab page-view no-print"),

        html.Div([
             html.A(' Map Coming Soon ', href='#')
        ], className="two columns tab page-view no-print"),

	html.Div([
             html.A('Twitter ', href='https://twitter.com/cocktails_guy',target = "_blank")
        ], className="two columns tab page-view no-print"),

	html.Div([
             html.A('LinkedIn ', href='https://www.linkedin.com/in/ajitsatpathy/',target = "_blank")
        ], className="two columns tab page-view no-print")


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
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
