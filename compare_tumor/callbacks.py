# callback.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output 
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from compare_tumor.data_functions import get_meta_values, get_case_columns_vs_query, vs_columnNames, add_comparison_lines
from app import region

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
