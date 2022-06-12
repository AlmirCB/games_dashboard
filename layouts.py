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


def darkTheme(element):
    return(
        daq.DarkThemeProvider(
            theme=styles.theme2,
            children=[element]))

def gender_selector(id = None, value = []): 
    return(
        html.Label([
            "Game Tag",
            dcc.Dropdown(
                id=id, clearable=True,
                multi=True,
                value=value, options=[
                    {'label': c, 'value': c}
                    for c in data.all_genres
                ])
        ]))

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