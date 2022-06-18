import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from jupyter_dash import JupyterDash
import dash
from dash import dcc
from dash import html, dash_table
import dash_daq as daq
import data
import styles as styles
import dash_bootstrap_components as dbc




def darkTheme(element):
    return(
        daq.DarkThemeProvider(
            theme=styles.theme2,
            children=[element]))

def title(text):
    return(
        html.H1(
            text, 
            style={
                "color": styles.theme2["primary"],
                "background": styles.theme["background_color"],"position": "relative",
                "margin-bottom": "-30px",
                "text-align": "center",
                "width": "120%",
                "left": "-10%",
                "border-top": "1px solid",
                "border-bottom": "1px solid"}))

def memory_app():
    return(dcc.Store(id="memory-app", data={}))

#FILTERING
def modal(header=None, children=None, footer=None, button=None):
    return html.Div(
        [
            html.Div(
                [dbc.Button(button or "Open Modal", id="open", n_clicks=0)], 
                style={"display": "flex", "justify-content": "space-around"}),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle(header)),
                    dbc.ModalBody(children),
                    dbc.ModalFooter([
                        footer,
                        dbc.Button(
                            "Close", id="close", className="ms-auto", n_clicks=0
                        )]
                    ),
                ],
                id="modal",
                is_open=False,
            ),
        ]
    )

def genres_selector(): 
    return(
        html.Label(
            children = [
                "Game Tag",
                dcc.Dropdown(
                    id="genres-selector", clearable=True,
                    multi=True,
                    value=[],
                    options=[
                        {'label': c, 'value': c}
                        for c in data.all_genres
                    ])],
            style={"width": "100%"},
        ))

def remove_outliers_selector():
    return(
        html.Label(
            children = [
                "Remove Outliers",
                dcc.Dropdown(
                    id="outliers-selector", clearable=True,
                    multi=True, 
                    value=[],
                    options=[
                        {'label': c, 'value': c}
                        for c in data.numeric_filter])],
            style={"width": "100%"}))

def filters_modal():
    children = [
        genres_selector(),
        remove_outliers_selector(),
        # filters_container(data.games)
    ]
    return(modal("Filters", children, "Query", "Select data"))

# PRINCIPAL COMPONENTS 
def counter(df):  
    count = data.count(data.games)
    
    return(darkTheme(
        daq.LEDDisplay(
            # label="Number of games",
            id="counter",
            label={
                "label": "Number of games",
                "style": styles.daq_label
                },
            color=styles.theme2['primary'],
            backgroundColor="ffffff",
            value=count)))

def score(df):
    mean = data.metacritic_mean(df)
    return(darkTheme(
        daq.Gauge(
            # color={"gradient":True,"ranges":{"red":[0,33], "yellow":[33,66],"green":[66,100],}},
            id="score",
            color=styles.theme2['primary'],
            className='dark-theme-control',
            value=mean,
            label={
                "label": 'Metacritic score',
                "style": styles.daq_label
                },
            max=100,
            min=0)))

def table(df):
    table_dict, columns = data.table(df)
    return(
        dash_table.DataTable(
            table_dict,
            columns,
            id='tbl',
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            page_action="native",
            page_current= 0,
            page_size= 10))

def pie(df):
    return dcc.Graph(id="pie-chart", figure=data.pie(df))

def date_plot(df):
    return dcc.Graph(id="scatter-plot", figure=data.scatter_plot(df))

def os_barchart(df):
    return dcc.Graph(id="bar-chart", figure=data.bar_chart(df))

def filters_container(df=None):
    filters_container_layout = html.Div([
        dcc.Store(
                id='filters-memory',
                data={}),
        html.Button("Add Group", id="add-filter-group", n_clicks=0),
        html.Div("QUERY"),
        html.Div(id='filter-groups-container', children = [], style={'display': 'flex', 'flex-direction': 'column'})
    ], style={'padding': 10, 'flex': 4})

    return filters_container_layout

def filter_group(n:int, variables:list, index:int, group_memory):
    children = group_memory
    return(
        html.Div([
            dcc.Store(
                id={"type": "group-memory", "index":index},
                data={}
            ),
            html.Button("+", id={"type":"add-filter", "index": index}, n_clicks=0),
            html.Div(id='group-container', children=[], style={'display': 'flex', 'flex-flow': 'column nowrap'}),
            html.Button("-", id={"type":"delete-group", "index": index}, n_clicks=0),
        ])
    )

def filter_row(n:int, variables:list):
    """Will return a Div with following components:
            - AND / OR dropdown selector
            - Variable selector with given variables argument
            - Checklist to negate filter
            - A div with needed inputs for filtering
    """
    return(
        html.Div([
            dcc.Store(id={'type':'filter-row-memory', 'index': n}),
            dcc.Dropdown(
                id={'type':'filter_operator', 'index': n}, clearable=False,
                value="AND", options=[
                    {'label': "AND", 'value': "AND"},
                    {'label': "OR", 'value': "OR"}
                ],
                style={'width': '100%'}),
            
            dcc.Dropdown(
                id={'type':'filter-variable-selector', 'index': n}, clearable=True,
                multi=False,
                placeholder="Variable",
                value=[], options=[
                    {'label': c, 'value': c}
                    for c in variables
                ],
                style={'width': '100%'}),
                
            dcc.Checklist(
                id={'type':"filter-negate", 'index': n},
                options=["NOT"],
                style={'width': '100%'}),

            dcc.Dropdown(
                id={'type':'filter-type', 'index': n}, clearable=True,
                multi=False,
                placeholder="Operator",
                value=[], options=[
                    {'label': "Lower than", 'value': "lt"},
                    {'label': "Greater than", 'value': "gt"},
                    {'label': "Between", 'value': "btw"},
                    {'label': "Equals", 'value': "eq"},
                    {'label': "in", 'value': "in"},
                ],
                style={'width': '100%'}),
            html.Div(
                id={'type': "f-vars-container", "index": n}, 
                children = [], 
                style=styles.one_row),

            html.Button("-", id={"type":"delete-filter", "index": n}, n_clicks=0),

        ], style={'padding': 10, 'flex': 1, 'display': 'flex', 'flex-flow': "row nowrap"})
    )

left_container = html.Div(
            id = "left-container",
            children=[
                        title("STEAM DATA EXPLORER"),
                        filters_modal(),
                        counter(data.games),
                        score(data.games)
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(1),
                styles.grid_column(),
                {"background": styles.theme["box_color"]}))

central_container = html.Div(
            id = "central-container",
            children = [
                table(data.games),
                date_plot(data.games)
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(7),
                styles.grid_column()))

right_container = html.Div(
            id = "right-container",
            children = [
                pie(data.games),
                os_barchart(data.games),
            ],
            style=styles.style_mix(
                styles.basic, 
                styles.box(2),
                styles.grid_column()))