import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils import titlebar

BASE_PATH = pathlib.Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH.joinpath("data").resolve()

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__)
server=app.server
app.title = 'SFR Dashboard'
bar_colors = ['#F5CDA7', '#FAA381', '#C9DBBA', '#99C5B5', '#899E8B', '#60935D', '#706C61', '#DCDBA8']
# bar_colors[1] = 'crimson'
colors = {
    'background': '#eef0a1',
    'text': '#092859'
}

#data = pd.read_csv("C://Users//User//Documents//fullsample")

tab_e = pd.read_csv(DATA_PATH.joinpath("data.csv"), engine="python")
tab_r = pd.read_csv(DATA_PATH.joinpath("receipts.csv"), engine="python")
summary = pd.read_csv(DATA_PATH.joinpath("summary.csv"), engine="python")
summary2 = pd.read_csv(DATA_PATH.joinpath("summary2.csv"), engine="python")
break_down = pd.read_csv(DATA_PATH.joinpath("breakdown.csv"), engine="python")

# lang1_subs = data.LANG1_SUB_NAME.unique()
# school_type = data.SCHOOL_TYPE.unique()
# dist = data.DISTRICT_NAME.unique()
# paper_lst = ["LANG1_SUB_NAME", "LANG2_SUB_NAME", "LANG3_SUB_NAME",
#              "SUB1_SUB_NAME", "SUB2_SUB_NAME", "SUB3_SUB_NAME",
#              "SUB4_SUB_NAME", "SUB5_SUB_NAME"]

app.layout = html.Div(
    [
        html.Div(
            titlebar(app),
        ),
        html.Div(
            [

                html.Div(
                    [
                    dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True},
                            figure=px.sunburst(
                                summary,
                                path=['Type', 'Section', 'Name'],
                                values='Values',
                                title="Summary of Fiscal Transactions 2016-17",
                                height=700,
                                width=700,
                                labels={
                                    "Name": "Name",
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                color="Name",
                                color_discrete_sequence=px.colors.qualitative.Pastel,
                                # template="seaborn",
                                # color="Name",
                                # color_continuous_scale=px.colors.sequential.BuGn,
                                # range_color=[10,15],
                                # hover_data=None,
                                # maxdepth=2
                                # branchvalues="remainder",
                                # hoverinfo=None,
                                # hover_name='Values',
                                # hover_data={"Name": False, "Type":False, "Section":False}
                                # color="Unarmed",
                                # color_discrete_sequence=px.colors.qualitative.Pastel,
                                # maxdepth=-1,                        # set the sectors rendered. -1 will render all levels in the hierarchy
                                # color="Victim's age",
                                # color_continuous_scale=px.colors.sequential.BuGn,
                                # range_color=[10,100],

                                # branchvalues="total",               # or 'remainder'
                                # hover_name="Unarmed",
                                # # hover_data={'Unarmed': False},    # remove column name from tooltip  (Plotly version >= 4.8.0)
                                # title="7-year Breakdown of Deaths by Police",
                                # template='ggplot2',               # 'ggplot2', 'seaborn', 'simple_white', 'plotly',
                                #                                   # 'plotly_white', 'plotly_dark', 'presentation',
                                #                                   # 'xgridoff', 'ygridoff', 'gridon', 'none'
                            ),
                        ),
                        html.P(
                            "This Chart provides a broad perspective of the finances of the Government of Karnataka during"
                            " 2016-17. It analyses important changes in major fiscal indicators compared to previous year."
                            " This Analysis is based on the finance accounts and information obtained from the state government",
                            style={
                                "padding": "30px"
                            }
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
                                title="Summary of Fiscal Transactions 2017-18",
                                height=700,
                                width=700,
                                labels={
                                    "Name": "Name",
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                template="ggplot2",
                                #hover_name='Values',
                            ),
                        ),
                        html.P(
                            "This Chart provides a broad perspective of the finances of the Government of Karnataka during"
                            " 2017-18. It analyses important changes in major fiscal indicators of year 2017-18"
                            " This Analysis is based on the finance accounts obtained from the state government",
                            style={
                                "padding": "30px"
                            }
                        ),
                    ],
                    className="six columns card"
                )
            ], className="row",
        ),
        # Graph 1
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="nine columns card",
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
                                      value=[tab_e.iloc[4, 0], tab_e.iloc[3, 0], tab_e.iloc[1, 0]],
                                      labelStyle={
                                          "display": "inline-block",
                                          "margin-right": "20px",
                                          "cursor": "pointer"}
                                      ),
                        dcc.Graph(id="year_vs_everything",
                                  config={
                                      'modeBarButtonsToRemove': ['lasso2d'],
                                      'displaylogo': False,
                                      # 'responsive': True
                                  },
                                  )
                    ],
                    style={"padding": 30}
                ),
                html.Div(
                    className="two columns",
                    children=html.P(
                        "Expenditure over the years is on Y axis. Total outlay in 2018-19 is 2,24,000 crores"
                        "and gender budget expenditure is 1,02,792 crores"
                        , style={"padding": 30}
                        )
                )
            ]
        ),
        # span
        html.Br(),
        # text
        html.P(
            "We have receipts on side and we can see detailed granular analysis of receipts on the other side"
            "On the right the figure contains chained callbacks where input in dropdown is being dynamically updated"
            "We can compare both",
            style={
                'padding': "30px"
            }
        ),
        # row3
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
                        dcc.Dropdown(id="subradio",
                                     multi=True,
                                     ),
                        dcc.RadioItems(id="radio",
                                       options=[
                                           {'label': ' Capital Receipts', 'value': 'cap'},
                                           {'label': ' Revenue Receipts', 'value': 'rev'},
                                           {'label': ' Public Account Receipts(Net)', 'value': 'pub'}
                                       ],
                                       value='cap',
                                       labelStyle={
                                           "display": "inline-block",
                                           "margin-left": "20px",
                                           "cursor": "pointer"
                                       }
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
        )
    ], className="subpage1"
)

tab_e.set_index('Year', inplace=True)
tab_r.set_index('Year', inplace=True)


@app.callback(dash.dependencies.Output("year_vs_everything", "figure"),
              [dash.dependencies.Input("outlay", "value"),
               dash.dependencies.Input("year_list", "value")])
def update_graph(olay, lst):
    if len(olay) <= 1:
        dat1 = [dict(x=lst,
                     y=tab_e.iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=tab_e.iloc[:][olay[0]],
                     type="bar",
                     name=olay[0])]
        dat2 = [dict(x=lst,
                     y=tab_e.loc[lst, :].iloc[:][item],
                     type="bar",
                     marker=go.bar.Marker(
                         color=bar_colors[olay.index(item) - 1]
                     ),
                     name=item) for item in olay[1:]]
    return (
        {"data": dat1 + dat2,
         "layout": go.Layout(
             title="Comparison of Expenditure over years",
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


@app.callback(dash.dependencies.Output("year_vs_receipts", "figure"),
              [dash.dependencies.Input("receipts", "value"),
               dash.dependencies.Input("year_list_r", "value")])
def update_graph(rec, lst):
    if len(rec) <= 1:
        dat1 = [dict(x=lst,
                     y=tab_r.iloc[:][rec[0]],
                     type="bar",
                     mode="markers",
                     width=0.5,
                     name=rec[0])]
        dat2 = []
    else:
        dat1 = [dict(x=lst,
                     y=tab_r.iloc[:][rec[0]],
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
    return [{'label': i, 'value': i} for i in break_down.columns[1:]]


@app.callback(
    dash.dependencies.Output('subradio', 'value'),
    [dash.dependencies.Input('subradio', 'options')]
)
def set_cities_value(available_options):
    return [available_options[0]['value']]


# print(break_down["Revenue Receipts"]),print(break_down.iloc[:,1])
# r = ["Revenue Receipts", "Central tax transfers", "State's Own revenue"]
# q = "Revenue Receipts"
# print(break_down[r[0]])
# print([q])
# print((len(r)))


@app.callback(dash.dependencies.Output("breakdown", "figure"),
              [dash.dependencies.Input("radio", "value"),
               dash.dependencies.Input("subradio", "value")])
def update_graph(rad, srad):
    print(rad, srad)
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
            # marker_color=bar_colors[item-1],
            name=srad[item]
        ) for item in range(len(srad))[1:]]

    return ({"data": dat1 + dat2,
             "layout": go.Layout(
                 title="Comparison of Receipts over years",
                 # plot_bgcolor='aliceblue',
                 # colorscale="anil",
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


if __name__ == '__main__':
    #app.run_server(debug=False)
    app.run_server(debug=True, port=8049)
