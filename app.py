import dash
from dash import html, State
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import data
import layouts
import styles
import flask

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    server=server,
    external_stylesheets=[dbc.themes.DARKLY]
)

app.title = "Steam Games By Gender"

app.layout = html.Div([
        html.Div(
            id = "left-container",
            children=[
                        layouts.title("STEAM DATA EXPLORER"),
                        layouts.filters_modal("genres-selector", [], "outliers_selector", []),
                        layouts.counter(data.games),
                        layouts.score(data.games)
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(1),
                styles.grid_column(),
                {"background": styles.theme["box_color"]})),
        
        html.Div(
            id = "central-container",
            children = [
                layouts.table(data.games, data.table_columns),
                layouts.date_plot(data.games)
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(7),
                styles.grid_column())),
        
        html.Div(
            id = "right-container",
            children = [
                layouts.pie(data.games, data.all_genres),
                layouts.os_barchar(data.games),
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(2),
                styles.grid_column()))
        ], 
    style=styles.style_mix(
        styles.body)
    )

@app.callback(
    Output('left-container', 'children'),
    Output('central-container', 'children'),
    Output('right-container', 'children'),
    Input("genres-selector", "value"),
    Input("outliers_selector", "value")
)
def update_layout(genres, outliers):
    pie_genres = [g for g in data.all_genres if g not in genres ]
    df = data.games_filtered(genres)
    df = data.remove_outliers(df, outliers)
    print(outliers)
    print(df)
    left_container = [
        layouts.title("STEAM DATA EXPLORER"),
        layouts.filters_modal("genres-selector", genres, "outliers_selector", outliers),
        layouts.counter(df),
        layouts.score(df)]

    central_container = [
        layouts.table(df, data.table_columns),
        layouts.date_plot(df)]
    right_container = [
        layouts.pie(df, pie_genres),
        layouts.os_barchar(df)]
    return (left_container, central_container, right_container)

@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

if __name__ == '__main__':
    app.run_server(debug=True)