# layouts.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from compare_tumor.callbacks import register_callbacks
from compare_tumor.data_functions import get_mz_values, get_case_columns_query, get_case_columns_vs_query, vs_columnNames, add_comparison_lines

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

main_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1("Cancer Research Portfolio", className="title"),
            html.P("About", className="about-text"),
            html.P(
                "In the same way that a recipe combines a few basic ingredients into a uniquely delicious baked confection, a portfolio is a collection of index funds intelligently mixed in the right proportions. Here you can learn about famous portfolios, study the real-world performance of each concept in both good times and bad, and generally get a good feel for the best investing ideas that the indexing world has to offer.",
                className='para'
            ),
            html.Div(className="border-line"),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Compound mz-h:", className="select-label"),
            dcc.Dropdown(
                id='compound-dropdown',
                options=[{'label': mz, 'value': mz}
                         for mz in get_mz_values("ascending")],
                placeholder="Select Mz Value",
                searchable=True,
                multi=False,
                style={'width': '100%'},
                className="select-input"
            ),
            html.Div(id='selected-mz-h-value', className="select-label"),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="outer-container-loading",
                type="circle",
                children=[
                    html.Div(
                        [
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id=f'scatter-plot-mz_minus_h-{i}',
                                        className="scatter-plot",
                                    ) for i in range(7)
                                ], className="inner-container"),
                            ]),

                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id=f'tumor-plot',
                                        className="tumor-plot",
                                    ),
                                ], md=6),
                                dbc.Col([
                                    dcc.Graph(
                                        id=f'normal-plot',
                                        className="normal-plot",
                                    ),
                                ], md=6),
                            ]),
                        ],
                        className="outer-container with-shadow",  # Added shadow
                    ),
                ],
            ),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Compound mz+h:", className="select-label"),
            dcc.Dropdown(
                id='compound-dropdown-mz-plus',
                options=[{'label': mz, 'value': mz}
                         for mz in get_mz_values("ascending_m_plus_h")],
                placeholder="Select M+H Value",
                searchable=True,
                multi=False,
                style={'width': '100%'},
                className="select-input"
            ),
            html.Div(id='selected-mz-plus-value'),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="outer-container-plus-loading",
                type="circle",
                children=[
                    html.Div(
                        [
                            dbc.Row([
                                dbc.Col([
                                    dcc.Graph(
                                        id=f'scatter-plot-mz_plus_h-{i}',
                                        className="scatter-plot",
                                    ) for i in range(7)
                                ], className="inner-container"),
                            ]),

                            dbc.Row([
                                dbc.Row([
                                    dcc.Graph(
                                        id=f'tumor-plus-plot',
                                        className="tumor-plot",
                                    ),

                                    dcc.Graph(
                                        id=f'normal-plus-plot',
                                        className="normal-plot",
                                    ),
                                ],),
                            ]),
                        ],
                        className="outer-container with-shadow",  # Added shadow
                    ),
                ],
            ),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            html.Label("Select Compound mz Compare:",
                       className="select-label"),
            dcc.Dropdown(
                id='compound-dropdown-compare',
                options=[{'label': mz, 'value': mz}
                         for mz in get_mz_values("tumor_comparable_plots")],
                placeholder="Select Mz Value",
                searchable=True,
                clearable=True,
                multi=False,
                style={'width': '100%'},
                className="select-input"
            ),
            html.Div(id='selected-mz-compare-value'),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="outer-container-loading",
                type="circle",
                children=[
                    html.Div(
                        [
                            dcc.Graph(
                                id=f'tumor-comparable-plot',
                                className="tumor-comparable-plot",

                            ),
                            dcc.Graph(
                                id=f'normal-comparable-plot',
                                className="normal-comparable-plot",

                            ),
                        ],
                        className="outer-container with-shadow",
                    ),
                ],
            ),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id="loading",
                className="loading",
                type="circle",
                children=[
                    html.Div(id="loading-output"),
                ],
            ),
        ], md=12),
    ]),
], fluid=True)  # Set fluid=True for a full-width container
