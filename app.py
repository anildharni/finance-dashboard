import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import titlebar
import time
from data import tab_e,tab_r,treemapf,summary,summary2,break_down,ntrpie,centaxtrf,corp,exp,approp

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

app = dash.Dash(__name__)
server = app.server
app.title = 'SFR Dashboard'
bar_colors = ['#F5CDA7', '#FAA381', '#C9DBBA', '#99C5B5', '#899E8B', '#60935D', '#706C61', '#DCDBA8', '#13262F'
    , '#E9E6FF', '#91818A', '#0EB1D2']
colors = {
    'background': '#eef0a1',
    'text': '#092859'
}


app.layout = html.Div(
    [
        html.Div(
            titlebar(app),
        ),
        html.Button(
            html.A("SFR",
                    href='http://cedar.gov.in:8055',
                    target='_blank',),
               className="sidebarbtn"
                    ),
        # First Sunburst Graphs
        html.Div([
                html.Div(
                    children=[
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True},
                            figure=px.sunburst(
                                summary,
                                path=['Type', 'Section', 'Name'],
                                values='Values',
                                title="Summary of Fiscal Transactions 2017-18",
                                height=700,
                                width=700,
                                labels={
                                    "Name": "Name",
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                color="Section",
                                color_discrete_sequence=px.colors.diverging.Tropic[1:3] + ['#229e8a']
                            ),
                        ),
                    ],
                    className="six columns card"
                ),
                html.Div(
                    [
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True
                            },
                            figure=px.sunburst(
                                summary2,
                                path=['Type', 'Section', 'Name'],
                                values='Values',
                                title="Summary of Fiscal Transactions 2018-19",
                                height=700,
                                width=700,
                                labels={
                                    "Name": "Name",
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                color="Section",
                                color_discrete_sequence=px.colors.sequential.Brwnyl[1:],  # finished
                            ),
                        ),
                    ],
                    className="six columns card"
                )
            ], className="row",
        ),
        html.Div(
            [
                html.P(
                    ["This set of sunburst charts captures a snapshot of the finances of"
                     " the Government of Karnataka during 2017-18 and 2018-19(",
                     html.A(' ref.table 1.1 of state finance report',
                            href='http://cedar.gov.in:8055/finances/introduction',
                            target='_blank'),
                     "). These visualisations have Receipts and Disbursements at its center and the data flows outward"
                     " based on the sub classification. The classification ends at the outer-most node and "
                     "doesn't flow out further. Length of the arc signifies the value of that subclass. Greater"
                     " the length, higher the value. All the charts are clickable and interactive."]
                )
            ], style={
                "margin-left": "100px",
                "margin-right": "100px"
            }
        ),
        # treemap
        html.Div(
            className="twelve columns card",
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True
                            },
                            figure=px.treemap(
                                treemapf,
                                path=['Root', 'Year', "Type", "Sub Type", "Minor Head"],
                                values="Values",
                                title="Snapshot of Karnataka finances between 2014-15 and 2018-19",
                                height=800,
                                labels={
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                template="seaborn",
                                color="Year",
                            ).update_layout(
                                font_family="Times New Roman",
                                showlegend=False,
                                font_size=15,
                                uniformtext_minsize=15
                            )
                        )
                    ]
                ),
                html.Div(
                    children=[
                        html.P(
                            ["All the major financial parameters of karnataka between the years 2014 and 2019 are"
                             " represented in the above treemap visualisation (",
                             html.A('ref Appendix 1.4 of state finance report',
                                    href='http://cedar.gov.in:8055/appendix/appendix14',
                                    target='_blank'),
                             "). Treemaps are ideal for displaying large "
                             "amounts of hierarchically structured (tree-structured)data.The sizes of the rectangles"
                             " indicate that Public Account Receipts has the highest share while capital receipts are"
                             " the lowest.The rectangles are nested. Each rectangle that represents a "
                             "receipts/expenditure consists of rectangles representing Years within that type of "
                             "receipt/expenditure and it goes few more levels further down. To take a closer look at"
                             " a certain part of the treemap, you can navigate from a higher hierarchy level to a lower"
                             " one. Click on the hierarchy header of the level you want to navigate to."
                             "The uppermost hierarchy header displays the hierarchy levels from the top level to the"
                             " level you are currently viewing. To navigate upwards in the hierarchy, click on the level"
                             " you want to navigate to."])
                    ], style={
                        "margin-left": "100px",
                        "margin-right": "100px"
                    }
                ),
            ]
        ),
        # receipts graphs
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="six columns card",
                    children=[
                        dcc.Dropdown(id="receipts",
                                     options=[{'label': i, 'value': i} for i in tab_r.columns[1:]],
                                     value=[tab_r.columns[1], tab_r.columns[2]],
                                     multi=True),
                        dcc.Checklist(id="year_list_r",
                                      options=[{'label': " " + i, 'value': i} for i in tab_r.iloc[0:, 0].unique()],
                                      value=[tab_r.iloc[4, 0], tab_r.iloc[3, 0]],
                                      labelStyle={
                                          "display": "inline-block",
                                          "margin-right": "20px",
                                          "cursor": "pointer"
                                      }
                                      ),
                        dcc.Graph(id="year_vs_receipts",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                      # 'responsive': True
                                  }
                                  )
                    ],
                    style={"padding": 30}
                ),
                html.Div(
                    className="six columns card",
                    children=[
                        dcc.RadioItems(id="radio",
                                       options=[
                                           {'label': ' Capital Receipts', 'value': 'cap'},
                                           {'label': ' Revenue Receipts', 'value': 'rev'},
                                           {'label': ' Public Account Receipts(Net)', 'value': 'pub'}
                                       ],
                                       value='rev',
                                       labelStyle={
                                           "display": "inline-block",
                                           "margin-left": "20px",
                                           "cursor": "pointer"
                                       },
                                       style={
                                           "box-shadow": "0 1px 2px 0 rgba(0,0,0,.15)",
                                       }
                                       ),
                        dcc.Dropdown(id="subradio",
                                     multi=True,
                                     ),
                        dcc.Graph(id="breakdown",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                      # 'responsive': True
                                  }
                                  )
                    ], style={"padding": 30}
                )
            ]
        ),
        # Non tax revenue pie
        html.Div(
            className="row card",
            children=[
                html.Div(
                    className="four columns card",
                    children=[
                        dcc.Dropdown(id="types",
                                     options=[
                                         {'label': " " + i, 'value': i} for i in
                                         ntrpie.iloc[0:, 0]
                                     ],
                                     value=ntrpie.iloc[:, 0],
                                     multi=True
                                     ),
                    ],
                    style={
                        "padding": "20px"
                    }
                ),
                html.Div(
                    className="seven columns card",
                    children=html.Div(
                        dcc.Graph(id="pie",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                  },
                                  )
                    )
                )
            ]
        ),
        # Expenditure graph
        html.Div(
            [
                html.Div(
                    className="twelve columns card",
                    children=[
                        dcc.Dropdown(id="exp",
                                     options=[{'label': i, 'value': i} for i in exp.columns[1:]],
                                     value=[exp.columns[1], exp.columns[2], exp.columns[3],
                                            exp.columns[4], exp.columns[5], exp.columns[6], exp.columns[7],
                                            exp.columns[8]],
                                     multi=True,
                                     style={
                                         'margin-right': '600px'
                                     }),
                        dcc.Checklist(id="year_list_exp",
                                      options=[{'label': " " + i, 'value': i} for i in exp.iloc[0:, 0].unique()],
                                      value=[exp.iloc[2, 0], exp.iloc[3, 0], exp.iloc[4, 0]],
                                      labelStyle={
                                          "display": "inline-block",
                                          "margin-right": "20px",
                                          "cursor": "pointer"
                                      }
                                      ),
                        dcc.Graph(id="year_vs_exp",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                  }
                                  ),
                    ],
                    style={"padding": 30}
                )]),
        # financial assistance to local bodies
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="eight columns card",
                    children=[
                        dcc.Dropdown(id="outlay",
                                     options=[{'label': i, 'value': i} for i in tab_e.columns[1:]],
                                     value=[tab_e.columns[1], tab_e.columns[2], tab_e.columns[3]],
                                     multi=True),
                        dcc.Checklist(id="year_list",
                                      options=[
                                          {'label': " " + i, 'value': i} for i in
                                          tab_e.iloc[0:, 0].unique()
                                      ],
                                      value=[tab_e.iloc[4, 0], tab_e.iloc[3, 0], tab_e.iloc[2, 0]],
                                      labelStyle={
                                          "display": "inline-block",
                                          "margin-right": "20px",
                                          "cursor": "pointer"}
                                      ),
                        dcc.Graph(id="year_vs_everything",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                  },
                                  )
                    ],
                    style={"padding": 30}
                ),
                html.Div(
                    className="four columns card",
                    children=[
                        html.Li(
                            " The figures under assistance to ULBs differs from those shown in the earlier reports before 2014-15"
                            " on account of inclusion of devolutions under the Minor Head 200 – Other compensations and"
                            " assignment.",
                        ),
                        html.Li("Out of the total devolution of `35,898 crore to PRIs during 2018-19, "
                                "14,709 crore (41 per cent) were towards salaries as the State Government’s"
                                " functions viz., education, water supply and sanitation, housing, health and "
                                "family welfare etc., were transferred to PRIs"),
                        html.Li("The assistance to ULBs decreased by 1,064 crore over the previous year.  The "
                                "decrease was mainly due to short release of funds to Municipal Corporations, "
                                "Municipalities/Municipal Councils and Nagara Panchayats/ Notified Area Committees by "
                                "23%, 2% and 3% respectively.  ")
                    ], style={
                        'padding': 30
                    }
                ),
            ]
        ),
        # central tax transfers
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="five columns",
                    children=
                    [
                        html.Div(
                            children=[
                                dcc.Dropdown(id="trftype",
                                             options=[{'label': i, 'value': i} for i in centaxtrf.columns[1:]],
                                             value=[centaxtrf.columns[1], centaxtrf.columns[2], centaxtrf.columns[3]],
                                             multi=True),
                                dcc.Checklist(id="year_list_trf",
                                              options=[
                                                  {'label': " " + i, 'value': i} for i in
                                                  centaxtrf.iloc[0:, 0].unique()
                                              ],
                                              value=[centaxtrf.iloc[4, 0], centaxtrf.iloc[3, 0], centaxtrf.iloc[2, 0]],
                                              labelStyle={
                                                  "display": "inline-block",
                                                  "margin-right": "20px",
                                                  "cursor": "pointer"}
                                              )
                            ]
                        ),
                        html.Div(
                            html.P("During 2018-19, out of the total net collection of Union taxes of "
                                   "7,58,731.13 crore, the net devolution of State’s share was `35,894.83 crore and the"
                                   " share of Corporation tax, Taxes on income other than Corporation tax, Customs,"
                                   " Union Excise duties and CGST was 4.713 per cent, IGST was 5.177 per cent and Service "
                                   "tax was 4.822 per cent."),
                            className="card"
                            , style={
                                'padding': 30
                            })
                    ], style={
                        'padding': 30
                    }
                ),
                html.Div(
                    className="seven columns card",
                    children=[
                        dcc.Graph(id="year_vs_trftype",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                  },
                                  )
                    ],
                    style={"padding": 30}
                )
            ]
        ),
        # Sunburst appropriation accounts
        html.Div(
            [
                html.Div(
                    [
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True
                            },
                            figure=px.sunburst(
                                approp,
                                path=['Type', 'SubType', 'Name'],
                                values='Values',
                                title="Appropriation Accounts",
                                labels={
                                    "Name": "Name",
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                height=800,
                                color="Type",
                                color_discrete_map={'Voted': '#42b7b9',
                                                    'Charged ': '#d39c83', },
                            )
                        ),
                    ],
                    className="six columns card",
                ),
                # Scatter plot of appendix 2.14
                html.Div(
                    [
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True
                            },
                            figure=px.scatter(
                                corp,
                                x='Amount surrendered',
                                y='Total Provision',
                                log_y=True,
                                log_x=True,
                                size='No. of cases',
                                color='Notation',
                                hover_name="Grant No./Nomenclature",
                                title="Cases of surrendered of funds in excess of five crore",
                                height=800,
                                color_discrete_map={'Below 50': '#3bd9db',
                                                    'Above 50': '#e88456', },
                            ))
                    ], className="six columns card"),
            ]
        ),
    ], className="subpage1"
)

tab_e.set_index('Year', inplace=True)
tab_r.set_index('Year', inplace=True)
exp.set_index('Year', inplace=True)
centaxtrf.set_index('Particulars', inplace=True)


@app.callback(dash.dependencies.Output("year_vs_everything", "figure"),
              [dash.dependencies.Input("outlay", "value"),
               dash.dependencies.Input("year_list", "value")])
def update_graph(olay, lst):
    time.sleep(2)
    if len(olay) <= 1:
        dat1 = [dict(x=lst,
                     y=tab_e.loc[lst, :].iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=tab_e.loc[lst, :].iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = [dict(x=lst,
                     y=tab_e.loc[lst, :].iloc[:][item],
                     type="bar",
                     marker=go.bar.Marker(
                         color=bar_colors[olay.index(item) - 1]
                     ),
                     name=item)
                for item in olay[1:]]
    return (
        {"data": dat1 + dat2,
         "layout": go.Layout(
             title="Financial assistance to local bodies and other institutions",
             xaxis={
                 'title': 'Years (Expenditure in crs.)',
                 "showgrid": True,
                 "showticklabels": True
             },
             yaxis={
                 'title': 'Type of Institution',
                 "showgrid": True,
                 "showticklabels": True,
                 "tickformat": ",g"
             },
             legend=dict(
                 y=-0.2,
                 x=0.1,
                 orientation='h'
             )
         )
         }
    )


@app.callback(dash.dependencies.Output("year_vs_receipts", "figure"),
              [dash.dependencies.Input("receipts", "value"),
               dash.dependencies.Input("year_list_r", "value")])
def update_graph(rec, lst):
    if len(rec) <= 1:
        dat1 = [dict(x=lst,
                     y=tab_r.loc[lst, :].iloc[:][rec[0]],
                     type="bar",
                     mode="markers",
                     width=0.5,
                     name=rec[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=tab_r.loc[lst, :].iloc[:][rec[0]],
                     type="bar",
                     mode="markers",
                     name=rec[0])]
        dat2 = [dict(x=lst,
                     y=tab_r.loc[lst, :].iloc[:][item],
                     type="bar",
                     mode="markers",
                     marker=go.bar.Marker(
                         color=bar_colors[rec.index(item) - 1]
                     ),
                     name=item) for item in rec[1:]]
    return (
        {"data": dat1 + dat2,
         "layout": go.Layout(
             title="Comparison of Receipts over years",
             xaxis={
                 'title': 'Years',
                 "showgrid": True,
                 "showticklabels": True
             },
             yaxis={
                 'title': 'Variables selected in dropdown',
                 "showgrid": True,
                 "showticklabels": True,
                 "tickformat": ",g"
             },
             legend=dict(
                 y=-0.2,
                 x=0.1,
                 orientation='h'
             )
         )
         }
    )


@app.callback(
    dash.dependencies.Output('subradio', 'options'),
    [dash.dependencies.Input('radio', 'value')]
)
def update_date_dropdown(rdio):
    if rdio == "rev":
        return [{'label': i, 'value': i} for i in break_down.columns[1:4]]
    elif rdio == "pub":
        return [{'label': i, 'value': i} for i in break_down.columns[4:9]]
    elif rdio == "cap":
        return [{'label': i, 'value': i} for i in break_down.columns[9:]]


@app.callback(
    dash.dependencies.Output('subradio', 'value'),
    [dash.dependencies.Input('subradio', 'options')]
)
def update_subradio_val(available_options):
    return [available_options[0]['value']]


@app.callback(dash.dependencies.Output("breakdown", "figure"),
              [dash.dependencies.Input("radio", "value"),
               dash.dependencies.Input("subradio", "value")])
def update_graph(rad, srad):
    if len(srad) <= 1:
        dat1 = [dict(
            x=break_down.iloc[:, 0],
            y=break_down[srad[0]],
            type="bar",
            mode="markers",
            name=srad[0]
        )]
        dat2 = []
    elif len(srad) > 1:
        dat1 = [dict(
            x=break_down.iloc[:, 0],
            y=break_down[srad[0]],
            type="bar",
            mode="markers",
            name=srad[0]
        )]
        dat2 = [dict(
            x=break_down.iloc[:, 0],
            y=break_down[srad[item]],
            type="bar",
            mode="markers",
            marker=go.bar.Marker(
                color=bar_colors[item - 1]
            ),
            name=srad[item]
        ) for item in range(len(srad))[1:]]

    return ({"data": dat1 + dat2,
             "layout": go.Layout(
                 title="Comparison of Receipts over years",
                 xaxis={
                     'title': 'Years',
                     "showgrid": True,
                     "showticklabels": True
                 },
                 yaxis={
                     'title': 'Sub classification',
                     "showgrid": True,
                     "showticklabels": True,
                     "tickformat": ",g"
                 },
                 legend=dict(
                     y=-0.2,
                     x=0.1,
                     orientation='h'
                 )
             )
             })

@app.callback(dash.dependencies.Output("pie", "figure"),
              [dash.dependencies.Input("types", "value")])
def update_graph(typs):
    data = [
        {
            'labels': typs,
            'values': ntrpie.set_index('column1').loc[typs].iloc[:, 0],
            'type': 'pie',
            'marker': {
                'colors': ['#577590', '43aa8b', '90be6d', 'f9c74f', 'f8961e', 'f3722c', 'e07a5f',
                           "#4C3B4D", "#E94F37", "#320A28"]
            },
        }
    ]

    return ({
        "data": data,
        "layout":
            go.Layout(
                width=800,
                title="Components of Non tax revenue",
                margin={
                    "r": 100,
                    "t": 50,
                    "b": 50,
                    "l": 100,
                    "pad": 2,
                },
            )
    })


@app.callback(dash.dependencies.Output("year_vs_trftype", "figure"),
              [dash.dependencies.Input("trftype", "value"),
               dash.dependencies.Input("year_list_trf", "value")])
def update_graph(olay, lst):
    if len(olay) <= 1:
        dat1 = [dict(x=lst,
                     y=centaxtrf.iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=centaxtrf.iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = [dict(x=lst,
                     y=centaxtrf.loc[lst, :].iloc[:][item],
                     type="bar",
                     marker=go.bar.Marker(
                         color=bar_colors[olay.index(item) - 1]
                     ),
                     name=item) for item in olay[1:]]
    return (
        {"data": dat1 + dat2,
         "layout": go.Layout(
             title="Different taxes and their shares",
             xaxis={
                 'title': 'Years (Expenditure in crs.)',
                 "showgrid": True,
                 "showticklabels": True
             },
             yaxis={
                 'title': 'Type of Institution',
                 "showgrid": True,
                 "showticklabels": True,
                 "tickformat": ",g"
             },
             legend=dict(
                 y=-0.2,
                 x=0.1,
                 orientation='h'
             )
         )
         }
    )


@app.callback(dash.dependencies.Output("year_vs_exp", "figure"),
              [dash.dependencies.Input("exp", "value"),
               dash.dependencies.Input("year_list_exp", "value")])
def update_graph(rec, lst):
    if len(rec) <= 1:
        dat1 = [dict(x=lst,
                     y=exp.loc[lst, :].iloc[:][rec[0]],
                     type="bar",
                     mode="markers",
                     width=0.5,
                     name=rec[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=exp.loc[lst, :].iloc[:][rec[0]],
                     type="bar",
                     mode="markers",
                     name=rec[0])]
        dat2 = [dict(x=lst,
                     y=exp.loc[lst, :].iloc[:][item],
                     type="bar",
                     mode="markers",
                     marker=go.bar.Marker(
                         color=bar_colors[rec.index(item) - 1]
                     ),
                     name=item) for item in rec[1:]]
    return (
        {"data": dat1 + dat2,
         "layout": go.Layout(
             title="Comparison of Expenditures over years",
             xaxis={
                 'title': 'Years',
                 "showgrid": True,
                 "showticklabels": True
             },
             yaxis={
                 'title': 'Variables selected in dropdown',
                 "showgrid": True,
                 "showticklabels": True,
                 "tickformat": ",g"
             },
             legend=dict(
                 y=-0.2,
                 x=0.1,
                 orientation='h'
             )
         )
         }
    )


if __name__ == '__main__':
    app.run_server(debug=False)
    # app.run_server(debug=True, port=80)
