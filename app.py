import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2
from dotenv import load_dotenv
from plotly.subplots import make_subplots
import os

load_dotenv()
# Function to fetch mz values from the database
db_url = os.getenv('DATABASE_URL')
print(db_url)

connection = psycopg2.connect(db_url)
cursor = connection.cursor()

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]


def get_mz_values():
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    query_mz_values = "SELECT DISTINCT mz FROM mz_value"
    cursor.execute(query_mz_values)
    mz_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return mz_values

# Function to fetch data from the database based on selected mz_value


def get_meta_values():
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    query_meta_values = "SELECT DISTINCT Metabolite FROM tumor_tumor_compare"
    cursor.execute(query_meta_values)
    meta_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return meta_values


def get_case_columns_query(table_name, selected_mz):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    # # Get all column names from the table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    # print(all_columns)
    # Construct the SQL query dynamically
    query_case = f"SELECT {', '.join([col for col in all_columns if '_case' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
    query_control = f"SELECT {', '.join([col for col in all_columns if '_control' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
    get_side_val = f"SELECT q_fdr, log_fc_matched FROM {table_name} WHERE mz = {selected_mz}"
    # print("query_case" ,query_case)
    # print("query_control", query_control)

    cursor.execute(query_case)
    case_results = cursor.fetchall()
    print(case_results)

    cursor.execute(query_control)
    control_results = cursor.fetchall()
    print(control_results)

    cursor.execute(get_side_val)
    final_get_side_val = cursor.fetchall()
    print(final_get_side_val)

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return case_results, control_results, final_get_side_val


def get_case_columns_vs_query(columName, selected_meta):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    table_name = "tumor_tumor_compare"

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    print("all_columns", all_columns)
    query_case = f"SELECT {', '.join([col for col in all_columns if f'case_{columName}_' in col.lower() and 'vs' not in col.lower()])} FROM {table_name} WHERE metabolite = '{selected_meta}'"

    cursor.execute(query_case)
    case_results = cursor.fetchall()

    case_values = [item for sublist in case_results for item in sublist]
    # Close the cursor and connection
    cursor.close()
    connection.close()

    return case_results


def vs_columnNames(table_name, fig, selected_meta):
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    col_vs = []

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    query_q_vs = f"SELECT {', '.join([col for col in all_columns if 'vs' in col.lower()])} FROM {table_name} WHERE metabolite = '{selected_meta}'"
    cursor.execute(query_q_vs, (selected_meta,))
    query_q_vs_result = cursor.fetchall()
    print(query_q_vs_result)

    for col in all_columns:
        if 'vs' in col.lower():
            col_vs.append(col)
    # print(col_vs)
    index = 0
    vpos = 0.69
    hpos = 0.7
    for i in range(len(region)):
        for j in range(i+1, len(region)):
            vs_value_name = "case_"+region[i]+"_vs_case_"+region[j]
            vs_value_name_neg = "case_"+region[j]+"_vs_case_"+region[i]
            print("vpos", vpos, hpos)

            if vs_value_name in col_vs:
                vs_value = col_vs.index(vs_value_name)
                print(query_q_vs_result[0][vs_value])
                qFdr = query_q_vs_result[0][vs_value]
                print("exist_", i)

                if qFdr < 0.001:
                    qFdrStars = '***'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)
                elif qFdr < 0.01:
                    qFdrStars = '**'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.05:
                    qFdrStars = '*'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)

                # add_comparison_lines(fig, [region[i], region[j]], [
                #                      0.78+index, 0.8+index], symbol=qFdrStars)
            elif vs_value_name_neg in col_vs:
                vs_value = col_vs.index(vs_value_name_neg)
                print(query_q_vs_result[0][vs_value])
                print("exist_", i)
                qFdr = query_q_vs_result[0][vs_value]
                if qFdr < 0.001:
                    qFdrStars = '***'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.01:
                    qFdrStars = '**'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.05:
                    qFdrStars = '*'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)
    cursor.close()
    connection.close()


external_stylesheets = ['styles.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Define the layout of the app
app.layout = html.Div([
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
        options=[{'label': mz, 'value': mz} for mz in get_mz_values()],
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

# Define callback to update the scatter plot based on dropdown selections


@app.callback(
    [Output(f'scatter-plot-{i}', 'figure') for i in range(7)],
    [Input('compound-dropdown', 'value')]
)
def tumor_vs_normal_plots(selected_compound):
    if selected_compound is not None:
        # Fetch and process data based on selected values
        # Assuming you have a column named "mz" in your tables
        selected_mz = float(selected_compound)

        figures = []

        for i in range(len(region)):
            # Fetch data from the database
            query_case, query_control, final_get_side_val = get_case_columns_query(
                region[i], selected_mz)
            query_case = list(query_case[0])
            query_control = list(query_control[0])
            final_get_side_val = list(final_get_side_val[0])

            qFdr = final_get_side_val[0]

            if qFdr < 0.001 and qFdr > 0.01:
                qFdrStars = '***'
            elif qFdr < 0.01 and qFdr > 0.05:
                qFdrStars = '**'
            elif qFdr < 0.05:
                qFdrStars = '*'
            else:
                qFdrStars = 'NA'

            # Create a scatter plot
            scatter_plot = make_subplots()

            # Add box plots for columns with '_case'
            scatter_plot.add_trace(go.Box(
                x=['Tumor'] * len(query_case),
                y=query_case,
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color='rgba(255, 0, 0, 1)'),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
                name='Tumor',
            ))

            # Add a box plot for 'Control' values
            scatter_plot.add_trace(go.Box(
                x=['Normal'] * len(query_control),
                y=query_control,
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color='rgba(0, 255, 0, 0.8)'),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
            ))

            scatter_plot.update_xaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
                gridcolor='lightgrey'
            )
            scatter_plot.update_yaxes(
                mirror=True,
                ticks='outside',
                showline=True,
                linecolor='black',
                gridcolor='lightgrey'
            )

            # Customize layout
            name = region[i]
            scatter_plot.update_layout(
                width=300,
                height=500,
                xaxis=dict(
                    title=dict(
                        text=f'<b>{name}</b>',
                        font=dict(
                            size=14, family='Arial, sans-serif', color='black')
                    ),
                    tickangle=90,
                ),
                yaxis=dict(
                    title='Relative Abundance',
                ),
                plot_bgcolor='white',
                annotations=[
                    dict(
                        x=1.57,
                        y=0.94,
                        xref='paper',
                        yref='paper',
                        text=f"q:{qFdrStars}<br>LogFC:{final_get_side_val[1]:.2f}",
                        align='left',
                        showarrow=False,
                        font={
                            'size': 12,
                            'color': 'black',
                        },
                        bordercolor='black',
                        borderwidth=1
                    )
                ]
            )

            figures.append(scatter_plot)

        # Show the graph container
        return figures
    else:
        # If dropdown is not selected, hide the container
        return [go.Figure()] * 7

# Callback to update the displayed mz value


@app.callback(
    Output('tumor-plot', 'figure'),
    Output('normal-plot', 'figure'),
    [Input('compound-dropdown', 'value')]
)
def tumor_normal_plot(selected_compound):
    if selected_compound is not None:
        # Fetch and process data based on selected values
        selected_mz = float(selected_compound)
        query_tumor_regions = []
        query_normal_regions = []

        # Define a list of colors for each region
        region_colors = {
            "cecum": 'aliceblue',
            "ascending": 'blue',
            "transverse": 'cyan',
            "descending": 'mistyrose',
            "sigmoid": 'yellow',
            "rectosigmoid": 'brown',
            "rectum": 'pink',
        }

        for i in range(len(region)):
            query_case, query_control, final_get_side_val = get_case_columns_query(
                region[i], selected_mz)
            query_case = list(query_case[0])
            query_control = list(query_control[0])
            query_tumor_regions.extend(query_case)
            query_normal_regions.extend(query_control)

        tumor_plot_all_regions = make_subplots()
        for i in range(len(region)):
            # Create a separate trace for each region with different color
            x_values = [f'{region[i]}' for _ in range(
                len(query_tumor_regions)//len(region))]
            tumor_plot_all_regions.add_trace(go.Box(
                x=x_values,
                y=query_tumor_regions[i*len(x_values):(i+1)*len(x_values)],
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color=region_colors[region[i]]),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
                name='Tumor',
            ))

        # Update layout for tumor plot
        tumor_plot_all_regions.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        tumor_plot_all_regions.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        tumor_plot_all_regions.update_layout(
            width=600,
            height=500,
            xaxis=dict(
                title=dict(
                    text=f'<b>All Regions Tumor</b>',
                    font=dict(
                        size=14, family='Arial, sans-serif', color='black')
                ),
                tickangle=90,
            ),
            yaxis=dict(
                title='Relative Abundance',
            ),
            plot_bgcolor='white',
        )

        normal_plot_all_regions = make_subplots()
        for i in range(len(region)):
            # Create a separate trace for each region with different color
            x_values = [f'{region[i]}' for _ in range(
                len(query_normal_regions)//len(region))]
            normal_plot_all_regions.add_trace(go.Box(
                x=x_values,
                y=query_normal_regions[i*len(x_values):(i+1)*len(x_values)],
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color=region_colors[region[i]]),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
                name='Normal',
            ))

        # Update layout for normal plot
        normal_plot_all_regions.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        normal_plot_all_regions.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        normal_plot_all_regions.update_layout(
            width=600,
            height=500,
            xaxis=dict(
                title=dict(
                    text=f'<b>All Regions Normal</b>',
                    font=dict(
                        size=14, family='Arial, sans-serif', color='black')
                ),
                tickangle=90,
            ),
            yaxis=dict(
                title='Relative Abundance',
            ),
            plot_bgcolor='white',
        )

        # Show the graph containers
        return tumor_plot_all_regions, normal_plot_all_regions
    else:
        # If dropdown is not selected, hide the containers
        return go.Figure(), go.Figure()


@app.callback(
    Output('selected-mz-value', 'children'),
    [Input('compound-dropdown', 'value')]
)
def update_selected_mz_value(selected_mz):
    if selected_mz:
        return f"Selected Mz Value: {selected_mz}"
    else:
        return ""


def add_comparison_lines(fig, regions, y_range, symbol):
    fig.add_shape(
        type="line",
        xref="x",
        yref="paper",
        x0=regions[0],
        y0=y_range[0],
        x1=regions[0],
        y1=y_range[1],
        line=dict(color="black", width=0.5),
    )
    fig.add_shape(
        type="line",
        xref="x",
        yref="paper",
        x0=regions[0],
        y0=y_range[1],
        x1=regions[1],
        y1=y_range[1],
        line=dict(color="black", width=0.5),
    )
    fig.add_shape(
        type="line",
        xref="x",
        yref="paper",
        x0=regions[1],
        y0=y_range[1],
        x1=regions[1],
        y1=y_range[0],
        line=dict(color="black", width=0.5),
    )

    bar_xcoord_map = {x: idx for idx, x in enumerate(region)}
    fig.add_annotation(
        dict(
            font=dict(color="black", size=14),
            x=(bar_xcoord_map[regions[0]] + bar_xcoord_map[regions[1]]) / 2,
            y=y_range[1] * 1.04,
            showarrow=False,
            text=symbol,
            textangle=0,
            xref="x",
            yref="paper",
        )
    )


@app.callback(
    Output('tumor-comparable-plot', 'figure'),
    Output('normal-comparable-plot', 'figure'),
    [Input('compound-dropdown-compare', 'value')]
)
def tumor_normal_comparable_plot(selected_compound):
    if selected_compound is not None:
        # Fetch and process data based on selected values
        selected_meta = selected_compound
        table_name = "tumor_tumor_compare"
        query_tumor_regions = []
        query_normal_regions = []
        # vs_columnNames(selected_meta)
        # Define a list of colors for each region
        region_colors = {
            "cecum": 'gold',
            "ascending": 'blue',
            "transverse": 'cyan',
            "descending": 'mistyrose',
            "sigmoid": 'yellow',
            "rectosigmoid": 'brown',
            "rectum": 'pink',
        }

        for i in region:
            print(i)
            print('\n')
            query_case = get_case_columns_vs_query(i, selected_meta)
            query_case = list(query_case[0])

            # print(query_case)

            # query_control = list(query_control[0])
            query_tumor_regions.extend(query_case)
            # print(query_tumor_regions)
            # query_normal_regions.extend(query_control)

        tumor_plot_comparable_all_regions = make_subplots()
        for i in range(len(region)):
            # Create a separate trace for each region with different color
            x_values = [f'{region[i]}' for _ in range(
                len(query_tumor_regions)//len(region))]
            tumor_plot_comparable_all_regions.add_trace(go.Box(
                x=x_values,
                y=query_tumor_regions[i*len(x_values):(i+1)*len(x_values)],
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color=region_colors[region[i]]),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
                name='Tumor',
            ))

        # Update layout for tumor plot
        tumor_plot_comparable_all_regions.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        tumor_plot_comparable_all_regions.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        tumor_plot_comparable_all_regions.update_layout(
            width=600,
            height=600,
            xaxis=dict(
                title=dict(
                    text=f'<b>All Regions Comparable Tumor</b>',
                    font=dict(
                        size=14, family='Arial, sans-serif', color='black')
                ),
                tickangle=90,
            ),
            yaxis=dict(
                title='Relative Abundance',
            ),
            plot_bgcolor='white',
        )
        vs_columnNames(
            table_name, tumor_plot_comparable_all_regions, selected_meta)

        normal_plot_comparable_all_regions = make_subplots()
        for i in range(len(region)):
            # Create a separate trace for each region with different color
            x_values = [f'{region[i]}' for _ in range(
                len(query_normal_regions)//len(region))]
            normal_plot_comparable_all_regions.add_trace(go.Box(
                x=x_values,
                y=query_normal_regions[i*len(x_values):(i+1)*len(x_values)],
                boxpoints='all',
                fillcolor='white',
                line=dict(color='black'),
                marker=dict(color=region_colors[region[i]]),
                jitter=0.1,
                pointpos=0,
                showlegend=False,
                name='Normal',
            ))

        # Update layout for normal plot
        normal_plot_comparable_all_regions.update_xaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        normal_plot_comparable_all_regions.update_yaxes(
            mirror=True,
            ticks='outside',
            showline=True,
            linecolor='black',
            gridcolor='lightgrey'
        )
        normal_plot_comparable_all_regions.update_layout(
            width=600,
            height=500,
            xaxis=dict(
                title=dict(
                    text=f'<b>All Regions Comparable Normal</b>',
                    font=dict(
                        size=14, family='Arial, sans-serif', color='black')
                ),
                tickangle=90,
            ),
            yaxis=dict(
                title='Relative Abundance',
            ),
            plot_bgcolor='white',
        )

        # Show the graph containers
        return tumor_plot_comparable_all_regions, normal_plot_comparable_all_regions
    else:
        # If dropdown is not selected, hide the containers
        return go.Figure(), go.Figure()


@app.callback(
    Output('selected-meta-value', 'children'),
    [Input('compound-dropdown-compare', 'value')]
)
def update_selected_meta_value(selected_meta):
    if selected_meta:
        return f"Selected meta Value: {selected_meta}"
    else:
        return ""


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
