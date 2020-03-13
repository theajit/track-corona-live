import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import base64

from app import app

layout = html.Div([
            html.Img(src=app.get_asset_url('symptoms.jpg'),
                    style={
                        'height': '650px',
                        'width': '91%',
                        'textAlign': 'center',
                        'display': 'inline-block'
                    })
        ], style={'textAlign': 'center'}, className="row tweleve columns")