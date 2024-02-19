# callback.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from compare_tumor.data_functions import get_mz_values, get_meta_values, get_case_columns_query, get_case_columns_vs_query, vs_columnNames, add_comparison_lines

from compare_tumor.dynamicPlots import tumor_vs_normal_plot, all_regions_plots, comparable_plots

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]


def register_callbacks(app):
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
                scatter_plot = tumor_vs_normal_plot(
                    query_case, query_control, final_get_side_val,  region[i])

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

            for i in range(len(region)):
                query_case, query_control, final_get_side_val = get_case_columns_query(
                    region[i], selected_mz)
                query_case = list(query_case[0])
                query_control = list(query_control[0])
                query_tumor_regions.extend(query_case)
                query_normal_regions.extend(query_control)

            tumor_plot_all_regions = make_subplots()
            tumor_plot_all_regions = all_regions_plots(
                tumor_plot_all_regions, query_tumor_regions)

            normal_plot_all_regions = make_subplots()
            normal_plot_all_regions = all_regions_plots(
                normal_plot_all_regions, query_normal_regions)

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

    @app.callback(
        Output('tumor-comparable-plot', 'figure'),
        Output('normal-comparable-plot', 'figure'),
        [Input('compound-dropdown-compare', 'value')]
    )
    def tumor_normal_comparable_plot(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            selected_meta = selected_compound
            table_name = "tumor_comparable_plots"
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
            tumor_plot_comparable_all_regions = comparable_plots(tumor_plot_comparable_all_regions, query_tumor_regions, "Tumor", table_name,selected_meta)
            

            normal_plot_comparable_all_regions = make_subplots()
            normal_plot_comparable_all_regions = comparable_plots(normal_plot_comparable_all_regions, query_tumor_regions, "Normal", table_name,selected_meta)
            
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
