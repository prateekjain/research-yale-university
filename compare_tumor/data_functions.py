# data_functions.py
import os
import psycopg2
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from dotenv import load_dotenv

all_columns = []

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

load_dotenv()
db_url = os.getenv('DATABASE_URL')


# add table name and column names for the function
def get_mz_values(table_name):
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    query_mz_values = f"SELECT DISTINCT mz FROM {table_name}"
    cursor.execute(query_mz_values)
    mz_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()
    print("mzval", mz_values[1])
    return mz_values


# def get_subsite_mz_values(subsite):
#     # Fetch Mz values for a specific subsite with q < 0.05
#     mz_values = Metabolite.objects.filter(
#         subsite=subsite, q_value__lt=0.05).values_list('mz_field', flat=True)
#     return list(mz_values)

# Define other filter functions as needed for the remaining filters


def get_cecum_and_ascending_mz_values(regions):
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    # Initialize an empty set to store the Mz values
    mz_values_set = set()

    # Loop through each region and dynamically generate the SQL query
    for region in regions:
        # SQL query to get Mz values with q_fdr < 0.05 in the specified region
        query = f"SELECT DISTINCT mz FROM {region} WHERE q_fdr <= 0.05"
        cursor.execute(query)
        region_mz_values = {row[0] for row in cursor.fetchall()}

        # If it's the first region, set the Mz values directly
        if not mz_values_set:
            mz_values_set = region_mz_values
        else:
            # If it's not the first region, take the intersection with the existing Mz values
            mz_values_set &= region_mz_values

    connection.close()
    return mz_values_set





def get_case_columns_query(table_name, selected_mz):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    # # Get all column names from the table
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    # print(all_columns)
    # Construct the SQL query dynamically
    query_case = f"SELECT {', '.join([col for col in all_columns if '_case' in col.lower()])} FROM {table_name} WHERE mz = '{selected_mz}'"
    query_control = f"SELECT {', '.join([col for col in all_columns if '_control' in col.lower()])} FROM {table_name} WHERE mz = '{selected_mz}'"
    get_side_val = f"SELECT q_fdr, log_fc_matched FROM {table_name} WHERE mz = '{selected_mz}'"
    # print("query_case" ,query_case)
    # print("query_control", query_control)

    cursor.execute(query_case)
    case_results = cursor.fetchall()
    print("heelooo5",case_results)

    cursor.execute(query_control)
    control_results = cursor.fetchall()
    print("heelooo4",control_results)

    cursor.execute(get_side_val)
    final_get_side_val = cursor.fetchall()
    print("heelooo6",final_get_side_val)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("heelooo7",case_results, control_results, final_get_side_val)
    return case_results, control_results, final_get_side_val


def get_case_columns_vs_query(columName, selected_mz, table_name):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    # print("all_columns", all_columns)
    query_case = f"SELECT {', '.join([col for col in all_columns if f'case_{columName}_' in col.lower() and 'vs' not in col.lower()])} FROM {table_name} WHERE mz = '{selected_mz}'"

    cursor.execute(query_case)
    case_results = cursor.fetchall()

    case_values = [item for sublist in case_results for item in sublist]
    # Close the cursor and connection
    cursor.close()
    connection.close()

    return case_results


def get_case_columns_linear_query(columName, selected_mz, table_name):
    # Connect to the database
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    # print("all_columns", all_columns)

    query_case = f"SELECT {', '.join([col for col in all_columns if f'case_{columName}_' in col.lower() and 'vs' not in col.lower()])} FROM {table_name} WHERE mz = '{selected_mz}'"
    cursor.execute(query_case)
    case_results = cursor.fetchall()

    get_side_val = f"SELECT q_fdr FROM {table_name} WHERE mz = '{selected_mz}'"
    cursor.execute(get_side_val)
    qfdr_results = cursor.fetchall()

    case_values = [item for sublist in case_results for item in sublist]
    # Close the cursor and connection
    cursor.close()
    connection.close()

    return case_results, qfdr_results


def vs_columnNames(table_name, fig, selected_mz, region_call):
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    col_vs = []

    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    all_columns = [desc[0] for desc in cursor.description]
    query_q_vs = f"SELECT {', '.join([col for col in all_columns if 'vs' in col.lower()])} FROM {table_name} WHERE mz = '{selected_mz}'"
    cursor.execute(query_q_vs, (selected_mz,))
    query_q_vs_result = cursor.fetchall()
    # print("query_q_vs_result", query_q_vs_result)

    for col in all_columns:
        if 'vs' in col.lower():
            col_vs.append(col)
    # print(col_vs)
    index = 0
    vpos = 0.69
    hpos = 0.7
    for i in range(len(region_call)):
        for j in range(i+1, len(region_call)):
            vs_value_name = region_call[i]+"_vs_"+region_call[j]
            vs_value_name_neg = region_call[j]+"_vs_"+region_call[i]
            # print("vpos", vs_value_name, vs_value_name_neg)

            if vs_value_name in col_vs:
                vs_value = col_vs.index(vs_value_name)
                # print(query_q_vs_result[0][vs_value])
                qFdr = query_q_vs_result[0][vs_value]
                # print("exist_", i)

                if qFdr < 0.001:
                    qFdrStars = '***'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars, )
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)
                elif qFdr < 0.01 and qFdr > 0.001:
                    qFdrStars = '**'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars, )
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.05 and qFdr > 0.01:
                    qFdrStars = '*'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars, )
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)

            elif vs_value_name_neg in col_vs:
                vs_value = col_vs.index(vs_value_name_neg)
                # print(query_q_vs_result[0][vs_value])
                # print("exist_", i)
                qFdr = query_q_vs_result[0][vs_value]
                if qFdr < 0.001:
                    qFdrStars = '***'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)
                elif qFdr < 0.01  and qFdr > 0.001:
                    qFdrStars = '**'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.05  and qFdr > 0.01:
                    qFdrStars = '*'
                    add_comparison_lines(fig, region_call, [region_call[i], region_call[j]], [
                                         vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    # print("vpos", vpos+index, hpos+index)
    cursor.close()
    connection.close()


def add_comparison_lines(fig, region_call, regions, y_range, symbol):
    # print("com,ing here")
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

    bar_xcoord_map = {x: idx for idx, x in enumerate(region_call)}
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
