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
server = app.server
app.title = 'SFR Dashboard'
bar_colors = ['#F5CDA7', '#FAA381', '#C9DBBA', '#99C5B5', '#899E8B', '#60935D', '#706C61', '#DCDBA8', '#13262F'
    , '#E9E6FF', '#91818A', '#0EB1D2']
# bar_colors[1] = 'crimson'
colors = {
    'background': '#eef0a1',
    'text': '#092859'
}


# remove later
# df1 = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/sunburst-coffee-flavors-complete.csv')
# print(df1.head(20))

# df= pd.read_csv(DATA_PATH.joinpath("treemap.csv"), engine="python")
# levels= ["Root","Type","Sub Type"]
# color_columns=["Values","2018-19"]
# value_column=["2018-19"]
def build_hierarchical_dataframe(df, levels, value_column, color_columns=None):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value', 'color'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i + 1]].copy()
        else:
            df_tree['parent'] = 'total'
        df_tree['value'] = dfg[value_column]
        df_tree['color'] = dfg[color_columns[0]] / dfg[color_columns[1]]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='total', parent='',
                           value=df[value_column].sum(),
                           color=df[color_columns[0]].sum() / df[color_columns[1]].sum()))
    df_all_trees = df_all_trees.append(total, ignore_index=True)
    return df_all_trees


# df_all_trees = build_hierarchical_dataframe(df, levels, value_column, color_columns)

# print(df_all_trees.iloc[:,1:3].head(15))


# till here remove

# data = pd.read_csv("C://Users//User//Documents//fullsample")

tab_e = pd.read_csv(DATA_PATH.joinpath("data.csv"), engine="python")
tab_r = pd.read_csv(DATA_PATH.joinpath("receipts.csv"), engine="python")
summary = pd.read_csv(DATA_PATH.joinpath("summary.csv"), engine="python")
summary2 = pd.read_csv(DATA_PATH.joinpath("summary2.csv"), engine="python")
break_down = pd.read_csv(DATA_PATH.joinpath("breakdown.csv"), engine="python")
treemapf = pd.read_csv(DATA_PATH.joinpath("treemap_fin.csv"), engine="python")
ntrpie = pd.read_csv(DATA_PATH.joinpath("nontaxrevpie.csv"), engine="python")
centaxtrf = pd.read_csv(DATA_PATH.joinpath("centaxtrf.csv"), engine="python")

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
                                # color_discrete_sequence=px.colors.sequential.Mint[3:],
                                # color_discrete_sequence=px.colors.sequential.ice[5:], #almost finalised
                                # color="Section",
                                # color_discrete_sequence=px.colors.qualitative.Pastel,
                                # template="seaborn",
                                # color="Name",
                                # color_continuous_scale=px.colors.sequential.BuGn,
                                # range_color=[10,15],
                                # hover_data=None,
                                # maxdepth=2
                                # branchvalues="remainder",
                                # hoverinfo=None,
                                # hover_name='Values',
                                # hover_data={"Name": False, "Type":False, "Section":False},
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
                                #                                   # 'xgridoff', 'ygridoff', 'gridon', 'none',
                                # template='ggplot2'
                            ),
                        ),
                        html.Div(
                            [
                                html.P(
                                    "This set of sunburst charts captures a snapshot of the finances of the Government of Karnataka during"
                                    " 2017-18 and 2018-19. It visualises important changes in major fiscal indicators vis-à-vis the other"
                                    " and is based on the finance accounts and information obtained from the Government of Karnataka."
                                )
                            ], style={
                                "padding": "30px"
                            }
                        )
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
                                # template="ggplot2",
                                color="Section",
                                color_discrete_sequence=px.colors.sequential.Brwnyl[1:],  # finished
                                # hover_name='Values',
                            ),
                        ),
                        html.Div(
                            [
                                "These visualisations have Receipts and Disbursements at its center and the data flows outward"
                                " based on the sub classification. The classification ends at the outer-most node and "
                                "doesn't flow out further. Length of the arc signifies the value of that subclass. Greater"
                                " the length, higher the value. All the charts are clickable and interactive. Explore at will. ",
                            ], style={
                                "padding": "30px"
                            }
                        )
                    ],
                    className="six columns card"
                )
            ], className="row",
        ),
        # treemap
        html.Div(
            className="twelve columns card",
            children=[
                html.Div(
                    style={
                        'padding': '30px'
                    },
                    children=[
                        dcc.Graph(
                            config={
                                'displaylogo': False,
                                'responsive': True
                            },
                            figure=px.treemap(
                                # summary,
                                # path=['Type', 'Section', 'Name'],
                                # values='Values',
                                treemapf,
                                path=['Root', 'Year', "Type", "Sub Type", "Minor Head"],
                                values="Values",
                                title="Snapshot of Karnataka finances between 2014-15 and 2018-19",
                                height=800,
                                # width=1420,
                                labels={
                                    "parent": "Classified under",
                                    "Values": "Amount in Rupees",
                                    "labels": "id",
                                },
                                template="seaborn",
                                color="Year",
                                # color_discrete_sequence=px.colors.sequential.PuBuGn[1::], #finished
                                # hover_name='Values',
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
                            "All the major financial parameters of karnataka between the years 2014 and 2019 are"
                            " represented in this treemap visualisation. Treemaps are ideal for displaying large "
                            "amounts of hierarchically structured (tree-structured)data.The sizes of the rectangles"
                            " indicate that Public Account Receipts has the highest share while capital receipts are"
                            " the lowest.The rectangles are nested. Each rectangle that represents a "
                            "receipts/expenditure consists of rectangles representing Years within that type of "
                            "receipt/expenditure and it goes few more levels further down. To take a closer look at"
                            " a certain part of the treemap, you can navigate from a higher hierarchy level to a lower"
                            " one. Click on the hierarchy header of the level you want to navigate to."
                            "The uppermost hierarchy header displays the hierarchy levels from the top level to the"
                            " level you are currently viewing. To navigate upwards in the hierarchy, click on the level"
                            " you want to navigate to.")
                    ], style= {
                        "margin-left":"100px",
                        "margin-right":"100px",
                        "padding-bottom":"30px"
                    }
                )
            ]
        ),
        # Graph 1
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
                                      # 'responsive': True
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
        # span
        html.Br(),
        # text
        html.P(
            "We have receipts on side and we can see detailed granular analysis of receipts on the other side. "
            "On the right the figure contains chained callbacks where input in dropdown is being dynamically updated. ",
            style={
                'padding': "30px"
            },
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
        # row 4
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
                                      # 'responsive': True
                                  },
                                  )
                    )
                )
            ]
        ),
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
                                      # 'responsive': True
                                  },
                                  )
                    ],
                    style={"padding": 30}
                )
            ]
        ),
    ], className="subpage1"
)

tab_e.set_index('Year', inplace=True)
tab_r.set_index('Year', inplace=True)
centaxtrf.set_index('Particulars', inplace=True)


@app.callback(dash.dependencies.Output("year_vs_everything", "figure"),
              [dash.dependencies.Input("outlay", "value"),
               dash.dependencies.Input("year_list", "value")])
def update_graph(olay, lst):
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


# typ = ["Dividend and profits"]
# print(ntrpie.set_index('column1').loc[["Dividend and profits", "Police"]].iloc[:, 0])


# print(ntrpie.loc[0,0])

@app.callback(dash.dependencies.Output("pie", "figure"),
              [dash.dependencies.Input("types", "value")])
def update_graph(typs):
    data = [
        {
            'labels': typs,
            'values': ntrpie.set_index('column1').loc[typs].iloc[:, 0],
            'type': 'pie',
            'hole': 0.4,
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


if __name__ == '__main__':
    # app.run_server(debug=False)
    app.run_server(debug=True, port=8049)
