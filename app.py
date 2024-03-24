# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from compare_tumor.callback import register_callbacks
from layout import main_layout
from layout404 import main_layout404

region = ["cecum", "ascending", "transverse",
          "descending", "sigmoid", "rectosigmoid", "rectum"]

external_stylesheets = ['assets/stylesheet.css', 'dbc.themes.BOOTSTRAP']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)
app.title = 'Colorectal Cancer Metabolome'
server = app.server
app.layout = main_layout
app.head = [html.Link(rel='stylesheet', href='assets/stylesheet.css')]

app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets,
                 suppress_callback_exceptions=True)
app2.layout = main_layout404


@app.callback(Output('yale-university', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/yale-university':
        return app.layout
    else:
        return app2.layout


register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
