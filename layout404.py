import dash
from dash import dcc, html
import dash_bootstrap_components as dbc


main_layout404 = dbc.Container(
    [
      dbc.Row(
            [
                html.H1("Page Not found 404",
                        className="title"),
            ]
        ),
        
    ]
  )