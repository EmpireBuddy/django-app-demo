import os
import time
import re
import simplejson as json
import random
from pathlib import Path
import discord
from discord.ext import commands

description = 'DR made another bot what a loser'
DISCORD_KEY = 'NDY1NjU4OTE0NDA3NDQ4NjEy.DiQwlQ.hOLDzfRIcfJplXpIcAGzz88bc1M'  # Nuselrosh
#DISCORD_KEY = 'NDY2MDMwNDI2NTcwMzU4Nzg1.DiWILg.KRJGw0py9mhg2yyerTu4313rJ-w' #BooBoo

bot = commands.Bot(command_prefix='!',
                   description=description)

DR_ID = "300807211674894346"

root_path = os.path.abspath(os.path.dirname(__file__))
locations_path = "/locations/"
state={
    "game":-1,
    "play":0,
    "turn":-1,
}
goals = {
    "max":5,
    "scored":0
}
players=[]
game_locations = {}

def init_game(ctx):
    message = ctx.message
    guild = message.guild
    ret = False
    if state["game"]>-1:
        return "ERR (#0hdy) - This game is already initialized"


    if str(message.author.id) == DR_ID:
        try:
            print("Initializing Hide and Go Veto Game")
            print("Load House Locations")
            load_house_locations()
            print("Building Channels")
            build_channels(guild)


            print("Setting Game State")
            state["game"] = 0
            ret = True
        except:
            ret = "ERR (#0hn3) - Could not load or parse locations"
    else:
        ret = "ERR (#0hdf) - Sorry I only !init for DR"

    return ret

    

def load_house_locations():
    with open("locations.json") as f:
        locations = json.load(f)
        for l in locations:
            game_locations[l["name"]] = []
            for s in l["locations"]:
                var gameloc = **s, **{"searched": 0}}
                game_locations[l]["name"].append(gameloc)
                Path(root_path + locations_path + s["id"].lower()).touch()


def build_channels(guild):for l in locations:
    for room in game_locations as r:
        guild.create_text_channel(r)

def begin_game(message):
    ret = False
    if state["game"] < 0:
        return "ERR(#0hna) - You cant begin before you !init"
    elif state["game"] > 1:
        return "ERR(#0hna) - This game has already !begin"

    if str(message.author.id) == DR_ID:
        try:
            print("Start the game")
            # print("Load the player list")
            # load_players()
            print("Setting Play State")
            state["play"] = 1
            print("Setting Turn State")
            state["turn"] = 0
            print("Setting Game State")
            state["game"] = 1
            ret = True
        except:
            ret="ERR (#0hn3) - Could not begin the game properly"
    else:
        ret="ERR (#0hn8) - Sorry I only !begin for DR"
    return ret

def stop_game():
    state["play"] = 0

def find_next_player():
    pass


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command(pass_context=True)
async def init(ctx):
    could_init = init_game(ctx)
    if could_init == True:
        await ctx.send("Initialized!")
    elif could_init is str:
        await ctx.send(could_init)
    else:
        await ctx.send("ERR (#0hn0) - There was some unspecificed error")
               

@bot.command(pass_context=True)
async def begin(ctx):
    could_begin = begin_game(ctx.message)
    if could_begin == True:
        await ctx.send("The game started correctly.  Lets go get the first player")
    elif could_begin is str:
        await ctx.send(could_begin)
    else:
        await ctx.send("ERR (#0hn0) - There was some unspecificed error")


@bot.command(pass_context=True)
async def die(ctx):
    if str(ctx.message.author.id) == DR_ID:
        ctx.send("How could you")
        state = {
            "game": -1,
            "play": 0,
            "turn": -1,
        }
    else:
        ctx.send("ERR (#000f) - I don't love you that much")
    exit()



@bot.event
async def on_message(message):
    with open("messages.log", "a") as f:
        f.write(json.dumps(str(message.author) + " - " +
                           str(message.author.id) + " - " + 
                           str(message.author.roles) + " - " +
                           str(message.content) + 
                           "\n"
        ))





@bot.event
async def on_command_error(ctx,error):
    print(str(error))



bot.run(DISCORD_KEY)
 
