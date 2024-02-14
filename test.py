from scipy import stats
import plotly.express as px
import plotly.graph_objects as go

tips = px.data.tips()
# stats.ttest_ind(tips[tips['day']=='Thur'].total_bill,tips[tips['day']=='Fri'].total_bill)
# stats.ttest_ind(tips[tips['day']=='Thur'].total_bill,tips[tips['day']=='Sat'].total_bill)

fig = go.Figure()
for day in ['Thur', 'Fri', 'Sat', 'Sun']:
    fig.add_trace(go.Box(
        y=tips[tips['day'] == day].total_bill,
        name=day,
        boxpoints='outliers'
    ))


def add_pvalue_annotation(days, y_range, symbol=''):
    """
    arguments:
    days --- a list of two different days e.g. ['Thur','Sat']
    y_range --- a list of y_range in the form [y_min, y_max] in paper units
    """
    pvalue = stats.ttest_ind(
        tips[tips['day'] == days[0]].total_bill,
        tips[tips['day'] == days[1]].total_bill)[1]
    # print(pvalue)
    if pvalue >= 0.05:
        symbol = 'ns'
    if pvalue < 0.05:
        symbol = '*'

    fig.add_shape(type="line",
                  xref="x", yref="paper",
                  x0=days[0], y0=y_range[0], x1=days[0], y1=y_range[1],
                  line=dict(
                      color="black",
                      width=2,
                  )
                  )
    fig.add_shape(type="line",
                  xref="x", yref="paper",
                  x0=days[0], y0=y_range[1], x1=days[1], y1=y_range[1],
                  line=dict(
                      color="black",
                      width=2,
                  )
                  )
    fig.add_shape(type="line",
                  xref="x", yref="paper",
                  x0=days[1], y0=y_range[1], x1=days[1], y1=y_range[0],
                  line=dict(
                      color="black",
                      width=2,
                  )
                  )
    # add text at the correct x, y coordinates
    # for bars, there is a direct mapping from the bar number to 0, 1, 2...
    bar_xcoord_map = {x: idx for idx, x in enumerate(
        ['Thur', 'Fri', 'Sat', 'Sun'])}
    fig.add_annotation(dict(font=dict(color="black", size=14),
                            x=(bar_xcoord_map[days[0]] +
                               bar_xcoord_map[days[1]])/2,
                            y=y_range[1]*1.01,
                            showarrow=False,
                            text=symbol,
                            textangle=0,
                            xref="x",
                            yref="paper"
                            ))


add_pvalue_annotation(['Fri', 'Sun'], [1.01, 1.02])
add_pvalue_annotation(['Thur', 'Sat'], [1.05, 1.06])

# fig.show()

# Save the plot as an image (PNG format)
fig.write_image("box_plot_with_pvalues.png")


# from sqlalchemy import select
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import pandas as pd
# import plotly.graph_objs as go
# import psycopg2
# from dotenv import load_dotenv
# import os

# load_dotenv()
# # Function to fetch mz values from the database
# db_url = os.getenv('DATABASE_URL')
# print(db_url)


# def get_case_columns_query(table_name, selected_mz):
#     # Connect to the database
#     connection = psycopg2.connect(db_url)
#     cursor = connection.cursor()

#     # Get all column names from the table
#     cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
#     all_columns = [desc[0] for desc in cursor.description]
#     print(all_columns)
#     # Construct the SQL query dynamically
#     query_case = f"SELECT {', '.join([col for col in all_columns if '_case' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"
#     query_control = f"SELECT {', '.join([col for col in all_columns if '_control' in col.lower()])} FROM {table_name} WHERE mz = {selected_mz}"

#     # print(query_case)
#     # print(query_control)
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()

#     return query_case, query_control


# selected_mz = '157.01199'  # replace with your actual value
# table_name = 'asceding_output'  # replace with your actual table name

# # Get the dynamic query
# query_case, query_control = get_case_columns_query(table_name, selected_mz)

# # Connect to the database
# connection = psycopg2.connect(db_url)
# cursor = connection.cursor()

# # Execute the query
# cursor.execute(query_case, (selected_mz,))
# cursor.execute(query_control, (selected_mz,))

# result = cursor.fetchall()

# # Print or process the query result
# print(result)

# # Close the cursor and connection
# cursor.close()
# connection.close()
