from datetime import datetime
from typing import Any, Literal
import discord
from discord.ext import commands
from blackjack import BlackjackGame
import config 
import json
import random
import enum
bot = commands.Bot("/", intents=discord.Intents.all())
guilds = []
tree = bot.tree
blackjackGames = {}
class HeadsOrTails(str, enum.Enum):
    heads = "heads"
    tails = "tails"
class RPS(str, enum.Enum):
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
#--------------------------# Data loading
data = open("db.json", "r")
db =  json.load(data)
data.close()
#--------------------------#
def save():
    print("aaaaaaaaaaaaaa")
    db2 = json.dumps(db)
    print(db2)
    print(db)
    data = open("db.json", "w")

    data.write(db2)
    
    data.close()
botname = "MorganPG Bot"
version = "release beta 1"


blacklist = ["https://tenor.com/view/meme-down-syndrome-funny-tongue-action-tongue-out-meme-gif-572114404054760484", 
             "https://tenor.com/view/super-mario-twerk-dance-gif-16007386",
             "https://tenor.com/view/freaky-tree-gif-5339980723356097006",
             "https://tenor.com/view/this-is-so-sad-gif-25352430",
             "https://tenor.com/view/trash-cans-dancing-trash-cans-trash-can-dancing-trash-can-shut-up-gif-24101099"]
class BaseEmbed(discord.Embed):
    successColor = discord.Color.green()
    failureColor = discord.Color.red()
    infoColor = discord.Color.blue()
    def __init__(self, *, colour: int | discord.Colour | None = None, color: int | discord.Colour | None = None, title: Any | None = None, type: Literal['rich'] | Literal['image'] | Literal['video'] | Literal['gifv'] | Literal['article'] | Literal['link'] = 'rich', url: Any | None = None, description: Any | None = None, timestamp: datetime | None = None):
        
        
        super().__init__(colour=colour, color=color, title=title, type=type, url=url, description=description, timestamp=timestamp)
        self.set_footer(text=botname+" | Version: "+version)


def getCredits(guild: discord.Guild,user: discord.User):
    gid = str(guild.id)
    uid = str(user.id)

    if gid in db:
        if uid in db[gid]:
            cred = db[gid][uid]
            return cred
        else:
            db[gid][uid] = 250
            save()
            return 250
    else:
        db[gid] = {}
        db[gid][uid] = 250
        save()
        return 250

        
def setCredits(guild:discord.Guild, user: discord.User, credits):
    gid = str(guild.id)
    uid = str(user.id)
    print(credits)
    if gid in db:
        if uid in db[gid]:
            print("a")
            db[gid][uid] = credits
            save()
            
            print("saved")
            return getCredits(guild=guild,user=user)
        else:
            print("aa")
            db[gid][uid] = 250+credits
            save()
            return 250+credits
    else:
        print("aaaa")
        db[gid] = {}
        db[gid][uid] = 250+credits
        save()
        return 250+credits
def CreateEmbed(title, description, color):
    return BaseEmbed(title=title, color=color, description=description)

def ping(id):
    return f"<@{id}>"

def channelPing(id):
    return f"<#{id}>"
@bot.event
async def on_ready():
    global guilds
    for guild in bot.guilds:
        print(guild.name, "-",guild.member_count,"members")
        guilds.append(guild)    
    print(guilds)
    await tree.sync()

@tree.command()
async def info(ctx: commands.Context|discord.Interaction):
    embed = BaseEmbed(
        title="Info",
        description=f"Information for {botname} and {ctx.guild.name}",
        color=BaseEmbed.infoColor
    )
    num_channels = 0
    for channel in ctx.guild.channels:
        if not isinstance(channel, discord.CategoryChannel):
            num_channels += 1
    embed.add_field(name="Number of channels:",value=f"`{str(num_channels)}`")
    embed.add_field(name="Number of members:",value=f"`{str(ctx.guild.member_count)}`")
    embed.add_field(name="Bot version:", value=f"`{version}`")
    embed.add_field(name="Number of servers bot is in:", value=f"`{str(len(bot.guilds))}`")
    await ctx.response.send_message(content=ping(ctx.user.id), embed=embed )

@tree.command()
async def credits(ctx: commands.Context|discord.Interaction):
    
    
        embed = CreateEmbed("Credits for "+ctx.user.display_name, "You have "+str(getCredits(ctx.guild, ctx.user))+" credits", color=BaseEmbed.infoColor)

        await ctx.response.send_message(content=ping(ctx.user.id), embed=embed)

@tree.command()

async def add_credits(ctx: commands.Context|discord.Interaction, user:discord.User, credits:int):
    if ctx.user.guild_permissions.administrator:
        setCredits(ctx.guild, user, getCredits(ctx.guild, user)+credits)
        
        embed = CreateEmbed(
            "Added credits",
            "The user "+user.display_name+" now has "+str(getCredits(ctx.guild, user))+" credits",
            BaseEmbed.successColor,
        )
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
    else:
        await ctx.response.send_message("You do not have permissions")

@add_credits.error
async def addcreditserror(error, ctx:discord.Interaction):
    if isinstance(error,commands.MissingPermissions):
        await ctx.response.send_message("You dont have the permission to do this "+ping(ctx.user.id))

@tree.command()
async def coinflip(ctx: commands.Context|discord.Interaction, credits:int, head:HeadsOrTails):

    cred = getCredits(ctx.guild, ctx.user)
    if cred >= credits:
        setCredits(ctx.guild, ctx.user, credits=cred-credits)
        sequence = ["heads", "tails","tails","heads","heads", "tails","tails","heads","heads", "tails","tails","heads","heads", "tails","tails","heads",]
        chance = random.choice(sequence)
        if chance == head:
            embed = CreateEmbed("Win!", "You won "+str(credits)+" credits!", BaseEmbed.successColor)
            setCredits(ctx.guild,ctx.user, cred+credits)
        else:
            embed = CreateEmbed("You lost!", "You lost! Play again?", BaseEmbed.failureColor)
        
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
        
    else:
        print(cred, credits, cred>=credits)
        embed = CreateEmbed("Error", "You do not have enough credits.", BaseEmbed.failureColor)
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
        

@tree.command()
async def rockpaperscissors(ctx: commands.Context|discord.Interaction, credits:int, rps:RPS):

    cred = getCredits(ctx.guild,ctx.user)
    if cred >= credits:
        setCredits(ctx.guild, ctx.user, credits=cred-credits)
        sequence = ["rock", "paper","scissors","rock","paper", "scissors","rock","scissors","rock", "paper","scissors","rock","paper", "scissors"]
        chance = random.choice(sequence)
        if (chance == "rock" and rps == "paper") or (chance == "paper" and rps == "scissors") or (chance == "scissors" and rps == "rock"):
            embed = CreateEmbed("Win!", "You won "+str(credits)+" credits! I picked "+chance, BaseEmbed.successColor)
            setCredits(ctx.guild, ctx.user, cred+credits)
        elif chance == rps:
            setCredits(ctx.guild, ctx.user,cred)
            embed = CreateEmbed("You tied!", "Credits returned! Play again?", BaseEmbed.infoColor)
        else:
            embed = CreateEmbed("You lost!", "I picked "+chance+"! Play again?", BaseEmbed.failureColor)
        
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
        
    else:
        print(cred, credits, cred>=credits)
        embed = CreateEmbed("Error", "You do not have enough credits.", BaseEmbed.failureColor)
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
        
@tree.command()
async def purge(ctx: discord.Interaction):
    if ctx.user.guild_permissions.manage_messages:
        msgs = ctx.channel.history(limit=25)
        async for msg in msgs:
            await msg.delete() 
    else:
        await ctx.response.send_message("You do not have permissions")


@tree.command()
async def blackjack(ctx:discord.Interaction, credits:int):
    cred = getCredits(ctx.guild,ctx.user)
    if cred >= credits:
        setCredits(ctx.guild,ctx.user, cred-credits)
        if ctx.guild_id in blackjackGames:
            blackjackGames[ctx.guild_id][ctx.user.id] = BlackjackGame(credits)
        else:
            blackjackGames[ctx.guild_id] = {}
            blackjackGames[ctx.guild_id][ctx.user.id] = BlackjackGame(credits)
        
        embed = BaseEmbed(title="Blackjack", description="respond with hit or stay", color=BaseEmbed.infoColor)
        cardNames = {"A": "Ace", "K": "King", "J": "Jack", "Q":"Queen"}
        playerDeck = ""
        for card in blackjackGames[ctx.guild_id][ctx.user.id].userCards:
            if isinstance(card, int):
                playerDeck += str(card)+", "
            else:
                playerDeck += cardNames[card]+", "
        
        embed.add_field(name=f"Your deck {blackjackGames[ctx.guild_id][ctx.user.id].userHand}", value=f"`{playerDeck}`")
        dealerDeck = ""
        for card in blackjackGames[ctx.guild_id][ctx.user.id].dealerCards:
            if isinstance(card, int):
                dealerDeck += str(card)+", "
            else:
                dealerDeck += cardNames[card]+", "
        
        embed.add_field(name="Dealers deck", value=f"`{dealerDeck}`")
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)
    else:
        print(cred, credits, cred>=credits)
        embed = CreateEmbed("Error", "You do not have enough credits.", BaseEmbed.failureColor)
        await ctx.response.send_message(ping(ctx.user.id), embed=embed)

@bot.event
async def on_message(ctx:discord.Message):
    if ctx.content == "hit" or ctx.content == "stay" and ctx.guild.id in blackjackGames:
        if ctx.author.id in blackjackGames[ctx.guild.id]:
            if not blackjackGames[ctx.guild.id][ctx.author.id].finished:
                if ctx.content == "hit":
                    frame = blackjackGames[ctx.guild.id][ctx.author.id].NextFrame(True)
                else:
                    frame = blackjackGames[ctx.guild.id][ctx.author.id].NextFrame(False)
                
                credits2 = blackjackGames[ctx.guild.id][ctx.author.id].credits
                print(frame)
                if frame["GameStatus"] == "win":
                    embed = CreateEmbed("You win!", "You won "+str(credits2)+" credits!", BaseEmbed.successColor)
                    setCredits(ctx.guild, ctx.author, getCredits(ctx.guild, ctx.author) + credits2*2)
                elif frame["GameStatus"] == "lost":
                    embed = CreateEmbed("You lost!", "You lost! Play again?", BaseEmbed.failureColor)
                elif frame["GameStatus"] == "bust":
                    embed = CreateEmbed("You lost!", "You bust! Play again?", BaseEmbed.failureColor)
                elif frame["GameStatus"] == "dealerBust":
                    embed = CreateEmbed("You won!", "Dealer Bust! You won "+str(credits2)+" credits!", BaseEmbed.successColor)
                    setCredits(ctx.guild, ctx.author, getCredits(ctx.guild,ctx.author) + credits2*2)
                else:
                    embed = BaseEmbed(title="Blackjack", description="respond with hit or stay", color=BaseEmbed.infoColor)
                    cardNames = {"A": "Ace", "K": "King", "J": "Jack", "Q":"Queen"}
                    playerDeck = ""
                    for card in blackjackGames[ctx.guild.id][ctx.author.id].userCards:
                        if isinstance(card, int):
                            playerDeck += str(card)+", "
                        else:
                            playerDeck += cardNames[card]+", "
                    
                    embed.add_field(name=f"Your deck {blackjackGames[ctx.guild.id][ctx.author.id].userHand}", value=f"`{playerDeck}`")
                    dealerDeck = ""
                    for card in blackjackGames[ctx.guild.id][ctx.author.id].dealerCards:
                        if isinstance(card, int):
                            dealerDeck += str(card)+", "
                        else:
                            dealerDeck += cardNames[card]+", "
                    
                    embed.add_field(name="Dealers deck", value=f"`{dealerDeck}`")
                await ctx.reply(ping(ctx.author.id), embed=embed)
    else:
        for i in blacklist:
            if ctx.content.startswith(i):
                await ctx.delete()
                    
    
bot.run(config.token)
