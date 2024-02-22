# layouts.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from compare_tumor.callbacks import register_callbacks
from compare_tumor.data_functions import get_mz_values, get_case_columns_query, get_case_columns_vs_query, vs_columnNames, add_comparison_lines

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]
tabs = dcc.Tabs([
    dcc.Tab(
        label='Mz-h',
        value='mz-h-tab',
        children=[
            dbc.Row([
                dbc.Col([html.Label("Select Compound mz-h:",  id="mz-h-section",
                                    className="select-label"),
                    dcc.Dropdown(
                        id='compound-dropdown',
                        options=[{'label': mz, 'value': mz}
                                 for mz in get_mz_values("ascending")],
                        placeholder="Select Mz Value",
                        searchable=True,
                        multi=False,
                        style={'width': '100%'},
                        className="select-input",
                        value=get_mz_values("ascending")[0]
                ),
                    html.Div(id='selected-mz-h-value',
                             className="select-label"),
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
                                            dcc.Graph(
                                                id=f'normal-plot',
                                                className="normal-plot",
                                            ),
                                        ], style={'display': 'flex'}),
                                    ]),
                                ],
                                className="outer-container with-shadow",  # Added shadow
                            ),
                        ],
                    ),
                ], md=12),
            ]),
        ]
    ),
    dcc.Tab(
        label='Mz+h',
        value='mz-plus-tab',
        children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Select Compound mz+h:",
                               id="mz-plus-section", className="select-label"),
                    dcc.Dropdown(
                        id='compound-dropdown-mz-plus',
                        options=[{'label': mz, 'value': mz}
                                 for mz in get_mz_values("ascending_m_plus_h")],
                        placeholder="Select M+H Value",
                        searchable=True,
                        multi=False,
                        style={'width': '100%'},
                        className="select-input",
                        value=get_mz_values("ascending_m_plus_h")[0]
                    ),
                    html.Div(id='selected-mz-plus-value'),
                ], md=12),


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
                                            ], style={'display': 'flex'}),
                                        ]),
                                    ],
                                    className="outer-container with-shadow",  # Added shadow
                                ),
                            ],
                        ),
                    ], md=12),
                ]),
            ]),
        ],
    ),

    # Add other tabs here if needed
    # dcc.Tab(label='Other Tab', value='other-tab', children=[...]),
], id='tabs', value='mz-h-tab', className='tabs')  # Initial selected tab is Mz-h
main_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H1("Colorectal Cancer Metabolome Database!", className="title"),
            html.P("About", className="about-text"),
            html.P(
                "Unlocking the complexities of colorectal cancer (CRC) requires a deeper understanding of its molecular landscape across different subsites of the colorectum. Our database is designed to serve as a comprehensive resource for researchers, clinicians, and enthusiasts alike, providing invaluable insights into CRC metabolomics and its implications for diagnosis, prognosis, and treatment. Explore metabolite markers across different colorectal subsites and identify survival markers for precision medicine. Join us in unraveling the intricacies of CRC and translating findings into impactful outcomes. Welcome to the forefront of colorectal cancer research!",
                className='para'
            ),
            
            
    dbc.Row([
        html.Div([  # Added a row of 3 buttons
                html.A("Mz-h", id="btn-mz-h", n_clicks=0,
                       className="btn-section btn-center", href="#mz-h-section"),
                html.Span("|", className="divider"), 
                html.A("Mz Compare", id="btn-mz-compare", n_clicks=0,
                       className="btn-section btn-center", href="#mz-compare-section"),
                html.Span("|", className="divider"),
                html.A("Mz Linear", id="btn-mz-linear", n_clicks=0,
                       className="btn-section btn-center", href="#mz-linear-section"),
            ], className="btn-row"),
                 
        ]),
            html.Div(className="border-line"),
        ], md=12),
    ]),

    dbc.Row([
        dbc.Col([
            # html.Div([  # Added a row of 3 buttons
            #     html.A("Mz-h", id="btn-mz-h", n_clicks=0,
            #            className="btn-section btn-center", href="#mz-h-section"),
            #     html.A("Mz Compare", id="btn-mz-compare", n_clicks=0,
            #            className="btn-section btn-center", href="#mz-compare-section"),
            #     html.A("Mz Linear", id="btn-mz-linear", n_clicks=0,
            #            className="btn-section btn-center", href="#mz-linear-section"),
            # ], className="btn-row"),

            dbc.Row([
                dbc.Col([
                    tabs,
                    html.Div(id='tabs-content'),
                ], md=12),
            ]),

        ], md=12),
    ]),

    html.Div(className="border-line"),

    dbc.Row([
        dbc.Col([
            html.Label("Select Compound mz Compare:", id="mz-compare-section",
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
                className="select-input",
                value=get_mz_values("tumor_comparable_plots")[0]
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
                        ], style={'display': 'flex'},
                        className="outer-container with-shadow",
                    ),
                ],
            ),
        ], md=12),
    ]),
    html.Div(className="border-line"),


    dbc.Row([
        dbc.Col([
            html.Label("Select Compound mz Linear:", id="mz-linear-section",
                       className="select-label"),
            dcc.Dropdown(
                id='compound-dropdown-linear',
                options=[{'label': mz, 'value': mz}
                         for mz in get_mz_values("tumor_linear_plots")],
                placeholder="Select Mz Value",
                searchable=True,
                clearable=True,
                multi=False,
                style={'width': '100%'},
                className="select-input",
                value=get_mz_values("tumor_linear_plots")[0]
            ),
            html.Div(id='selected-mz-linear-value'),
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
                                id=f'tumor-linear-plot',
                                className="tumor-linear-plot",

                            ),
                            dcc.Graph(
                                id=f'normal-linear-plot',
                                className="normal-linear-plot",

                            ),
                        ], style={'display': 'flex'},
                        className="outer-container with-shadow",
                    ),
                ],
            ),
        ], md=12),
    ]),
    
    html.Div(className="border-line"),


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
], fluid=True)
