# layouts.py
import dash
from dash import dcc, html
from compare_tumor.callbacks import register_callbacks
from compare_tumor.data_functions import region
from compare_tumor.data_functions import get_meta_values, get_case_columns_vs_query, vs_columnNames, add_comparison_lines
from app import region

main_layout = html.Div([
    html.H1("Cancer Research Portfolio"),

    # Body content
    html.Div([
        html.P("About"),
        html.P(
            "In the same way that a recipe combines a few basic ingredients into a uniquely delicious baked confection, a portfolio is a collection of index funds intelligently mixed in the right proportions. Here you can learn about famous portfolios, study the real-world performance of each concept in both good times and bad, and generally get a good feel for the best investing ideas that the indexing world has to offer."
        ),
        html.Div(className="border-line"),
    ], className="main-container"),

    # Body content
    html.Div([
        html.P("This is some content in a body font."),
    ]),

    html.Label("Select Compound mz-h:"),
    dcc.Dropdown(
        id='compound-dropdown',
        options=[{'label': mz, 'value': mz} for mz in get_meta_values()],
        placeholder="Select Mz Value",
        searchable=True,
        multi=False,
        style={'width': '50%'},
    ),
    html.Div(id='selected-mz-value'),

    html.Div(
        [dcc.Graph(
            id=f'scatter-plot-{i}',
            style={'width': '100%', 'display': 'inline-block',
                   'margin-right': '10px'}
        ) for i in range(7)],
        style={'display': 'flex'}
    ),
    html.Div(
        [
            dcc.Graph(
                id=f'tumor-plot',
                style={'width': '50%', 'display': 'inline-block',
                       'margin-right': '10px'}
            ),
            dcc.Graph(
                id=f'normal-plot',
                style={'width': '50%', 'display': 'inline-block',
                       'margin-right': '10px'}
            ),
        ],
        style={'display': 'flex'}
    ),
    html.Label("Select Compound mz Compare:"),

    dcc.Dropdown(
        id='compound-dropdown-compare',
        options=[{'label': mz, 'value': mz} for mz in get_meta_values()],
        placeholder="Select Mz Value",
        searchable=True,
        clearable=True,
        multi=False,
        style={'width': '50%'},
    ),
    html.Div(id='selected-meta-value'),

    html.Div(
        [
            dcc.Graph(
                id=f'tumor-comparable-plot',
                style={'width': '50%', 'display': 'inline-block',
                       'margin-right': '10px'}
            ),
            dcc.Graph(
                id=f'normal-comparable-plot',
                style={'width': '50%', 'display': 'inline-block',
                       'margin-right': '10px'}
            ),
        ],
        style={'display': 'flex'}
    ),

    # Loading indicator
    dcc.Loading(
        id="loading",
        type="default",
        children=[
            html.Div(id="loading-output"),
        ],
    ),
])
