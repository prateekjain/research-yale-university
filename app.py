import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
# Function to fetch mz values from the database
db_url = os.getenv('DATABASE_URL')
print(db_url)

connection = psycopg2.connect(db_url)
cursor = connection.cursor()


def get_mz_values():

    query_mz_values = "SELECT DISTINCT mz FROM mz_value"
    cursor.execute(query_mz_values)
    mz_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return mz_values

# Function to fetch data from the database based on selected mz_value
def get_case_columns_query(table_name, selected_mz):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    # Get all column names from the table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    # print(all_columns)
    # Construct the SQL query dynamically
    query_case = f"SELECT {', '.join([col for col in all_columns if '_case' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
    query_control = f"SELECT {', '.join([col for col in all_columns if '_control' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"

    # print("query_case" ,query_case)
    # print("query_control", query_control)
    cursor.execute(query_case, (selected_mz,))
    case_results = cursor.fetchall()

    cursor.execute(query_control, (selected_mz,))
    control_results = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return case_results, control_results

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
        # print("hello")
        # Fetch data from the database
        query_case, query_control = get_case_columns_query(
            "asceding_output", selected_mz)
        query_case = list(query_case[0])
        query_control = list(query_control[0])

        # print("asceding_data", query_case)
        # print("asceding_data1", type(query_case[0][0]))
        # print(query_case[0][0])

        # print("asceding_data1", query_control)

        # Create a scatter plot
        scatter_plot = go.Figure()

        # Add box plots for columns with '_case'
        # for i, case_value in enumerate(query_case[1:]):
        scatter_plot.add_trace(go.Box(
            x=['Tumor'] * len(query_case),
            y=query_case,
            boxpoints='all',
            marker=dict(color='rgba(255, 0, 0, 0.5)'),
            jitter=0.3,
            pointpos=0,
            showlegend=False,

            name='Tumor',
        ))

        # Add a box plot for 'Control' values
        scatter_plot.add_trace(go.Box(
            x=['Normal'] * len(query_control),
            y=query_control,
            boxpoints='all',
            marker=dict(color='rgba(0, 255, 0, 0.5)'),
            jitter=0.3,
            pointpos=0,
            showlegend=False,
            name='Control',
        ))

        # Customize layout
        scatter_plot.update_layout(
            title=f'Scatter Plot - asceding - MZ: {selected_mz}',
            width=300,
            height=500,
            xaxis=dict(
                title=dict(
                    text=f'<b>asceding</b>',
                    font=dict(size=14, family='Arial, sans-serif',
                              color='black')
                ),
                tickangle=90,
                # line=dict(color='black', width=0.5)
            ),
            yaxis=dict(
                title='Relative Abundance',
                # line=dict(color='black', width=0.5)
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
