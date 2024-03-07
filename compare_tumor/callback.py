# callback.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from compare_tumor.data_functions import get_mz_values, get_case_columns_query, get_case_columns_vs_query, vs_columnNames, add_comparison_lines, get_case_columns_linear_query, get_cecum_and_ascending_mz_values, get_q05_mz_values, selected_mz_cleaning, get_dropdown_options

from compare_tumor.dynamicPlots import tumor_vs_normal_plot, all_regions_plots, comparable_plots, addAnotations

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]


def register_callbacks(app):
    @app.callback(
        [Output(f'scatter-plot-mz_minus_h-{i}', 'figure') for i in range(7)],
        [Input('compound-dropdown', 'value')]
    )
    def tumor_vs_normal_m_mins_plots(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            # Assuming you have a column named "mz" in your tables
            selected_mz = float(selected_compound)

            figures = []

            for i in range(len(region)):
                # Fetch data from the database
                query_case, query_control, final_get_side_val = get_case_columns_query(
                    region[i], selected_mz)
                if not query_case or not query_control:
                    figures.append(go.Figure())
                    continue
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
    def tumor_normal_m_plus_plot(selected_compound):
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
                tumor_plot_all_regions, query_tumor_regions, "Tumor")

            normal_plot_all_regions = make_subplots()
            normal_plot_all_regions = all_regions_plots(
                normal_plot_all_regions, query_normal_regions, "Normal")

            # Show the graph containers
            return tumor_plot_all_regions, normal_plot_all_regions
        else:
            # If dropdown is not selected, hide the containers
            return go.Figure(), go.Figure()

    # @app.callback(
    #     Output('selected-mz-h-value', 'children'),
    #     [Input('compound-dropdown', 'value')]
    # )
    # def update_selected_mz_value(selected_mz):
    #     if selected_mz:
    #         return f"Selected Mz Value: {selected_mz}"
    #     else:
    #         return ""

    @app.callback(
        [Output(f'scatter-plot-mz_plus_h-{i}', 'figure') for i in range(7)],
        [Input('compound-dropdown-mz-plus', 'value')]
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
                    region[i]+"_m_plus_h", selected_mz)
                if not query_case or not query_control:
                    figures.append(go.Figure())
                    continue
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

    @app.callback(
        Output("compound-dropdown-meta", "options"),
        Output("compound-dropdown-meta", "value"),
        Input("filter-radio", "value")
    )
    def update_compound_dropdown(filter_value):
        # Logic to update options based on the selected filter
        
        if filter_value == "all":
            options = [{"label": mz, "value": mz}
                       for mz in get_mz_values("ascending_metabolites")]
            default_value = get_mz_values("ascending_metabolites")[0]

        elif filter_value == "across_all":
            options = [{"label": mz, "value": mz}
                       for mz in list(get_cecum_and_ascending_mz_values(["cecum_metabolites", "ascending_metabolites", "transverse_metabolites", "descending_metabolites", "sigmoid_metabolites", "rectosigmoid_metabolites", "rectum_metabolites"]))]
            default_value = list(get_cecum_and_ascending_mz_values(
                ["cecum_metabolites", "ascending_metabolites", "transverse_metabolites", "descending_metabolites", "sigmoid_metabolites", "rectosigmoid_metabolites", "rectum_metabolites"]))[0]
            
        elif filter_value == "specific_subsites":
            # print("not done")
            # List of all regions
            all_regions = ["cecum_metabolites", "ascending_metabolites", "transverse_metabolites",
                           "descending_metabolites", "sigmoid_metabolites", "rectosigmoid_metabolites", "rectum_metabolites"]

            # Get Mz values for each region
            region_mz_values = {region: set(get_mz_values(region)) for region in all_regions}

            # Find Mz values with q < 0.05 only in one region (not in other 6)
            unique_specific_subsites_mz = set()
            for current_region in all_regions:
                other_regions = set(all_regions) - {current_region}
                current_region_mz = region_mz_values[current_region]

                # Find Mz values with q < 0.05 in the current region
                current_region_q05_mz = set(get_q05_mz_values(current_region))

                # Find Mz values with q < 0.05 in all other regions
                other_regions_q05_mz = set()
                for other_region in other_regions:
                    other_regions_q05_mz |= set(get_q05_mz_values(other_region))

                # Find Mz values with q < 0.05 only in the current region (not in other 6)
                specific_subsites_mz = current_region_q05_mz - other_regions_q05_mz

                # Update the set of unique Mz values
                unique_specific_subsites_mz |= specific_subsites_mz

            # Create options and default value
            options = [{"label": mz, "value": mz} for mz in unique_specific_subsites_mz]
            default_value = list(unique_specific_subsites_mz)[0] if unique_specific_subsites_mz else None

        elif filter_value == "proximal_distal":
            options = [{"label": mz, "value": mz}
                       for mz in list(get_cecum_and_ascending_mz_values(["sigmoid_metabolites", "rectosigmoid_metabolites", "rectum_metabolites"]))]
            default_value = list(get_cecum_and_ascending_mz_values(
                ["sigmoid_metabolites", "rectosigmoid_metabolites", "rectum_metabolites"]))[0]
        else:
            # Default options and value
            options = []
            default_value = None

        return options, default_value

    @app.callback(
        [Output(f'scatter-plot-meta-{i}', 'figure') for i in range(7)],
        [Input('compound-dropdown-meta', 'value')]
    )
    def tumor_vs_normal_meta_plots(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            # Assuming you have a column named "mz" in your tables
            selected_mz = selected_mz_cleaning(selected_compound)

            figures = []

            for i in range(len(region)):
                # Fetch data from the database
                # print("meta_valyes")
                query_case, query_control, final_get_side_val = get_case_columns_query(
                    region[i]+"_metabolites", selected_mz)
                if not query_case or not query_control :
                    figures.append(go.Figure())
                    continue
                
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

    @app.callback(
        Output('tumor-plus-plot', 'figure'),
        Output('normal-plus-plot', 'figure'),
        [Input('compound-dropdown-mz-plus', 'value')]
    )
    def tumor_normal_plot(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            selected_mz = float(selected_compound)
            query_tumor_regions = []
            query_normal_regions = []

            for i in range(len(region)):
                query_case, query_control, final_get_side_val = get_case_columns_query(
                    region[i]+"_m_plus_h", selected_mz)
                query_case = list(query_case[0])
                query_control = list(query_control[0])
                query_tumor_regions.extend(query_case)
                query_normal_regions.extend(query_control)

            tumor_plot_all_regions = make_subplots()
            tumor_plot_all_regions = all_regions_plots(
                tumor_plot_all_regions, query_tumor_regions, "Tumor")

            normal_plot_all_regions = make_subplots()
            normal_plot_all_regions = all_regions_plots(
                normal_plot_all_regions, query_normal_regions, "Normal")

            # Show the graph containers
            return tumor_plot_all_regions, normal_plot_all_regions
        else:
            # If dropdown is not selected, hide the containers
            return go.Figure(), go.Figure()

    @app.callback(
        Output('tumor-comparable-plot', 'figure'),
        Output('normal-comparable-plot', 'figure'),
        [Input('compound-dropdown-compare', 'value')]
    )
    def tumor_normal_comparable_plot(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            selected_meta = selected_mz_cleaning(selected_compound)
            # table_name = "tumor_comparable_plots"
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
                # print(i)
                # print('\n')

                query_case = get_case_columns_vs_query(
                    i, selected_meta, "tumor_comparable_plots")
                query_case = list(query_case[0])
                query_tumor_regions.extend(query_case)
                # print("123qwe", query_tumor_regions)

                query_control = get_case_columns_vs_query(
                    i, selected_meta, "normal_comparable_plots")
                query_control = list(query_control[0])
                query_normal_regions.extend(query_control)
                # print("456qwe", query_normal_regions)

            tumor_plot_comparable_all_regions = make_subplots()
            tumor_plot_comparable_all_regions = comparable_plots(
                tumor_plot_comparable_all_regions, query_tumor_regions, "Tumor", "tumor_comparable_plots", selected_meta, region)

            normal_plot_comparable_all_regions = make_subplots()
            normal_plot_comparable_all_regions = comparable_plots(
                normal_plot_comparable_all_regions, query_normal_regions, "Normal", "normal_comparable_plots", selected_meta, region)

            # Show the graph containers
            return tumor_plot_comparable_all_regions, normal_plot_comparable_all_regions
        else:
            # If dropdown is not selected, hide the containers
            return go.Figure(), go.Figure()

    
    @app.callback(Output("selected-image", "src"),
              [Input("image-dropdown", "value")])
    def update_selected_image(selected_value):
        if selected_value is not None:
            return selected_value
        else:
            return "assets/images/car.jpg"
        
    
    @app.callback(
        Output('tumor-comparable-rcc-lcc-plot', 'figure'),
        Output('normal-comparable-rcc-lcc-plot', 'figure'),
        [Input('compound-dropdown-compare-rcc-lcc', 'value')]
    )
    def tumor_normal_comparable_rcc_lcc_plot(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            selected_meta = selected_mz_cleaning(selected_compound)
            # table_name = "tumor_comparable_plots"
            query_tumor_regions = []
            query_normal_regions = []
            # vs_columnNames(selected_meta)
            # Define a list of colors for each region
            region_colors = {
                "rcc": 'gold',
                "lcc": 'blue',
                "rectum": 'pink',
            }
            region_rcc_lcc = ["rcc", "lcc", "rectum"]

            for i in region_rcc_lcc:
                # print(i)
                # print('\n')

                query_case = get_case_columns_vs_query(
                    i, selected_meta, "tumor_rcc_lcc_comparable_plots")
                query_case = list(query_case[0])
                query_tumor_regions.extend(query_case)
                # print("query_tumor_regions2", query_tumor_regions)

                query_control = get_case_columns_vs_query(
                    i, selected_meta, "normal_rcc_lcc_comparable_plots")
                query_control = list(query_control[0])
                query_normal_regions.extend(query_control)
                # print("query_normal_regions2", query_normal_regions)

            tumor_plot_comparable_all_regions = make_subplots()
            tumor_plot_comparable_all_regions = comparable_plots(
                tumor_plot_comparable_all_regions, query_tumor_regions, "Tumor", "tumor_rcc_lcc_comparable_plots", selected_meta, region_rcc_lcc)

            normal_plot_comparable_all_regions = make_subplots()
            normal_plot_comparable_all_regions = comparable_plots(
                normal_plot_comparable_all_regions, query_normal_regions, "Normal", "normal_rcc_lcc_comparable_plots", selected_meta, region_rcc_lcc)

            # Show the graph containers
            return tumor_plot_comparable_all_regions, normal_plot_comparable_all_regions
        else:
            # If dropdown is not selected, hide the containers
            return go.Figure(), go.Figure()

    @app.callback(
        Output('tumor-linear-plot', 'figure'),
        Output('normal-linear-plot', 'figure'),
        [Input('compound-dropdown-linear', 'value')]
    )
    def tumor_normal_linear_plot(selected_compound):
        if selected_compound is not None:
            # Fetch and process data based on selected values
            selected_meta = selected_mz_cleaning(selected_compound)
            # table_name = "tumor_comparable_plots"
            query_tumor_linear_regions = []
            query_normal_linear_regions = []
            # vs_columnNames(selected_meta)
            # Define a list of colors for each region

            for i in region:
                # print(i)
                # print('\n')

                query_case, q_fdr_case = get_case_columns_linear_query(
                    i, selected_meta, "tumor_linear_plots")
                query_case = list(query_case[0])
                query_tumor_linear_regions.extend(query_case)
                # print(query_tumor_linear_regions)

                query_control, q_fdr_control = get_case_columns_linear_query(
                    i, selected_meta, "normal_linear_plots")

                # print("q_fdr_control", q_fdr_control[0][0])
                query_control = list(query_control[0])
                query_normal_linear_regions.extend(query_control)
                # print(query_normal_linear_regions)

            tumor_linear_plot_all_regions = make_subplots()
            tumor_linear_plot_all_regions = all_regions_plots(
                tumor_linear_plot_all_regions, query_tumor_linear_regions, "Tumor")
            qFdrStars = ''
            if q_fdr_case[0][0] <= 0.001:
                qFdrStars = '***'
                tumor_linear_plot_all_regions = addAnotations(
                    tumor_linear_plot_all_regions, qFdrStars)
            elif q_fdr_case[0][0] <= 0.01 and q_fdr_case[0][0] > 0.001:
                qFdrStars = '**'
                tumor_linear_plot_all_regions = addAnotations(
                    tumor_linear_plot_all_regions, qFdrStars)
            elif q_fdr_case[0][0] <= 0.05 and q_fdr_case[0][0] > 0.01:
                qFdrStars = '*'
                tumor_linear_plot_all_regions = addAnotations(
                    tumor_linear_plot_all_regions, qFdrStars)

            normal_linear_plot_all_regions = make_subplots()
            normal_linear_plot_all_regions = all_regions_plots(
                normal_linear_plot_all_regions, query_normal_linear_regions, "Normal")
            qFdrStars1 = ''
            if q_fdr_control[0][0] <= 0.001:
                qFdrStars1 = '***'
                normal_linear_plot_all_regions = addAnotations(
                    normal_linear_plot_all_regions, qFdrStars1)
            elif q_fdr_control[0][0] <= 0.01 and q_fdr_control[0][0] > 0.001:
                qFdrStars1 = '**'
                normal_linear_plot_all_regions = addAnotations(
                    normal_linear_plot_all_regions, qFdrStars1)
            elif q_fdr_control[0][0] <= 0.05 and q_fdr_control[0][0] > 0.01:
                qFdrStars1 = '*'

                normal_linear_plot_all_regions = addAnotations(
                    normal_linear_plot_all_regions, qFdrStars1)

    #             if qFdr <= 0.001:
    #       qFdrStars = '***'
    # elif 0.001 < qFdr <= 0.01:
    #     qFdrStars = '**'
    # elif 0.01 < qFdr <= 0.05:
    #     qFdrStars = '*'
            # Show the graph containers
            return tumor_linear_plot_all_regions, normal_linear_plot_all_regions
        else:
            # If dropdown is not selected, hide the containers
            return go.Figure(), go.Figure()