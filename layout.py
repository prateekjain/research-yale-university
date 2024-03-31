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
    get_linear_values,
    get_dropdown_options,
    get_q05_mz_forest_values
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

tabs_survival = dcc.Tabs(
    [
        dcc.Tab(
            label="All Metabolites",
            value="all-meta",
            children=[
                dbc.Col(
                    [
                        html.Label(
                            "Select Forest Plot mx:",
                            id="mz-forest-section",
                            className="select-label",
                        ),
                        dcc.Dropdown(
                            id="compound-dropdown-forest",
                            options=[
                                {"label": mz, "value": mz}
                                for mz in get_mz_values("forest_plot")
                            ],

                            placeholder="Select Mz Value",
                            searchable=True,
                            multi=False,
                            style={"width": "100%"},
                            className="select-input",
                            value=get_mz_values("forest_plot")[0],
                        ),
                        html.Div(id="selected-mz-forest-value"),
                    ],
                    md=12,
                ),
                dcc.Loading(
                    id="outer-container-loading",
                    type="circle",
                    children=[
                        html.Div(
                            [
                                html.Img(
                                    id='forest-plot-image',
                                    className="forest-plot",
                                    style={'width': '60%',
                                           'height': '40%',
                                           'align-item': 'center', }
                                )
                            ],
                            style={"display": "flex"},
                            className="outer-container with-shadow",
                        ),
                    ],
                ),
            ]
        ),
        dcc.Tab(
            label="Subsites specific survival markers",
            value="less-subsites",
            children=[
                dbc.Col(
                    [
                        html.Label(
                            "Select Subsites Specific Survival:",
                            id="mz-forest-specific-section",
                            className="select-label",
                        ),
                        dcc.Dropdown(
                            id="compound-dropdown-forest-specific",
                            options=[
                                {"label": mz, "value": mz}
                                for mz in get_q05_mz_forest_values()
                            ],

                            placeholder="Select Mz Value",
                            searchable=True,
                            multi=False,
                            style={"width": "100%"},
                            className="select-input",
                            value=list(get_q05_mz_forest_values())[0],
                        ),
                        html.Div(id="selected-mz-forest-specific-value"),
                    ],
                    md=12,
                ),
                dcc.Loading(
                    id="outer-container-loading",
                    type="circle",
                    children=[
                        html.Div(
                            [
                                html.Img(
                                    id='forest-specific-plot-image',
                                    className="forest-plot",
                                    style={'width': '60%',
                                           'height': '40%',
                                           'align-item': 'center', }

                                )
                            ],
                            style={"display": "flex"},
                            className="outer-container with-shadow",
                        ),
                    ],
                ),
            ]
        ),
        dcc.Tab(
            label="RCC or LCC or Rectum",
            value="survival-rcc-lcc-rectum",
            children=[

            ]
        )
    ],
    id="tabs_survival",
    value="all-meta",
    className="tabs",
)
study_info_dropdown = html.Div(
    className='dropdown',
    children=[
        html.Button('Study Information', className='dropbtn'),
        html.Div(
            className='dropdown-content',
            children=[
                html.Div(
                    className='row',
                    children=[
                        dbc.Col(
                            [
                                html.Div(
                                    className='column left-column',
                                    children=[
                                        html.H3(
                                            'Sample Cohort Information', id='sample-cohort'),
                                        html.H3(
                                            'Sample Preparation and LC-MS Analysis', id='sample-preparation'),
                                        html.H3(
                                            'Metabolic Feature Identification', id='metabolic-feature'),
                                        html.H3(
                                            'Link to Publication and Citing the Database', id='link-to-publication'),
                                        html.H3(
                                            'Project and Funding Information', id='project-funding'),
                                    ]
                                )
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.Div(
                                    className='column right-column',
                                    children=[
                                        html.Div(id='sample-cohort-info', className='content hidden',
                                                 children=[
                                                     html.P("Patient-matched tumor tissues and normal mucosa tissues (collected furthest away from tumor within the subsite) were surgically removed during colectomy for colorectal cancer in the operating room at Memorial Sloan Kettering Cancer Center (MSKCC), New York, NY, USA, frozen immediately in liquid nitrogen and stored at -80oC before analysis. Sample were collected in 1991-2001. The Yale University Institutional Review Board (IRB) determined that the study conducted in this publication was not considered to be Human Subjects Research and did not require an IRB review (IRB/HSC# 1612018746). Patient characteristics can be found in supplementary table 1 in our publication: (link).")
                                                 ]),
                                        html.Div(id='sample-preparation-info', className='content hidden',
                                                 children=[
                                                     html.P("Detailed sample preparation and LC-MS information can be found in our publication here (link). The data displayed in this database was acquired from the analysis of patient-matched tumor tissues and normal mucosa using a UPLC-ESI-QTOFMS (H-Class ACQUITY and Xevo G2-XS; Waters Corporation, Milford, MA, USA) was used for MS data acquisitionby RPLC ESI positive and HILIC ESI negative mode. We chose to make our data available in the format of this database, other data requests, along with protocols and codes can be made by email, please see contact us section.")
                                                 ]),
                                        html.Div(id='metabolic-feature-info', className='content hidden',
                                                 children=[
                                                     html.P("In this database we have displayed all metabolite features generated from the analysis of the tumor tissues and normal mucosa tissues, by electrospray ionization (ESI) mode; negative or positive. These features are displayed in Section 1. For subsequent sections we only display annotated metabolites. The level of annotation is defined by the metabolomics standards initiative (MSI) levels; Level 1:…….Level 2:…….Level 3:……..Metabolite identification methods are published in Jain. Et al…..(paper under submission).")
                                                 ]),
                                        html.Div(id='link-to-publication-info', className='content hidden',
                                                 children=[
                                                     html.P(
                                                         "Please cite the following: Jain A,...paper details here")
                                                 ]),
                                        html.Div(id='project-funding-info', className='content hidden',
                                                 children=[
                                                     html.P(
                                                         "The data acquired in this database was supported by funding from the American Cancer Society awarded to Caroline Johnson, and the Yale Center for Clinical Investigation awarded to Abhishek Jain.")
                                                 ]),
                                    ]
                                )
                            ],
                            width=6
                        ),
                    ]
                )
            ]
        )
    ]
)


mega_menu = html.Div(
    className='navbar',
    children=[
        html.Div(
            className='dropdown',
            children=[
                study_info_dropdown,
            ]
        )
    ]
)

main_layout = dbc.Container(
    [
        html.Div(
            className='header-bar',
            children=[
                mega_menu,
            ]
        ),
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
                                            "Tumor vs Normal (Metabolite features)",
                                            id="btn-mz-h",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section1",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Tumor vs Normal (Annotated Metabolites)",
                                            id="btn-mz-Mucosa2",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section2",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Inter-subsite comparisons",
                                            id="btn-inter-subsite",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section3",
                                        ),

                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Concentration gradient of metabolites",
                                            id="btn-mz-linear",
                                            n_clicks=0,
                                            className="btn-section btn-center",
                                            href="#section4",
                                        ),
                                        html.Span("|", className="divider"),
                                        html.A(
                                            "Survival markers",
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
                    "Tumor vs. Normal Mucosa Metabolic features Comparison Across Subsites",
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
                    "Tumor vs. Normal Mucosa Metabolite Comparison Across Subsites",
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
                    "Inter-subsite metabolites comparisons",
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
                dbc.Col([dcc.Dropdown(id="image-dropdown", className="select-input",
                                      options=get_dropdown_options(),
                                      value=get_dropdown_options()[0]["value"])], md=4),
                dbc.Col([
                    html.Div([
                        html.Img(id="selected-image", style={"width": "80%"}),
                    ], id="selected-image-container")
                ], md=8),
            ]
        ),

        html.Div(className="border-line"),
        dbc.Row(
            [
                html.H2(
                    "Linear metabolite gradient across colorectal subsites",
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
                                for mz in list(get_linear_values(["tumor_linear_plots", "normal_linear_plots"]))
                            ],
                            placeholder="Select Mz Value",
                            searchable=True,
                            clearable=True,
                            multi=False,
                            style={"width": "100%"},
                            className="select-input",
                            value=list(get_linear_values(
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
                    "Survival Metabolite Marker Comparison Across Colorectal Subsites",
                    className="section-heading",
                    id="section5",
                ),
                html.P(
                    "Your description goes here. Provide relevant details or information about the section.",
                    className="section-description",
                ),

            ]),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Col([tabs_survival, html.Div(
                            id="tabs-content")], md=12),

                    ],
                    md=12,
                ),
            ]
        ),
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
