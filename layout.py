# layouts.py
import dash
from dash import dcc, html
from compare_tumor.callbacks import register_callbacks
from compare_tumor.data_functions import get_mz_values, get_meta_values, get_case_columns_query, get_case_columns_vs_query, vs_columnNames, add_comparison_lines
region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

main_layout = html.Div([
    # Added class to the title
    html.H1("Cancer Research Portfolio", className="title"),

    # Body content
    html.Div([
        # Added class to the about-text
        html.P("About", className="about-text"),
        html.P(
            "In the same way that a recipe combines a few basic ingredients into a uniquely delicious baked confection, a portfolio is a collection of index funds intelligently mixed in the right proportions. Here you can learn about famous portfolios, study the real-world performance of each concept in both good times and bad, and generally get a good feel for the best investing ideas that the indexing world has to offer."
        ),
        # Added class to the border-line
        html.Div(className="border-line"),
    ], className="main-container"),

    # Added class to the select label
    html.Label("Select Compound mz-h:", className="select-label"),
    dcc.Dropdown(
        id='compound-dropdown',
        options=[{'label': mz, 'value': mz} for mz in get_mz_values()],
        placeholder="Select Mz Value",
        searchable=True,
        multi=False,
        style={'width': '50%'},
        className="select-input"  # Added class to the select input
    ),
    html.Div(id='selected-mz-value'),

    html.Div(
        [
            dcc.Loading(
                id="outer-container-loading",
                type="circle",
                children=[
                    html.Div(
                        [
                            html.Div(
                                [
                                    dcc.Graph(
                                        id=f'scatter-plot-{i}',
                                        className="scatter-plot",
                                        style={
                                            'width': '100%',
                                            'display': 'inline-block',
                                            'marginRight': '10px'
                                        }
                                    ) for i in range(7)
                                ],
                                style={'display': 'flex'},
                                className="inner-container",
                            ),
                            html.Div(
                                [
                                    dcc.Graph(
                                        id=f'tumor-plot',
                                        style={
                                            'width': '50%',
                                            'display': 'inline-block',
                                            'marginRight': '10px'
                                        }
                                    ),
                                    dcc.Graph(
                                        id=f'normal-plot',
                                        style={
                                            'width': '50%',
                                            'display': 'inline-block',
                                            'marginRight': '10px'
                                        }
                                    ),
                                ],
                                style={'display': 'flex'}
                            ),
                        ],
                        className="outer-container",
                    ),
                ],
            ),
        ],
    ),

    # Added class to the select label
    html.Label("Select Compound mz Compare:", className="select-label"),
    dcc.Dropdown(
        id='compound-dropdown-compare',
        options=[{'label': mz, 'value': mz} for mz in get_meta_values()],
        placeholder="Select Mz Value",
        searchable=True,
        clearable=True,
        multi=False,
        style={'width': '50%'},
        className="select-input"  # Added class to the select input
    ),
    html.Div(id='selected-meta-value'),
    
    html.Div(
        [
            dcc.Loading(
                id="outer-container-loading",
                type="circle",
                children=[html.Div(
                    html.Div(
                        [
                            dcc.Graph(
                                id=f'tumor-comparable-plot',
                                style={'width': '50%', 'display': 'inline-block',
                                       'marginRight': '10px'}
                            ),
                            dcc.Graph(
                                id=f'normal-comparable-plot',
                                style={'width': '50%', 'display': 'inline-block',
                                       'marginRight': '10px'}
                            ),
                        ],
                        style={'display': 'flex'}
                    ),
                    className="outer-container",),]),
        ]

    ),

    # Loading indicator
    dcc.Loading(
        id="loading",
        className="loading",  # Added class to the loading indicator
        type="circle",  # Updated to circular loading animation
        children=[
            html.Div(id="loading-output"),
        ],
    ),]
)
