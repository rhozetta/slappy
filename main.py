#!/usr/bin/env python3

import discord
from discord.ext.commands import bot
import json

with open("tokenfile", "r") as tokenfile:
    token=tokenfile.read()

client = discord.Client()

statslappedfile = open("statslapped.json", "rt")
statslapped = json.loads(statslappedfile.read())
statslappedfile.close()

statslapfile = open("statslap.json", "rt")
statslap = json.loads(statslapfile.read())
statslapfile.close()

async def saveslapstats(saved, slappednum, slapnum):
    
    id = int(saved.id)


    try:
        statslapped[id] += slappednum
        statslap[id] += slapnum
    except KeyError:
        
        statslapped[id] = 0
        statslap[id] = 0

        statslapped[id] += slappednum
        statslap[id] += slapnum

    statslapfile = open("statslap.json", "wt")
    statslapfile.write(json.dumps(statslap))
    statslapfile.close()

    statslappedfile = open("statslapped.json", "wt")
    statslappedfile.write(json.dumps(statslapped))
    statslappedfile.close()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the beautiful sound of slaps"))
    print('hello world')

@client.event
async def on_message(message):
    if message.content.startswith("!slap"):
        
        slapper = message.author
        
        slapped = message.mentions
        
        if message.mention_everyone:
            await message.channel.send(f"{slapper.name} slapped everyone! what a powermove!")

            await saveslapstats(saved=slapper, slappednum=0, slapnum=len(message.guild.members))

        elif message.mentions == []:
            if (message.content[5:] != ""):
                await message.channel.send(f"{slapper.name} slapped {message.clean_content[6:]}")
                await saveslapstats(saved=slapper, slappednum=0, slapnum=1)

            else:
                await message.channel.send(f"{slapper.name} slapped the air")

        elif slapped[0] == slapper:
            await message.channel.send(f"{slapper.name} slapped themself")
            await saveslapstats(saved=slapper, slappednum=1, slapnum=1)

        elif slapped[0] == client.user:
            await message.channel.send("You cant slap me, I'm unslapable!")

        else:
            await message.channel.send(f"{slapper.name} slapped {slapped[0].name}")
            await saveslapstats(saved=slapper, slappednum=0, slapnum=1)
            await saveslapstats(saved=slapped, slappednum=1, slapnum=0)

client.run(token)