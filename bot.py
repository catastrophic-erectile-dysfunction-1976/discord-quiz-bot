# bot.py
import os
import discord
from dotenv import load_dotenv
import asyncio
import pandas as pd
from question_picker import draw_a_question
from leaderboards import leaderboard_write, userscore, call_leaderboard
from dollar import usd

# some shit who care ddddddd
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# settings and initial variable values
xcountdown = 0
set_timer = 15
xtimer = set_timer
contestant = ""
abcd = ['A', 'B', 'C', 'D']

# open csv file with questions database
qdb = pd.read_csv('questions_db.csv', delimiter = ';', error_bad_lines=False, encoding = 'utf-8')
qdb.index = qdb['No']
print(qdb)

# list of categories
categories = qdb['Category'].unique().tolist()

# empty list of users who answered last 10 questions
naughty_list = []

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    global xcountdown, xtimer, xuser, contestant, correct, prize, categories, qdb, naughty_list

    if message.author == client.user:
        return

    if message.content[:4] == '!ask' and xcountdown == 0:

        if qdb.empty:
            await message.channel.send("That's our show, folks! No more questions in the database. Type '!leaderboard' to see the final results!")

        elif naughty_list.count(message.author) == 5:
            await message.channel.send("You've answered too many questions recently. Please give someone else a chance. :)")

        else:
            xuser = str(message.author.id)
            contestant = message.author
            xmsg = str(message.content)
            xmsg = xmsg.split(' ', 1)
            # 1) random category (no category was selected)
            if len(xmsg) == 1:
                question = draw_a_question("", xuser)
                prize = question[2]
                correct = question[1]
                await message.channel.send(question[0])
                contestant = message.author
                if len(naughty_list) < 10:
                    naughty_list = naughty_list + [contestant]
                else:
                    naughty_list = naughty_list[1:10] + [contestant]

                # countdown
                xcountdown = 1
                message = await message.channel.send('Time left: ' + str(xtimer) + ' seconds')
                while xtimer > -1 and xcountdown == 1:
                    await message.edit(content='Time left: ' + str(xtimer) + ' seconds')
                    xtimer = xtimer - 1
                    await asyncio.sleep(1)
                if xcountdown == 1:
                    await message.edit(
                        content="Time's up! No answer has been given. You've lost " + usd(str(prize)) + ".")
                    leaderboard_write(contestant, -1, int(prize))
                    xcountdown = 0
                    xtimer = set_timer
            # 2) chosen category (picked by user)
            elif len(xmsg) > 1:
                xcat = xmsg[1].lower()
                xswitch = 0
                for cat in categories:
                    if cat == xcat:
                        xswitch = xswitch + 1

                if xswitch == 1:
                    question = draw_a_question(xcat, xuser)
                    prize = question[2]
                    correct = question[1]
                    await message.channel.send(question[0])
                    contestant = message.author
                    if len(naughty_list) < 10:
                        naughty_list = naughty_list + [contestant]
                    else:
                        naughty_list = naughty_list[1:10] + [contestant]
                    # countdown
                    xcountdown = 1
                    message = await message.channel.send('Time left: ' + str(xtimer) + ' seconds')
                    while xtimer > -1 and xcountdown == 1:
                        await message.edit(content='Time left: ' + str(xtimer) + ' seconds')
                        xtimer = xtimer - 1
                        await asyncio.sleep(1)
                    if xcountdown == 1:
                        await message.edit(
                            content="Time's up! No answer has been given. You've lost " + usd(str(prize)) + ".")
                        leaderboard_write(contestant, -1, int(prize))
                        xcountdown = 0
                        xtimer = set_timer
                # 3) chosen category has not been found in the database
                else:
                    await message.channel.send("Sorry, couldn't find category called " + xmsg[1])
                # question = draw_a_question(xmsg[1], xuser)



    if message.content == '!countdown':
        xcountdown = 1
        message = await message.channel.send('Time left: ' + str(xtimer) + ' seconds')
        while xtimer > 0 and xcountdown == 1:
            await message.edit(content='Time left: ' + str(xtimer) + ' seconds')
            xtimer = xtimer - 1
            await asyncio.sleep(1)
        if xcountdown == 1:
            await message.edit(content="Time's up! No answer has been given.")
            xcountdown = 0
            xtimer = set_timer

    if message.content.upper() in abcd and message.author == contestant and xcountdown == 1:
            xcountdown = 0
            if message.content.upper() == correct:
                leaderboard_write(contestant,1,int(prize)+xtimer)
                await message.channel.send("Correct! You've won " + usd(str(int(prize)+xtimer)) + ".")
            else:
                leaderboard_write(contestant, -1, int(prize))
                await message.channel.send("Incorrect, the correct answer is: " + str(correct) + ". You've lost " + usd(str(prize)) + ".")
            xtimer = set_timer

    if message.content == '!categories':
        qdb = pd.read_csv('questions_db.csv', delimiter=';', error_bad_lines=False, encoding='utf-8')
        qdb.index = qdb['No']
        categories = qdb['Category'].unique().tolist()
        xlistcats = ""
        for cat in categories:
            cash = qdb[qdb['Category']==cat].sum()["Level"] * 100
            qleft = qdb[qdb['Category']==cat].shape[0]
            xlistcats = xlistcats + "- *" + cat + "* (" + str(qleft) + " questions, " + usd(str(cash)) + ")" + "\n"

        xlistcats = xlistcats + str(qdb.shape[0]) + " questions left in the database."
        await message.channel.send('Categories you can choose:\n' + xlistcats)

    if message.content[:7] == '!deduct' and message.author.id == 279715165996318721:
        ymsg = str(message.content)
        ymsg = ymsg.split(" ")
        leaderboard_write(ymsg[2],-1,int(ymsg[1]))
        await message.channel.send(usd(ymsg[1]) + " deducted from contestant's score.")

    if message.content == '!score':
        await message.channel.send('<@!' + str(message.author.id) + ">, your current score is: " + usd(userscore(str(message.author))) + ".")

    if message.content == '!leaderboard':
        await message.channel.send(call_leaderboard())

client.run(TOKEN)
