import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    [
        html.Br(),
        dcc.Tabs(
            id="tabs-with-classes",
            value="ajit",
            parent_className="custom-tabs",
            className="custom-tabs-container",
            children=[
                dcc.Tab(
                    label="Ajit Kumar Satpathy",
                    value="ajit",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="Sunit Kumar Behera",
                    value="sunit",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                ),
                dcc.Tab(
                    label="Neila Sreenivas",
                    value="neila",
                    className="custom-tab",
                    selected_className="custom-tab--selected",
                ),
            ],
        ),
        html.Div(id="tabs-content-classes"),
    ]
)


@app.callback(
    Output("tabs-content-classes", "children"), [Input("tabs-with-classes", "value")]
)
def render_content(tab):
    if tab == "ajit":
        return html.Div(
            [
                html.Br(),
                html.P(
                    [
                        "He holds a Bachelors in Electrical Engineering and pursuing Executive MBA at IIM, Kozhikode"
                    ]
                ),
                html.P(
                    ["Developer @ Xola || Data || Entrepreneur || Advisor || Startup"]
                ),
                html.P(
                    [
                        "You can contact him at ajit@theajit.in or find him in social platform as well"
                    ]
                ),
                html.Br(),
                html.Ul(
                    [
                        html.Li(
                            [
                                html.A(
                                    "Github ",
                                    href="https://github.com/theajit/",
                                    target="_blank",
                                )
                            ]
                        ),
                        html.Li(
                            [
                                html.A(
                                    "LinkedIn ",
                                    href="https://www.linkedin.com/in/ajitsatpathy/",
                                    target="_blank",
                                )
                            ]
                        ),
                        html.Li(
                            [
                                html.A(
                                    "Twitter ",
                                    href="https://twitter.com/cocktails_guy",
                                    target="_blank",
                                )
                            ]
                        ),
                    ]
                ),
            ]
        )
    elif tab == "sunit":
        return html.Div(
            [
                html.Br(),
                html.P(
                    [
                        "He holds a Bachelors in Mechanical Engineering and Post Graduation in Data Science"
                    ]
                ),
                html.P(
                    [
                        "His skills include Python , R, Pandas, Numpy, Machine Learning, AI, Deep Learning, Statistics, Part Modelling in CAD"
                    ]
                ),
                html.P(
                    [
                        "He has Prior Experience in Business Development, Business Analysis"
                    ]
                ),
                html.P(
                    [
                        ("You can contact him at sunit350@gmail.com or "),
                        html.A(
                            "LinkedIn profile ",
                            href="https://www.linkedin.com/in/sunit-behera-65a451136/",
                            target="_blank",
                        ),
                    ]
                ),
                html.Br(),
            ]
        )
    elif tab == "neila":
        return html.Div(
            [
                html.Br(),
                html.P(
                    [
                        "Post Graduate in Fashion Design and Clothing Technology. She is into apparel and graphic design."
                    ]
                ),
                html.P(
                    [
                        "Her skills include Adobe Illustrator, Photoshop and Corel Draw."
                    ]
                ),
                html.P(
                    [
                        ("You can contact her on "),
                        html.A(
                            "neilasree@yahoo.com ",
                            href="mailto:neilasree@yahoo.com",
                            target="_blank",
                        ),
                    ]
                ),
                html.Br(),
            ]
        )
