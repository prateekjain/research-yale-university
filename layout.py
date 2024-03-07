# layouts.py
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from compare_tumor.callback import register_callbacks
from compare_tumor.data_functions import (
    get_mz_values,
    get_case_columns_query,
    get_case_columns_vs_query,
    vs_columnNames,
    add_comparison_lines,
    get_cecum_and_ascending_mz_values,
    get_dropdown_options,
)

region = [
    "cecum",
    "ascending",
    "transverse",
    "descending",
    "sigmoid",
    "rectosigmoid",
    "rectum",
]




tabs_mz = dcc.Tabs(
    [
        dcc.Tab(
            label="Negative ions",
            value="mz-h-tab",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select Compound mz-h:",
                                    id="mz-h-section",
                                    className="select-label",
                                ),
                                dcc.Dropdown(
                                    id="compound-dropdown",
                                    options=[
                                        {"label": mz, "value": mz}
                                        for mz in get_mz_values("ascending")
                                    ],
                                    placeholder="Select Mz Value",
                                    searchable=True,
                                    multi=False,
                                    style={"width": "100%"},
                                    className="select-input",
                                    value=get_mz_values("ascending")[0],
                                ),
                                html.Div(
                                    id="selected-mz-h-value",
                                    className="select-label",
                                ),
                            ],
                            md=12,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Loading(
                                    id="outer-container-loading",
                                    type="circle",
                                    children=[
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dcc.Graph(
                                                                    id=f"scatter-plot-mz_minus_h-{i}",
                                                                    className="scatter-plot",
                                                                )
                                                                for i in range(7)
                                                            ],
                                                            className="inner-container",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dcc.Graph(
                                                                    id="tumor-plot",
                                                                    className="tumor-plot",
                                                                ),
                                                                dcc.Graph(
                                                                    id="normal-plot",
                                                                    className="normal-plot",
                                                                ),
                                                            ],
                                                            style={
                                                                "display": "flex"
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="outer-container with-shadow",
                                        ),
                                    ],
                                ),
                            ],
                            md=12,
                        ),
                    ]
                ),
            ],
        ),
        dcc.Tab(
            label="Positive ions",
            value="mz-plus-tab",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select Compound mz+h:",
                                    id="mz-plus-section",
                                    className="select-label",
                                ),
                                dcc.Dropdown(
                                    id="compound-dropdown-mz-plus",
                                    options=[
                                        {"label": mz, "value": mz}
                                        for mz in get_mz_values("ascending_m_plus_h")
                                    ],
                                    placeholder="Select M+H Value",
                                    searchable=True,
                                    multi=False,
                                    style={"width": "100%"},
                                    className="select-input",
                                    value=get_mz_values(
                                        "ascending_m_plus_h")[0],
                                ),
                                html.Div(id="selected-mz-plus-value"),
                            ],
                            md=12,
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Loading(
                                    id="outer-container-plus-loading",
                                    type="circle",
                                    children=[
                                        html.Div(
                                            [
                                                dbc.Row(
                                                    [
                                                        dbc.Col(
                                                            [
                                                                dcc.Graph(
                                                                    id=f"scatter-plot-mz_plus_h-{i}",
                                                                    className="scatter-plot",
                                                                )
                                                                for i in range(7)
                                                            ],
                                                            className="inner-container",
                                                        ),
                                                    ]
                                                ),
                                                dbc.Row(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dcc.Graph(
                                                                    id="tumor-plus-plot",
                                                                    className="tumor-plot",
                                                                ),
                                                                dcc.Graph(
                                                                    id="normal-plus-plot",
                                                                    className="normal-plot",
                                                                ),
                                                            ],
                                                            style={
                                                                "display": "flex"
                                                            },
                                                        ),
                                                    ]
                                                ),
                                            ],
                                            className="outer-container with-shadow",
                                        ),
                                    ],
                                ),
                            ],
                            md=12,
                        ),
                    ]
                ),
            ],
        ),
    ],
    id="tabs_mz",
    value="mz-h-tab",
    className="tabs",
)

tabs_compare = dcc.Tabs(
    [
        dcc.Tab(
            label="7 Subsites",
            value="compare-all",
            children=[
                dbc.Row(
                    [
                        html.Label(
                            "Select Compound mz Compare:",
                            id="mz-compare-section",
                            className="select-label",
                        ),
                        dcc.Dropdown(
                            id="compound-dropdown-compare",
                            options=[
                                {"label": mz, "value": mz}
                                for mz in get_mz_values("tumor_comparable_plots")
                            ],
                            placeholder="Select Mz Value",
                            searchable=True,
                            clearable=True,
                            multi=False,
                            style={"width": "100%"},
                            className="select-input",
                            value=get_mz_values("tumor_comparable_plots")[0],
                        ),
                        html.Div(id="selected-mz-compare-value"),
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dcc.Loading(
                                            id="outer-container-loading",
                                            type="circle",
                                            children=[
                                                html.Div(
                                                    [
                                                        dcc.Graph(
                                                            id="tumor-comparable-plot",
                                                            className="tumor-comparable-plot",
                                                        ),
                                                        dcc.Graph(
                                                            id="normal-comparable-plot",
                                                            className="normal-comparable-plot",
                                                        ),
                                                    ],
                                                    style={"display": "flex"},
                                                    className="outer-container with-shadow",
                                                ),
                                            ],
                                        ),
                                    ],
                                    md=12,
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ),
        dcc.Tab(
            label="LCC, RCC, Rectum",
            value="compare-rcc-lcc",
            children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label(
                                    "Select Compound RCC LCC mz Compare:",
                                    id="mz-compare-rcc-lcc-section",
                                    className="select-label",
                                ),
                                dcc.Dropdown(
                                    id="compound-dropdown-compare-rcc-lcc",
                                    options=[
                                        {"label": mz, "value": mz}
                                        for mz in get_mz_values("tumor_rcc_lcc_comparable_plots")

                                    ],
                                    placeholder="Select Mz Value",
                                    searchable=True,
                                    clearable=True,
                                    multi=False,
                                    style={"width": "100%"},
                                    className="select-input",
                                    value=get_mz_values(
                                        "tumor_rcc_lcc_comparable_plots")[0],
                                ),
                                html.Div(
                                    id="selected-mz-compare-rcc-lcc-value"),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dcc.Loading(
                                                    id="outer-container-loading",
                                                    type="circle",
                                                    children=[
                                                        html.Div(
                                                            [
                                                                dcc.Graph(
                                                                    id="tumor-comparable-rcc-lcc-plot",
                                                                    className="tumor-comparable-rcc-lcc-plot",
                                                                ),
                                                                dcc.Graph(
                                                                    id="normal-comparable-rcc-lcc-plot",
                                                                    className="normal-omparable-rcc-lcc-plot",
                                                                ),
                                                            ],
                                                            style={
                                                                "display": "flex"},
                                                            className="outer-container with-shadow",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                            md=12,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        ),
    ],
    id="tabs_compare",
    value="compare-all",
    className="tabs",
)

main_layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Br(),
                        html.H1("Colorectal Cancer Metabolome Database!",
                                className="title"),
                        html.P("About", className="about-text"),
                        html.P(
                            "Unlocking the complexities of colorectal cancer (CRC) requires a deeper understanding of its molecular landscape across different subsites of the colorectum. Our database is designed to serve as a comprehensive resource for researchers, clinicians, and enthusiasts alike, providing invaluable insights into CRC metabolomics and its implications for diagnosis, prognosis, and treatment. Explore metabolite markers across different colorectal subsites and identify survival markers for precision medicine. Join us in unraveling the intricacies of CRC and translating findings into impactful outcomes. Welcome to the forefront of colorectal cancer research!",
                            className="para",
                        ),
                        dbc.Row(
                            [
                                html.Div(
                                    [
                                        html.A(
                                            "Mz-h",
                                            id="btn-mz-h",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section1",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Mucosa2",
                                            id="btn-mz-Mucosa2",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section2",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Inter-subsite ",
                                            id="btn-inter-subsite",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section3",
                                        ),

                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Linear metabolite",
                                            id="btn-mz-linear",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section4",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Survival Metabolite",
                                            id="btn-mz-Survival",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section5",
                                        ),
                                    ],
                                    className="btn-row",
                                ),
                            ]
                        ),
                        html.Div(className="border-line"),
                    ],
                    md=12,
                ),
            ]
        ),
        dbc.Row(
            [
                html.H2(
                    "Tumor vs. Normal Mucosa Metabolic features Comparison Across Subsites 1",
                    className="section-heading",
                    id="section1",
                ),
                html.P(
                    "In this Section, we present the comparison between tumors and matched normal mucosa across all seven subsites of CRC. This analysis encompasses 10,126 metabolic features in HILIC negative mode and 9,600 features in RPLC positive mode. Statistical significance was determined using a paired Mann-Whitney U test, with all p-values adjusted for multiple comparisons using the Benjamini-Hochberg (BH) false discovery rate (FDR).",
                    className="section-description",
                ),
                dbc.Col(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [tabs_mz, html.Div(id="tabs-content")], md=12),
                            ]
                        ),
                    ],
                    md=12,
                ),
            ]
        ),
        html.Div(className="border-line"),
        # add tabs to it
        dbc.Row(
            [
                html.H2(
                    "Tumor vs. Normal Mucosa Metabolite Comparison Across Subsites 2",
                    className="section-heading",
                    id="section2",
                ),
                html.P(
                    "In this Section, we present the comparison between tumors and matched normal mucosa across all seven subsites of CRC. This analysis focuses on 409 annotated metabolites, with 220 annotated using standards and 190 annotated at level 3. Statistical significance was assessed using a paired Mann-Whitney U test, with all p-values adjusted for multiple comparisons using the Benjamini-Hochberg (BH) false discovery rate (FDR) method. Additionally, users can analyze the unique metabolite alteration specific to each subsite",
                    className="section-description",
                ),
            ]),
        dbc.Row([
                dbc.Col([
                    html.Label(
                        "Select Filter:",
                        id="filter-section-meta",
                        className="select-label",
                    ),
                    dcc.RadioItems(
                        id="filter-radio",
                        options=[
                            {"label": "All metabolites", "value": "all"},
                            {"label": "Metabolites altered across all subsites",
                             "value": "across_all"},
                            {"label": "Subsites specific alterations",
                             "value": "specific_subsites"},
                            {"label": "Proximal or Distal subsites",
                             "value": "proximal_distal"},
                        ],
                        value="all",
                        inline=True,  # Display radio items horizontally
                        className="select-input",
                    ),
                ],
                    md=4,
                ),
                ]),
        dbc.Row([
                dbc.Col([
                    html.Label(
                        "Select Compound meta:",
                        id="meta-section",
                        className="select-label",
                    ),
                    dcc.Dropdown(
                        id="compound-dropdown-meta",
                        placeholder="Select Meta Value",
                        searchable=True,
                        multi=False,
                        style={"width": "100%"},
                        className="select-input",
                    ),
                    html.Div(
                        id="selected-meta-value",
                        className="select-label",
                    ),
                ],
                    md=12,
                ),
                ]),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="outer-container-plus-loading",
                            type="circle",
                            children=[
                                html.Div(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dcc.Graph(
                                                            id=f"scatter-plot-meta-{i}",
                                                            className="scatter-plot",
                                                        )
                                                        for i in range(7)
                                                    ],
                                                    className="inner-container",
                                                ),
                                            ]
                                        ),

                                    ],
                                    className="outer-container with-shadow",
                                ),
                            ],
                        ),
                    ],
                    md=12,
                ),
            ]
        ),
        html.Div(className="border-line"),

        dbc.Row(
            [
                html.H2(
                    "Inter-subsite metabolites comparisons 3",
                    className="section-heading",
                    id="section3",
                ),
                html.P(
                    "Your description goes here. Provide relevant details or information about the section.",
                    className="section-description",
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([tabs_compare, html.Div(id="tabs-content")], md=12),
                dbc.Col([dcc.Dropdown(id="image-dropdown", options=get_dropdown_options(), value=0)], md=4),
                dbc.Col([html.Img(id="selected-image", style={"width": "100%"})], md=8),
            ]
        ),

        html.Div(className="border-line"),
        dbc.Row(
            [
                html.H2(
                    "Linear metabolite gradient across colorectal subsites 4",
                    className="section-heading",
                    id="section4",
                ),
                html.P(
                    "Your description goes here. Provide relevant details or information about the section.",
                    className="section-description",
                ),
                dbc.Col(
                    [
                        html.Label(
                            "Select Compound mz Linear:",
                            id="mz-linear-section",
                            className="select-label",
                        ),
                        dcc.Dropdown(
                            id="compound-dropdown-linear",
                            options=[
                                {"label": mz, "value": mz}
                                for mz in list(get_cecum_and_ascending_mz_values(["tumor_linear_plots", "normal_linear_plots"]))
                            ],
                            placeholder="Select Mz Value",
                            searchable=True,
                            clearable=True,
                            multi=False,
                            style={"width": "100%"},
                            className="select-input",
                            value=list(get_cecum_and_ascending_mz_values(
                                ["tumor_linear_plots", "normal_linear_plots"]))[0],
                        ),
                        html.Div(id="selected-mz-linear-value"),
                    ],
                    md=12,
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="outer-container-loading",
                            type="circle",
                            children=[
                                html.Div(
                                    [
                                        dcc.Graph(
                                            id="tumor-linear-plot",
                                            className="tumor-linear-plot",
                                        ),
                                        dcc.Graph(
                                            id="normal-linear-plot",
                                            className="normal-linear-plot",
                                        ),
                                    ],
                                    style={"display": "flex"},
                                    className="outer-container with-shadow",
                                ),
                            ],
                        ),
                    ],
                    md=12,
                ),
            ]
        ),
        html.Div(className="border-line"),
        dbc.Row(
            [
                html.H2(
                    "Section 5 : Survival Metabolite Marker Comparison Across Colorectal Subsites",
                    className="section-heading",
                    id="section5",
                ),
                html.P(
                    "Your description goes here. Provide relevant details or information about the section.",
                    className="section-description",
                ),
            ]),
        html.Div(className="border-line"),

        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            id="loading",
                            className="loading",
                            type="circle",
                            children=[html.Div(id="loading-output")],
                        ),
                    ],
                    md=12,
                ),
            ]
        ),
    ],
    fluid=True,
)
