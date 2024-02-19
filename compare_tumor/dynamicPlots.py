import plotly.graph_objects as go
from plotly.subplots import make_subplots
from compare_tumor.data_functions import vs_columnNames

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

region_colors = {
    "cecum": 'aliceblue',
    "ascending": 'blue',
    "transverse": 'cyan',
    "descending": 'mistyrose',
    "sigmoid": 'yellow',
    "rectosigmoid": 'brown',
    "rectum": 'pink',
}


def tumor_vs_normal_plot(query_case, query_control, final_get_side_val, region_name):
    qFdr = final_get_side_val[0]

    # Determine stars based on qFdr value
    if 0.001 < qFdr < 0.01:
        qFdrStars = '***'
    elif 0.01 < qFdr < 0.05:
        qFdrStars = '**'
    elif qFdr < 0.05:
        qFdrStars = '*'
    else:
        qFdrStars = 'NA'

    # Create a scatter plot
    scatter_plot = make_subplots()

    # Add box plots for 'Tumor' values
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

    # Add a box plot for 'Normal' values
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
    scatter_plot.update_layout(
        width=300,
        height=500,
        xaxis=dict(
            title=dict(
                text=f'<b>{region_name}</b>',
                font=dict(size=14, family='Arial, sans-serif', color='black')
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
                font={'size': 12, 'color': 'black'},
                bordercolor='black',
                borderwidth=1
            )
        ]
    )

    return scatter_plot


def all_regions_plots(plot_all_regions, query_regions, title):

    for i in range(len(region)):
        # Create a separate trace for each region with different color
        x_values = [f'{region[i]}' for _ in range(
            len(query_regions)//len(region))]
        plot_all_regions.add_trace(go.Box(
            x=x_values,
            y=query_regions[i*len(x_values):(i+1)*len(x_values)],
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
    plot_all_regions.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    plot_all_regions.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    plot_all_regions.update_layout(
        width=600,
        height=500,
        xaxis=dict(
            title=dict(
                text=f'<b>All Regions {title}</b>',
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
    return plot_all_regions


def comparable_plots(plot_all_regions, query_regions, title, table_name,selected_meta ):

    for i in range(len(region)):
        # Create a separate trace for each region with different color
        x_values = [f'{region[i]}' for _ in range(
            len(query_regions)//len(region))]
        plot_all_regions.add_trace(go.Box(
            x=x_values,
            y=query_regions[i*len(x_values):(i+1)*len(x_values)],
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
    plot_all_regions.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    plot_all_regions.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    plot_all_regions.update_layout(
        width=600,
        height=500,
        xaxis=dict(
            title=dict(
                text=f'<b>All Regions Comparable {title}</b>',
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
    
    vs_columnNames(table_name, plot_all_regions, selected_meta)

    return plot_all_regions
