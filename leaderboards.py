import csv
from pathlib import Path
import pandas as pd
from dollar import usd

def leaderboard_write(user: str, correct: int, prize: int):
    if Path('leaderboard.csv').is_file():
        # 1) add results and write new rows
        with open('leaderboard.csv', 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            record = [user, correct, prize]
            writer.writerow(record)
    else:
        # 2) start a new csv file if leaderboards.csv doesn't exist
        with open('leaderboard.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(["User", "Correct", "Prize"])
            record = [user, correct, prize]
            writer.writerow(record)


def userscore(user: str):
    if Path('leaderboard.csv').is_file():
        # 1) if leaderboard.csv exists
        leader_db = pd.read_csv('leaderboard.csv', encoding='utf-8', sep=';')
        leader_db = leader_db[leader_db['User'] == user]
        leader_db["score"] = leader_db['Correct'] * leader_db['Prize']
        score = leader_db["score"].sum()

    else:
        # 2) if leaderboard.csv doesn't exist (this theoretically shouldn't happen but you know, it's me and my spaghetti)
        score = "Error: Currently no leaderboard exists."

    return str(score)


def call_leaderboard():
    if Path('leaderboard.csv').is_file():
        # 1) if leaderboard.csv exists
        # a) Get unique values from 'User' column
        df_leaderboard = pd.read_csv('leaderboard.csv', encoding='utf-8', sep=';')
        df_leaderboard['score'] = df_leaderboard['Correct'] * df_leaderboard['Prize']
        df_leaderboard = df_leaderboard.groupby('User').sum()
        df_leaderboard = df_leaderboard.sort_values(by=['score'], ascending=False)
        user_list = df_leaderboard.index.tolist()
        rank = 0
        ldb = ""
        for contestant in user_list:
            score = df_leaderboard.iloc[rank,2]
            rank = rank + 1
            ldb = ldb + str(rank) + ") " + contestant + ": " + usd(str(score)) + "\n"
        return ldb

    else:
        # 2) if leaderboard.csv doesn't exist (this theoretically shouldn't happen but you know, it's me and my spaghetti)
        ldb = "Currently no leaderboard exists."
        return ldb
