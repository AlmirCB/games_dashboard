import pandas as pd
import csv


games = pd.read_csv("games.csv")

def add_day(date):
    date = date.split(" ")
    if len(date) > 2:
        return " ".join(date)
    date[0] = date[0] + " 1,"
    return " ".join(date)

games["Release date"] = games["Release date"].apply(add_day)
games['Release date'] =  pd.to_datetime(games['Release date'], format='%b %d, %Y')

table_columns = ["Name", 'Price', 'Release date', 'DLC count', 'Achievements', 'Recommendations', 'Metacritic score', 'Required age']

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

def games_filtered(genre_list=None):
    if not genre_list:
        return games
    search_string = "|".join(genre_list)
    mask = games["Genres"].str.contains(search_string) | games["Categories"].str.contains(search_string)
    return games[mask]