import dash
from dash import html
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
import dash_daq as daq
# import dash_bootstrap_components as dbc
import data
import layouts
import styles
import flask

server = flask.Flask(__name__)

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    server=server
)

app.title = "Steam Games By Gender"

app.layout = html.Div([
        html.Div(
            id = "left-container",
            children=[
                
                        layouts.gender_selector("genres-selector"),
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

print("Entra")

@app.callback(
    Output('left-container', 'children'),
    Output('central-container', 'children'),
    Output('right-container', 'children'),
    Input("genres-selector", "value"),
)
def update_layout(genres):
    print("Callback: " , genres)
    pie_genres = [g for g in data.all_genres if g not in genres ]
    df = data.games_filtered(genres)
    left_container = [
        layouts.gender_selector("genres-selector", value=genres),
        layouts.counter(df),
        layouts.score(df)]

    central_container = [
        layouts.table(df, data.table_columns),
        layouts.date_plot(df)]
    right_container = [
        layouts.pie(df, pie_genres),
        layouts.os_barchar(df)]
    return (left_container, central_container, right_container)

if __name__ == '__main__':
    app.run_server(debug=True)