from typing import ContextManager
import discord
from datetime import date
from datetime import datetime
import os.path
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import MemberConverter
from discord.flags import Intents
import json
import time

today = date.today()

#Bot Initialization
with open("config.json", "r") as configjsonFile:
    configData = json.load(configjsonFile)
    TOKEN = configData["token"]
    PREFIX = configData["prefix"]
    USERPATH = configData["userpath"]
    IDARRAYPATH = configData["idarraypath"]
    GUILDID = configData["guildid"]
bot = discord.Client()
bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    f = open(IDARRAYPATH, "r")
    userArray = str(f.read()).split()

    for x in range(len(userArray)):
        userID = userArray[x]
        dayFile = str(USERPATH + userID + ".txt")
        f = open(dayFile, "r")
        datearray = str(f.read()).split()
        f.close()
        decisionDate = date(int(datearray[2]), int(datearray[0]), int(datearray[1]))
        userDays = ((today - decisionDate) * -1).days

        print("Days Left: " + str(userDays))

        guild = bot.get_guild(GUILDID)
        print("Guild: " + str(guild))
        member = await guild.fetch_member(userID)
        print("Member: " + str(member))
        print("It's here: " + str(str(member.display_name).find("|")))
        newnick = ""
        if str(member.display_name).find("|") != -1:
            divider = (str(member.display_name).find("|"))
            discordName = str(member.display_name)
            newnick = discordName[0:divider] + "| " + str(userDays) + " Days"
        else: 
            divider = len(member.display_name) + 1
            discordName = str(member.display_name)
            newnick = discordName[0:divider] + " | " + str(userDays) + " Days"
        print("Added: " + str(userDays) + " Days")
        await member.edit(nick=newnick)

        #Command to check for updates every second
        while True:
            time.sleep(1) #potentially chance
        #Add method for notifcation

@bot.command()
async def set(ctx, usermonth, userdate, useryear):
    useryear = "20" + str(useryear[-2:])
    print("Year: " + str(useryear))
    dayFile = USERPATH + str(ctx.author.id) + ".txt"
    decisionDate = date(int(useryear),int(usermonth),int(userdate))
    userDays = ((today - decisionDate) * -1).days

    #Save Days
    f = open(dayFile, "w")
    f.write(str(str(usermonth) + " " + str(userdate) + " " + useryear))
    f.close()
    await ctx.channel.send("Date successfully updated. Thaaaaank yooouuuuu!")

    #Set Username
    if str(ctx.author.display_name).find("|") != -1:
        divider = (str(ctx.author.display_name).find("|"))
        discordName = str(ctx.author.display_name)
        newnick = discordName[0:divider] + "| " + str(userDays) + " Days"
    else: 
        divider = len(ctx.author.display_name) + 1
        discordName = str(ctx.author.display_name)
        newnick = discordName[0:divider] + " | " + str(userDays) + " Days"
    await ctx.author.edit(nick=newnick)
        
    #Add to database
    f = open(IDARRAYPATH, "r")
    userArray = str(f.read()).split()
    for x in userArray:
        print(x)
    if str(ctx.author.id) in userArray:
        f.close()
        print("User already in database")
    else:
        f.close()
        f = open(IDARRAYPATH, "a")        
        f.write(" " + str(ctx.author.id))
        f.close()

@bot.command()
async def date(ctx):
    userFile = USERPATH + str(ctx.author.id) + ".txt"
    f = open(userFile, "r")
    fileData = f.read()
    await ctx.channel.send("Your date is set to " + fileData)


@bot.command()
async def delete(ctx):
    userFile = USERPATH + str(ctx.author.id) + ".txt"
    os.remove(userFile)

    #Remove from database

    f = open(IDARRAYPATH, "r")
    fileData = f.read()
    fileData = fileData.replace(str(ctx.author.id), "")
    f.close()
    f = open(IDARRAYPATH, "w")
    f.write(fileData)
    f.close()

    #Set Username
    divider = (str(ctx.author.display_name).find("|"))
    discordName = str(ctx.author.display_name)
    newnick = discordName[0:divider]
    await ctx.author.edit(nick=newnick)

    await ctx.channel.send("Okaaay. I delete you :(")

bot.run(TOKEN)


