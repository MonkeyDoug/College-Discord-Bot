#!/usr/bin/env python3

# Imports
import os
import discord
import time
# from dotenv import load_dotenv
from bs4 import BeautifulSoup
import disc_commands

# Function for obtaining and formatting uptime for discord
def uptime(message):
    # Obtains uptime by getting difference between time from program start and current time
    up = time.time() - start_time
    # Returns time in days if time uptime is larger than a day"
    if up/60/60/24 >= 1:
        up = '__**Uptime:**__ ' + str(round(up/60/60/24,2)) + ' Days'
    # Returns time in hours if time uptime is larger than a hour"
    elif up/60/60 >=1 :
        up = '__**Uptime:**__ ' + str(round(up/60/60,2)) + ' Hours'
    # Returns time in minutes if time uptime is larger than a minute"
    elif up/60 >= 1:
        up = '__**Uptime:**__ ' + str(round(up/60,2)) + ' Minutes'
    # Returns time in days if time uptime is larger than a day"
    else:
        up = '__**Uptime:**__ ' + str(round(up,2)) + ' Seconds'
    return up

def get_ping(message):
    return '__**Ping:**__ ' + str(round(client.latency*1000,2)) + ' ms'

def search(message,args):
    link = 'https://www.collegedata.com/college-search/'
    college = message.content.lower()[9:]
    college = college.replace(' ','-')
    request = link + str(college)

    return disc_commands.scraping(request,args)

call_names = ['stats','college','help']
commands = { 'uptime' : uptime , 'ping' : get_ping}

# load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    global start_time
    start_time = time.time()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    split = msg.lower().split(' ')

    if split[0] == '!':
        return

    if len(split) > 1:
        args = split[1:]
        arg_wanted = split[1]

    command = split[0].replace('!','')

    if msg.startswith('!'):
        if command not in call_names:
            await message.channel.send('Command not found, please check documentation in !help')
            return
        elif command == 'help':
                print('Call Recieved From: ' + str(message.author) + ' Command: ' + msg.lower())
                await message.channel.send("```Street Smart Gaming Discord Bot\nMade by Douglas Chen\nCommand Prefix: !\nCommands:\n!college Returns stats on college\n>>> Arguments: <Name of College> <Data Wanted>\n>>> Usage: !college University of Pennsylvania\n>>> Possible Values for Data Wanted: Default/None: all 'all' 'description' 'averages' 'early' 'admission rate' 'cost of attendance' 'mascot' 'popular': 'special'\n!stats\n!help```")
                return
        elif len(split) == 1:
            await message.channel.send('No arguments found, please check documentation in !help for arguments')
            return
        else:
            if command == 'college':
                print('Call Recieved From: ' + str(message.author) + ' Command: ' + msg.lower())
                returned = search(message,args)
                if isinstance(returned,str):
                    await message.channel.send(returned)
                elif len(returned) > 1:
                    for array in returned:
                        await message.channel.send(array)

            if command == 'stats':
                print('Call Recieved From: ' + str(message.author) + ' Command: ' + msg.lower())
                await message.channel.send(commands[arg_wanted](message))

client.run(TOKEN)

# To Do
# Finish other college data
# Make dict and dynamically find commands ex "!college" and "!stats"
# Add Docs
# Fix Aggregated Output
# Add Better Time Outputs
# @ Person who sent command before sending output
# @ bot would send message and help page
# Blacklist certain guilds from certain commands
