import dash_core_components as dcc
import dash_html_components as html


def titlebar(app):
    return html.Div(
        [
            get_header(app)
        ],
        className="titleheader"
    )


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        html.A(
                            html.Img(
                                src=app.get_asset_url("IAAD Logo.jpg"),
                                style={
                                    'height': '23%',
                                    'width': '23%',
                                    "margin-left": "160px"
                                }
                            ),
                            className="four columns",
                            href="https://agkar.gov.in",
                            target="_blank"),
                    ),
                    html.Div(
                        [
                            html.H4("State Financial Report, Karnataka 2019",
                                    style={"fontWeight": "bold"}
                                    )
                        ],
                        className="six columns main-title",
                        style={
                            "margin-left": "50px",
                            "margin-top": "30px"
                        }
                    ),
                    html.Div(
                        html.A(
                            html.Img(
                                src=app.get_asset_url("emblem.png"),
                                style={
                                    'height': '95px',
                                    'width': '45%',
                                    'textAlign': 'center'
                                }
                            ),
                            className="two columns",
                            href="https://cag.gov.in",
                            target="_blank")
                    )
                ],
                className="twelve columns",
                style={"padding-left": "0px"
                       },
            ),
        ],
        className="row",
    )
    return header
