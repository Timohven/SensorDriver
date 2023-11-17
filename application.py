import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc


application = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.UNITED])


application.layout = html.Div([
    html.H2('Laser sensor driver'),
    dash.page_container,
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ])
])


if __name__ == '__main__':
    application.run(debug=True)