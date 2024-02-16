# data_functions.py
import psycopg2

from app import region

import psycopg2
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from dotenv import load_dotenv
import os

table_name = 'tumor_tumor_compare'
all_columns = []

load_dotenv()
db_url = os.getenv('DATABASE_URL')

# add table name and column names for the function
def get_mz_values():
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    query_mz_values = "SELECT DISTINCT mz FROM mz_value"
    cursor.execute(query_mz_values)
    mz_values = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return mz_values

# add table name and column names for the function
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

                if qFdr < 0.001 and qFdr > 0.01:
                    qFdrStars = '***'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)
                elif qFdr < 0.01 and qFdr > 0.05:
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
                if qFdr < 0.001 and qFdr > 0.01:
                    qFdrStars = '***'
                    add_comparison_lines(fig, [region[i], region[j]], [
                        vpos+index, hpos+index], symbol=qFdrStars)
                    index += 0.03
                    print("vpos", vpos+index, hpos+index)

                elif qFdr < 0.01 and qFdr > 0.05:
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

  
def add_comparison_lines(fig, regions, y_range, symbol):
  fig.add_shape(
      type="line",
      xref="x",
      yref="paper",
      x0=regions[0],
      y0=y_range[0],
      x1=regions[0],
      y1=y_range[1],
      line=dict(color="black", width=2),
  )
  fig.add_shape(
      type="line",
      xref="x",
      yref="paper",
      x0=regions[0],
      y0=y_range[1],
      x1=regions[1],
      y1=y_range[1],
      line=dict(color="black", width=2),
  )
  fig.add_shape(
      type="line",
      xref="x",
      yref="paper",
      x0=regions[1],
      y0=y_range[1],
      x1=regions[1],
      y1=y_range[0],
      line=dict(color="black", width=2),
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