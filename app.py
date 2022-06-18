import dash
from dash import html, State
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas
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
        layouts.memory_app(),
        layouts.left_container,
        layouts.central_container,
        layouts.right_container,
        ], 
    style=styles.style_mix(
        styles.body)
    )

# @app.callback(
#     Output('left-container', 'children'),
#     Output('central-container', 'children'),
#     Output('right-container', 'children'),
#     Output('memory-app', "data"),
#     Input("genres-selector", "value"),
#     Input("outliers-selector", "value"),
#     State("memory-app", "data")
# )
# def update_layout(genres, outliers, memory_app):
#     updated_memory = {}
#     print("Memory app: ", memory_app)
#     pie_genres = [g for g in data.all_genres if g not in genres ]
#     df = data.games_filtered(genres)
#     df = data.remove_outliers(df, outliers)
#     print(outliers)
#     print(df)
#     left_container = [
#         layouts.filters_modal(),
#         layouts.counter(df),
#         layouts.score(df)]

#     central_container = [
#         layouts.table(df, data.table_columns),
#         layouts.date_plot(df)]
#     right_container = [
#         layouts.pie(df, pie_genres),
#         layouts.os_barchar(df)]
#     return (left_container, central_container, right_container, updated_memory)

@app.callback(
    Output('counter', 'value'),
    Output('score', 'value'),
    Output('tbl', 'data'),
    Output('tbl', 'columns'),
    Output('pie-chart', 'figure'),
    Output('scatter-plot', 'figure'),
    Output('bar-chart', "figure"),
    Input("genres-selector", "value"),
    Input("outliers-selector", "value"),
#   Input("filters-memory", "data")
)
def update(genres, outliers):
    df = data.games_filtered(data.games, genres)
    df = data.remove_outliers(df, outliers)
    print("Update")
    counter = data.count(df)
    score = data.metacritic_mean(df)
    table_data, table_columns = data.table(df)
    pie = data.pie(df, genres)
    scatter = data.scatter_plot(df)
    bar = data.bar_chart(df)
    return(
        counter,
        score,
        table_data,
        table_columns,
        pie,
        scatter,
        bar        
    )

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