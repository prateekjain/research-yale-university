import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import psycopg2

db_params = {
    'dbname': 'researchDB',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

# Function to fetch mz values from the database


def get_mz_values():
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    query_mz_values = "SELECT DISTINCT mz FROM mz_value"
    cursor.execute(query_mz_values)
    mz_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return mz_values

# Function to fetch data from the database based on selected mz_value


def get_data(selected_mz):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Fetch data from the "asceding" table
    query_asceding = f"SELECT * FROM asceding WHERE mz = {selected_mz}"
    cursor.execute(query_asceding)
    asceding_data = cursor.fetchall()

    # Fetch data from the "asceding_output" table
    query_asceding_output = f"SELECT * FROM asceding_output WHERE mz = {selected_mz}"
    cursor.execute(query_asceding_output)
    asceding_output_data = cursor.fetchall()

    # Get column names for "asceding" table
    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = 'asceding'")
    asceding_columns = [row[0] for row in cursor.fetchall()]

    # Get column names for "asceding_output" table
    cursor.execute(
        f"SELECT column_name FROM information_schema.columns WHERE table_name = 'asceding_output'")
    asceding_output_columns = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    print("asceding_data:")
    print(asceding_data)
    print("asceding_output_data:")
    print(asceding_output_data)

    print("\nColumn names for asceding table:")
    print(asceding_columns)

    print("\nColumn names for asceding_output table:")
    print(asceding_output_columns)

    return asceding_data, asceding_output_data


# Initialize the Dash app
app = dash.Dash(__name__)
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

    html.Label("Select Compound:"),
    dcc.Dropdown(
        id='compound-dropdown',
        options=[{'label': mz, 'value': mz} for mz in get_mz_values()],
        placeholder="Select Mz Value",
        multi=False,
        style={'width': '50%'}
    ),
    html.Div(id='selected-mz-value'),

    # Scatter plot
    dcc.Graph(id='scatter-plot'),

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
    [Output('scatter-plot', 'figure'),
     Output('loading-output', 'children')],
    [Input('compound-dropdown', 'value')]
)
def update_scatter_plot(selected_compound):
    loading_message = None

    if selected_compound is not None:
        # Fetch and process data based on selected values
        loading_message = f"Fetching data for Compound {selected_compound}..."

        # Assuming you have a column named "mz" in your tables
        selected_mz = float(selected_compound)

        # Fetch data from the database
        asceding_data, asceding_output_data = get_data(selected_mz)

        # Create a DataFrame from the fetched data
        # print(pd.DataFrame(asceding_data))
        # print(pd.DataFrame(asceding_output_data))

        df_asceding = pd.DataFrame(
            asceding_data, columns=['col1', 'col2', 'mz'])
        df_asceding_output = pd.DataFrame(
            asceding_output_data, columns=['col1', 'col2', 'mz'])

        # Create a scatter plot
        scatter_plot = go.Figure()

        # Add box plots for columns with '_case'
        for column_name in df_asceding.columns:
            if '_case' in column_name:
                scatter_plot.add_trace(go.Box(
                    x=['Tumor'],
                    y=df_asceding[column_name],
                    boxpoints='all',
                    marker=dict(color='rgba(255, 0, 0, 0.5)'),
                    jitter=0.3,
                    pointpos=0,
                    name=column_name,
                ))

        # Add box plots for columns with '_control'
        for column_name in df_asceding_output.columns:
            if '_control' in column_name:
                scatter_plot.add_trace(go.Box(
                    x=['Normal'],
                    y=df_asceding_output[column_name],
                    boxpoints='all',
                    marker=dict(color='rgba(0, 255, 0, 0.5)'),
                    jitter=0.3,
                    pointpos=0,
                    name=column_name,
                ))

        # Customize layout
        scatter_plot.update_layout(
            title=f'Scatter Plot - asceding - MZ: {selected_mz}',
            width=800,
            height=500,
            xaxis=dict(
                title=dict(
                    text=f'<b>{selected_mz}</b>',
                    font=dict(size=14, family='Arial, sans-serif',
                              color='black')
                ),
                tickangle=90,
                line=dict(color='black', width=0.5)
            ),
            yaxis=dict(
                title='Relative Abundance',
                line=dict(color='black', width=0.5)
            )
        )

        return scatter_plot, loading_message
    else:
        # If dropdown is not selected, return an empty plot
        return go.Figure(), None

# Callback to update the displayed mz value


@app.callback(
    Output('selected-mz-value', 'children'),
    [Input('compound-dropdown', 'value')]
)
def update_selected_mz_value(selected_mz):
    if selected_mz:
        return f"Selected Mz Value: {selected_mz}"
    else:
        return ""


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
