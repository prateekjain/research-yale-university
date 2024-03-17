import plotly.graph_objects as go
from plotly.subplots import make_subplots
from compare_tumor.data_functions import vs_columnNames, forest_plot
import pandas as pd
import matplotlib.pyplot as plt
import forestplot as fp
import io
import base64
import numpy as np
import cv2

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
    "rcc": 'gold',
    "lcc": 'blue',
}


def tumor_vs_normal_plot(query_case, query_control, final_get_side_val, region_name):
    qFdr = final_get_side_val[0]
    print("qfdr first", qFdr)
    # Determine stars based on qFdr value
    if qFdr <= 0.001:
        qFdrStars = '***'
    elif 0.001 < qFdr <= 0.01:
        qFdrStars = '**'
    elif 0.01 < qFdr <= 0.05:
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
        # gridcolor='lightgrey'
    )
    scatter_plot.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        # gridcolor='lightgrey'
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
        # gridcolor='lightgrey'
    )
    plot_all_regions.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        # gridcolor='lightgrey'
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


def addAnotations(plot_all_regions, qFdrStars):
    plot_all_regions.update_layout(
        annotations=[
            dict(
                x=0.5,
                y=1,
                xref='paper',
                yref='paper',
                text=f"{qFdrStars}<br>",
                align='left',
                showarrow=False,
                font={'size': 16, 'color': 'black'}
            )
        ]
    )

    return plot_all_regions


def comparable_plots(plot_all_regions, query_regions, title, table_name, selected_meta, region_call):

    for i in range(len(region_call)):
        # Create a separate trace for each region with different color
        x_values = [f'{region_call[i]}' for _ in range(
            len(query_regions)//len(region_call))]
        plot_all_regions.add_trace(go.Box(
            x=x_values,
            y=query_regions[i*len(x_values):(i+1)*len(x_values)],
            boxpoints='all',
            fillcolor='white',
            line=dict(color='black'),
            marker=dict(color=region_colors[region_call[i]]),
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
        # gridcolor='lightgrey'
    )
    plot_all_regions.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        # gridcolor='lightgrey'
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

    vs_columnNames(table_name, plot_all_regions, selected_meta, region_call)

    return plot_all_regions


def generate_and_crop_plot(selected_mz):
    result_list = forest_plot(selected_mz)
    result_df = pd.DataFrame(result_list)

    fig, ax = plt.subplots()  # Create a new figure and axes
    fp.forestplot(
        result_df,
        estimate="HR",
        ll="Low",
        hl="High",
        varlabel="region",
        xlabel="Hazard Ratio",
        annote=["region", "est_hr"],
        annoteheaders=["Metabolites", "HR (95%  CI)"],
        flush=False,
        ci_report=False,
        capitalize="capitalize",
        rightannote=["Pval"],
        right_annoteheaders=["P-Value"],
        table=True,
        ax=ax,
        xline_kwargs=dict(linewidth=2)
    )
    # Adjust the layout of the subplot
    plt.subplots_adjust(top=0.855, bottom=0.165, left=0.450,
                        right=0.830, hspace=0.2, wspace=0.2)

    # Save the Matplotlib figure as bytes
    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png",
                bbox_inches="tight", pad_inches=0.1)
    plt.close()  # Close the Matplotlib figure to free up resources

    # Convert bytes to base64 string
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    # Decode the base64 image string to bytes
    img_data = base64.b64decode(img_base64)
    img_np = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

    # Crop the image
    height, width = img.shape[:2]
    new_width = int(width * 0.17)  # Crop 17% from the left
    cropped_img = img[:, new_width:]

    # Encode the cropped image back to base64 string
    _, img_base64_cropped = cv2.imencode('.png', cropped_img)
    img_base64_cropped_str = base64.b64encode(
        img_base64_cropped).decode('utf-8')

    # Create the image source for the html.Img component
    image_src_cropped = f"data:assets/image/png;base64,{img_base64_cropped_str}"
    return image_src_cropped
