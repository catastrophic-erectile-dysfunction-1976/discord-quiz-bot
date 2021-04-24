import pandas as pd
import random
from dollar import usd
import numpy as np

def draw_a_question (category: str, userid: str):
    qdb = pd.read_csv('questions_db.csv', delimiter=';', error_bad_lines=False, encoding='utf-8')
    qdb = qdb.set_index('No')

    if category == "":
        q_no = random.randint(1,qdb.shape[0])
        q_data = qdb.iloc[[q_no-1]]
        qdb = qdb.drop(labels=q_no, axis=0)
        qdb.index = np.arange(1, len(qdb) + 1)

    else:
        qdb_2 = qdb[qdb["Category"] == category]
        index_range = qdb_2.index.tolist()
        q_no = random.randint(index_range[0],index_range[-1])
        q_data = qdb.iloc[[q_no-1]]
        qdb = qdb.drop(labels=q_no, axis=0)
        qdb.index = np.arange(1, len(qdb) + 1)

    # saving qdb to csv after deleting the question
    qdb.to_csv('questions_db.csv', sep=';', encoding='utf-8', index_label='No')

    cat = q_data['Category'].iloc[0]
    question = q_data['Question'].iloc[0]
    ans_a = "\n   A) " + str(q_data["A"].iloc[0])
    ans_b = "\n   B) " + str(q_data["B"].iloc[0])
    if str(q_data["C"].iloc[0]) != "nan":
        ans_c = "\n   C) " + str(q_data["C"].iloc[0])
    else:
        ans_c = ""
    if str(q_data["D"].iloc[0]) != "nan":
        ans_d = "\n   D) " + str(q_data["D"].iloc[0])
    else:
        ans_d = ""

    ans_correct = q_data["Correct"].iloc[0]
    prize = int(q_data["Level"]) * 100

    question_full = "<@!" + userid + ">, you are playing for **" + usd(str(prize)) + "**. Category: **" + str(cat) + "**.\n**Question**: " + str(question) + ans_a + ans_b + ans_c + ans_d

    return [question_full,str(ans_correct),prize]