import dash
from dash import dcc, html
from dash.exceptions import PreventUpdate
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


# google_analytics_scripts = html.Div([
#     html.Script(**{"async": True}, src="https://www.googletagmanager.com/gtag/js?id=G-W6VVKGXT93"),
#     html.Script("""
#         window.dataLayer = window.dataLayer || [];
#         function gtag(){dataLayer.push(arguments);}
#         gtag('js', new Date());
#         gtag('config', 'G-W6VVKGXT93');
#     """)
# ])


app.layout = html.Div([
    # google_analytics_scripts, 
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/yale-university':
        return main_layout
    elif pathname == '/':
        # Redirect to '/yale-university' when visiting '/'
        return dcc.Location(pathname='/yale-university', id='redirect')
    else:
        return main_layout404

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
