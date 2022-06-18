from typing import List
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import csv
import styles 
games = pd.read_csv("games.csv")

def add_day(date):
    date = date.split(" ")
    if len(date) > 2:
        return " ".join(date)
    date[0] = date[0] + " 1,"
    return " ".join(date)

games["Release date"] = games["Release date"].apply(add_day)
games['Release date'] =  pd.to_datetime(games['Release date'], format='%b %d, %Y')


#Following variables are set to apply filters depending on column value.
numeric_filter_columns = ["Price", "DLC count", "Achievements", "Recommendations", "Metacritic score", "Required age"]
str_filter_columns = ["Name", "Gender"]
date_filter_columns = ["Release Date"]

TABLE_COLUMNS = ["Name", 'Price', 'Release date', 'DLC count', 'Achievements', 'Recommendations', 'Metacritic score', 'Required age']
numeric_filter = ['Price', 'DLC count', 'Achievements', 'Recommendations', 'Metacritic score', 'Required age']
def create_genres_csv_file(file_name):
    all_genres = []
    for index, row in games.iterrows():
        genres = []
        if type(row['Genres']) == str:
            genres += row['Genres'].split(",")
        # if type(row['Categories']) == str:
        #     genres += row['Categories'].split(",")

        for g in genres:
            if g not in all_genres: all_genres.append(g)

    with open(f"{file_name}.csv", 'w') as f:
        writer = csv.writer(f)
        writer.writerow(all_genres)

all_genres = []
with open("genders.csv", 'r') as f:
    reader = csv.reader(f)
    all_genres = list(reader)[0]

ALL_GENRES = all_genres

def count(df:pd.DataFrame)->int:
    """Counts rows

    Args:
        df (pd.DataFrame): Any dataframe containing at least one index

    Returns:
        int: len(df.index)
    """
    return len(df.index)

def metacritic_mean(df:pd.DataFrame)->float: 
    """Returns Metacritic mean score
    Args:
        df (pd.DataFrame): Required columns: ['Metacritic score']
        

    Returns:
        float: Mean of all values but zeros.
    """
    return df['Metacritic score'][df['Metacritic score'] != 0].mean()

def table(df:pd.DataFrame)->tuple:
    """Returns data ready to be inserted in a dcc.table component

    Args:
        df (pd.DataFrame): Any dataframe containing columns in 
        global variable TABLE_COLUMNS

    Returns:
        tuple: (
            dict: data to be represented,
            list: dict of dicts containing name and id of each column
    """
    table = df[TABLE_COLUMNS]
    return ( 
        table.to_dict('records'),
        [{"name": i, "id": i} for i in table.columns],
    )

# TODO: Aggregate all ignored units in an "Others" category
def pie(df:pd.DataFrame, selected:str=[])->go.Figure:
    """Returns Pie chart figure of given dataframe separated by genre

    Args:
        df (pd.DataFrame): steam games dataset used in this project.
            Required columns: ['Genres']
        selected (str): Name of selected genres so they are excluded.

    Returns:
        go.Figure: Pie chart of videogames by genres in df
    """
    labels = []
    values = []
    genres = [g for g in ALL_GENRES if g not in selected]
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

    return fig

def scatter_plot(df:pd.DataFrame)->go.Figure:
    """Scatter plot Release-date ~ Price

    Args:
        df (pd.DataFrame): steam games dataset used in this project.
            Required columns: ['Release date', 'Price']
    Returns:
        go.Figure: Scatter plot x=date y=price of videogames in df
    """
    color = ['rgb(56, 75, 126)'] * len(df.index)
    # color = ['rgb(0, 234, 100)'] * len(df.index)
    fig = px.scatter(
            df, x="Release date", y="Price",
            render_mode="webgl", title="Price by Release Date",
            hover_name="Name",
            color=color)

    fig.update_layout(styles.plotly_layout) 
    fig.layout.update(showlegend=False)

    return fig

def bar_chart(df:pd.DataFrame)->px.bar:
    """Bar plot of games by operating system

    Args:
        df (pd.DataFrame): steam games dataset used in this project.
            Required columns: ['Windows', 'Mac', 'Linux']

    Returns:
        px.bar: Barchart with number of videogames by operating system
    """
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
    return fig

def games_filtered(df:pd.DataFrame, genre_list:List=[])->pd.DataFrame:
    """Given a list of genres will return the mask (Series containing True)
    on each row match containing one of those genres in genre_list.

    Args:
        df (pd.DataFrame): DF to be filtered. Required columns: ['Genres']
        genre_list (List, optional): List with genres to be filtered. 
        Defaults to [].

    Returns:
        pd.Series: Filtered DF with only rows containig any of given genres
        in "Genres" column 
    """
    if not genre_list:
        return df
    search_string = "|".join(genre_list)
    mask = df["Genres"].str.contains(search_string) | df["Categories"].str.contains(search_string)
    return df[mask]

def remove_outliers(df:pd.DataFrame, columns:list, factor:int=3)->pd.DataFrame:
    """Filters out outliers from given columns in given dataframe. stats.zscore
    method is used with a default value of 3. This factor indicates the number
    of standar desviations from mean to be considerated outlier

    Args:
        df (pd.DataFrame): DF in wich outliers will be removed.
            Required columns: columns given in following input.
        columns (list): List of numeric columns names in wich apply the filter.
            factor (int, optional): Factor * standar desviation
        Will be the limit distance to be considered outlier. Defaults to 3.

    Returns:
        pd.DataFrame: given dataframe without rows with outliers in 
        given columns.
    """
    if not columns:
        return df

    result = df[(np.abs(stats.zscore(df[columns])) <3).all(axis=1)]
    return result