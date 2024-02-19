# app.py
import dash
from dash import dcc, html
from compare_tumor.callbacks import register_callbacks
from layout import main_layout

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

external_stylesheets = ['assets/stylesheet.css', 'dbc.themes.BOOTSTRAP']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = main_layout

app.head = [html.Link(rel='stylesheet', href='assets/stylesheet.css')]

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)
