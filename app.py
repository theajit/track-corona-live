import dash

external_stylesheets = ['https://codepen.io/theajit/pen/vYYxVLb.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True