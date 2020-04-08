import dash_html_components as html

layout = html.Div([
    html.P(
        [
            ("For detailed prediction "),
            html.A(
                "click here",
                href="https://trackcorona.online/prediction",
                target="_blank",
            ),
        ]
    ),
    html.P(
        [
            ("Special thanks to Ganesh Prasad for the prediction. For his wonderful work visit "),
            html.A(
                "Gnsp.in",
                href="https://gnsp.in",
                target="_blank",
            ),
        ]
    ),
    html.Iframe(src="https://gnsp.in/covid19?source=trackcorona.online", width="100%", height="700", style={'border': 'none'}, className="twelve columns")
], className="twelve columns")
