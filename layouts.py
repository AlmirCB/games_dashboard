import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# from jupyter_dash import JupyterDash
import dash
import dash_core_components as dcc
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

def gender_selector(id = None, value = []): 
    return(
        html.Label(
            children = [
                "Game Tag",
                dcc.Dropdown(
                    id=id, clearable=True,
                    multi=True,
                    value=value, options=[
                        {'label': c, 'value': c}
                        for c in data.all_genres
                    ])],
            style={"width": "100%"},
        ))

def remove_outliers_selector(id = None, value = []):
    return(
        html.Label(
            children = [
                "Remove Outliers",
                dcc.Dropdown(
                    id=id, clearable=True,
                    multi=True,
                    value=value, options=[
                        {'label': c, 'value': c}
                        for c in data.numeric_filter])],
            style={"width": "100%"}))

def filters_modal(gen_id = None, gen_values = [], out_id = None, out_values = None):
    children = [
        gender_selector(gen_id, gen_values),
        remove_outliers_selector(out_id, out_values)
    ]
    return(modal("Filters", children, "Query", "Select data"))

def counter(df,):  
    count = len(df.index)
    
    return(darkTheme(
        daq.LEDDisplay(
            # label="Number of games",
            label={
                "label": "Number of games",
                "style": styles.daq_label
                },
            color=styles.theme2['primary'],
            backgroundColor="ffffff",
            value=count)))

def score(df):
    mean = df['Metacritic score'][df['Metacritic score'] != 0].mean()
    return(darkTheme(
        daq.Gauge(
            # color={"gradient":True,"ranges":{"red":[0,33], "yellow":[33,66],"green":[66,100],}},
            color=styles.theme2['primary'],
            className='dark-theme-control',
            value=mean,
            label={
                "label": 'Metacritic score',
                "style": styles.daq_label
                },
            max=100,
            min=0)))

def table(df, columns):
    table = df[columns]
    return(
        dash_table.DataTable(
            table.to_dict('records'),
            [{"name": i, "id": i} for i in table.columns], 
            id='tbl',
            style_cell={
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'maxWidth': 0
            },
            page_action="native",
            page_current= 0,
            page_size= 10))

def pie(df, genres):
    labels = []
    values = []
    for genre in genres:
        subset = df[df['Genres'].str.contains(genre)==True]
        labels.append(genre)
        values.append(len(subset.index))
    
    labels = [x for _, x in sorted(zip(values, labels), reverse=True)]
    values = sorted(values, reverse=True)
    labels = labels[0:9]
    values = values[0:9]

    colors =  ['rgb(56, 75, 126)']

    marker = {
            "colors": colors*10,
            "line":{
                "color": 'rgb(4,15,15)',
                "width": 2}}

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, textinfo='label+percent',
                             insidetextorientation='radial',
                             marker=marker
                            )])
    
    fig.update(layout_title_text='Subgenres',
            layout_showlegend=False)
    
    fig.update_layout(styles.plotly_layout)


    return dcc.Graph(figure=fig)

def date_plot(df):
    color = ['rgb(56, 75, 126)'] * len(df.index)
    # color = ['rgb(0, 234, 100)'] * len(df.index)
    fig = px.scatter(
            df, x="Release date", y="Price",
            render_mode="webgl", title="Price by Release Date",
            hover_name="Name",
            color=color)

    fig.update_layout(styles.plotly_layout) 
    fig.layout.update(showlegend=False)

    return dcc.Graph(figure=fig)

def os_barchar(df):
    color = ['rgb(56, 75, 126)'] * 3
    win_games = len(df[df['Windows']].index)
    mac_games = len(df[df['Mac']].index)
    linux_games = len(df[df['Linux']].index)
    values = [['Windows', win_games], ['Mac', mac_games], ['Linux', linux_games]]
    df_os = pd.DataFrame(values, columns = ["Operating System", "Number of games"])
    fig = px.bar(
        df_os, 
        x='Operating System', 
        y='Number of games',
        title="Games per OS",
        height=400,
        color=color)
    
    fig.update_layout(styles.plotly_layout)
    fig.update_layout(xaxis_title=None, yaxis_title=None, yaxis_showticklabels=False)
    fig.layout.update(showlegend=False)

    return dcc.Graph(figure=fig)