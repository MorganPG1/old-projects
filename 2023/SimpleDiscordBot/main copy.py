import discord
from discord.ext import commands
import asyncio
import requests
import random
from json_handler import main as main_json
from json_handler import other as jsonToken
from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch('REDACTED', 'REDACTED', validate_images=False)


token = jsonToken.get_token() #Use custom json_handler api to get token from token.json
client = commands.Bot(command_prefix="!", intents=discord.Intents.all()) #Set up bot
log_channel = "admin-log" #Change to change the log channel
sayAdmin = True #Change to false if say dosent need admin (DELETE LINE 74 FOR IT TO NOT NEED ADMIN, THIS ONLY CHANGES HELP PAGE DISPLAYs)

client.remove_command("help")
@client.event
async def on_ready(): #Check if bot is ready and set up presence (status)

    print("Connected bot ("+client.user.name+") to discord servers!")#Logging
    await asyncio.sleep(2) #Wait for discord to be ready for API calls
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for !help "),status=discord.Status.idle)

@client.command(name='kick')#Define command
@commands.has_permissions(kick_members=True)#Check if user has permission

async def kick(ctx, member: discord.Member, reason=None):#Define kick function
    if not isinstance(ctx.me, discord.ClientUser):#Check if not in DM
        print("User "+str(ctx.author)+" ran !cat")
        embed = discord.Embed(color=discord.Color.blue() ) #Set up embed
        embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
        embed.add_field(name="Notification", value=f"You were kicked from {ctx.guild.name} by {ctx.author.name}!")
        if reason != None:
            embed.add_field(name="Reason", value=reason)
        await member.send(embed=embed)#Send embed to kicked user
        await member.kick()#Kick user
   
        embed = discord.Embed(color=discord.Color.blue(), title="Moderation")#Set up new embed
        embed.add_field(name="Notification", value=f"User {member.mention} was kicked")
        embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
        await ctx.send(embed=embed)#Send embed to channel
        for channel in ctx.guild.channels:#Loop through all channels
            if channel.name == log_channel:#Check if log channel
                embed.add_field(name="Initiator", value=ctx.author.mention)
                await channel.send(embed=embed)#Log the kick in log channel
                return #Quit function
        embed = discord.Embed(color=discord.Color.blue() )#Set up log error message
        embed.add_field(name="Notification", value=f"Couldnt find log channel! Set up a text channel called {log_channel} for logging!")
        embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
        await ctx.send(embed=embed)#Send log error
    else:
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="Error", value="You cant issue commands in DM's")
        await ctx.send(embed=embed)

@client.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx:commands.Context):
    deleted = await ctx.channel.purge(limit=100)
    embed = discord.Embed(color=discord.Color.blue(), title="Notification")
    embed.add_field(name="Notification", value=f"Deleted {str(len(deleted))} messages!")
    await ctx.send(embed=embed)
    embed = discord.Embed(color=discord.Color.blue(), title="Notification")#Set up new embed
    embed.add_field(name="Notification", value=f"{str(len(deleted))} messages were cleared from {ctx.channel.mention}")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    for channel in ctx.guild.channels:#Loop through all channels
        if channel.name == log_channel:#Check if log channel
            embed.add_field(name="Initiator", value=ctx.author.mention)
            await channel.send(embed=embed)#Log the kick in log channel
            return #Quit function
        
    embed = discord.Embed(color=discord.Color.blue() )#Set up log error message
    embed.add_field(name="Notification", value=f"Couldnt find log channel! Set up a text channel called {log_channel} for logging!")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
    await ctx.send(embed=embed)#Send log error

@client.command(name="google")
async def google(ctx: commands.Context, term:str):
    _search_params = {
        'q': '...',
        'num': 10,
        'fileType': 'gif',
        'rights': 'cc_nonderived',
        'safe': 'safeUndefined', ##
        'imgType': 'imgTypeUndefined', ##
        'imgSize': 'imgSizeUndefined', ##
        'imgDominantColor': 'imgDominantColorUndefined', ##
        'imgColorType': 'imgColorTypeUndefined' ##
    }
    await gis.search()
    count = 0
    for image in gis.results():
        if random.randrange(1,10) == 6:
                
                embed = discord.Embed(color=discord.Color.random(), title="goofy ahh google searcher")
                embed.set_footer("probably not anything to do with what you searched but who gives a fuck")
                embed.set_image(url=image.url)
                return
        count = count+1
        print(count)

@client.command(name="say") #Define say command
@commands.has_permissions(manage_guild=True)#Check if user has permission
async def say(ctx, text:str): #Define say function
    print("User "+str(ctx.author)+" ran !cat")
    if not isinstance(ctx.me, discord.ClientUser):#Check if not in DM
        print(ctx)
        
        await ctx.send(text)
        
        for channel in ctx.guild.channels:#Loop through all channels
            if channel.name == log_channel:#Check if log channel
                embed = discord.Embed(color=discord.Color.blue())#Set up new embed
                embed.add_field(name="Notification", value=f"User used !say with message '{text}'")
                embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
                embed.add_field(name="Initiator", value=ctx.author.mention)
                await channel.send(embed=embed)#Log the command in log channel
                return #Quit function
        embed = discord.Embed(color=discord.Color.blue() )#Set up log error message
        embed.add_field(name="Notification", value=f"Couldnt find log channel! Set up a text channel called {log_channel} for logging!")
        embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
        await ctx.send(embed=embed)#Send log error
    else:
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="Error", value="You cant issue commands in DM's")
        await ctx.send(embed=embed)

@client.command("cat")#Define command cat
async def cat(ctx, id=None):#Define cat function
    if not isinstance(ctx.me, discord.ClientUser):#Check if not in DM
        print("User "+str(ctx.author)+" ran !cat")
        if isinstance(id, str): #Check if id is not None
            try:
                a = int(id) #Change from str to int
                print(a)#Logging
                cats = main_json.open_file("cat.json")#Open file of ids
                try:
                    url = cats[a] #Define url
                except IndexError: #Error handling
                    embed = discord.Embed(color=discord.Color.dark_red())
                    embed.add_field(name="Error", value="ID Invalid, to generate a new image just run !cat")
                    await ctx.send(embed=embed)
                    return
                embed = discord.Embed(color=discord.Color.blue(), title="Custom Cat") #Set up cat embed
                embed.set_image(url=url)
                embed.set_footer(text=f"This cat has id {id}. Use that with !cat {id} to see the cat again or !send-cat {id} to send it to someone!") 
                await ctx.send(embed=embed)           
            except ValueError as e:#Error handling
                embed = discord.Embed(color=discord.Color.dark_red())
                embed.add_field(name="Error", value="Python error during function cat(): "+str(e.with_traceback(None))+". Make sure you used a number as id!")
                await ctx.send(embed=embed)
                for channel in ctx.guild.channels:#Loop through all channels
                    if channel.name == log_channel:#Check if log channel
                        embed = discord.Embed(color=discord.Color.red())#Set up new embed
                        embed.add_field(name="Error Notification", value=f"User used !cat with message '{id}', resulted in: {str(e.with_traceback(None))}")
                        embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
                        embed.add_field(name="Initiator", value=ctx.author.mention)
                        await channel.send(embed=embed)#Log the command in log channel
                        return #Quit function
        else:
            cat_json = requests.get(url='https://api.thecatapi.com/v1/images/search') #Generate cat image
            print(cat_json.json()[0]["url"]) #Logging
            file = main_json.open_file("cat.json")#Open file of ids
            current_id = file[0]+1 #Get current id
            url = cat_json.json()[0]["url"]#Get url
            file.append(url)#Add url to list 
            file[0] = current_id #Update current id
            main_json.write_file(file, "cat.json")#Update file
            embed = discord.Embed(color=discord.Color.blue(), title="Random Cat")#Set up embed
            embed.set_image(url=url)
            embed.set_footer(text=f"This cat has id {current_id}. Use that with !cat {current_id} to see the cat again or !send-cat {id} to send it to someone!") 
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="Error", value="You cant issue commands in DM's")
        await ctx.send(embed=embed)        

@client.command("send-cat")#Define send-cat command
async def send_cat(ctx, user: discord.Member, id=None):#Define send-cat function
    if not isinstance(ctx.me, discord.ClientUser):#Check if not in DM
        if isinstance(id, str):#Check if None
                try:
                    a = int(id)#Change str to int 
                    print(a)#Logging
                    cats = main_json.open_file("cat.json")#Open list of ids
                    try:
                        url = cats[a]#Get url
                    except IndexError: #Error handling
                        embed = discord.Embed(color=discord.Color.dark_red())
                        embed.add_field(name="Error", value="ID Invalid, to generate a new image just run !cat")
                        await ctx.send(embed=embed)
                        return
                    embed = discord.Embed(color=discord.Color.blue(), title="You recieved a cat!", description=ctx.author.mention + f" sent a cat to you from {ctx.guild.name}!") #Set up embed
                    embed.set_image(url=url)
            
                    embed.set_footer(text=f"This cat has id {id}. Use that with !cat {id} to see the cat in the server ({ctx.guild.name})!") 
                    await user.send(embed=embed) #Send DM
                except ValueError as e: #Error handling
                    embed = discord.Embed(color=discord.Color.dark_red())
                    embed.add_field(name="Error", value="Python error during function cat(): "+str(e.with_traceback(None))+". Make sure you used a number as id!")
                    await ctx.send(embed=embed)
                    for channel in ctx.guild.channels:#Loop through all channels
                        if channel.name == log_channel:#Check if log channel
                            embed = discord.Embed(color=discord.Color.red())#Set up new embed
                            embed.add_field(name="Error Notification", value=f"User used !send-cat with message '{id}', resulted in: {str(e.with_traceback(None))}")
                            embed.set_author(name=client.user.name, icon_url=client.user.avatar.url)
                            embed.add_field(name="Initiator", value=ctx.author.mention)
                            await channel.send(embed=embed)#Log the command in log channel
                            return #Quit function     
        else:
            embed = discord.Embed(color=discord.Color.dark_red(), title="Error")
            embed.add_field(name="Error", value="No ID specified!")
            await ctx.send(embed=embed) 

    else:
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="Error", value="You cant issue commands in DM's")
        await ctx.send(embed=embed)

@client.command("help")
async def help(ctx):
    embed = discord.Embed(color=discord.Color.blue(), title="Help")
    embed.add_field(name="!clear", value="Clear messages from channel (ADMIN ONLY)")
    embed.add_field(name="!kick", value="Kick a user (ADMIN ONLY), \nargs:\n user: The user to kick in mention form (@user)\n reason (optional): The reason")
    if sayAdmin:
        embed.add_field(name="!say", value="Say text as the bot (ADMIN ONLY), \nargs:\n text: The text to say")
    else:
        embed.add_field(name="!kick", value="Say text as the bot, \nargs:\n text: The text to say")

    embed.add_field(name="!cat", value="Generate a random cat image!, \nargs:\n id (optional): Show a previously generated cat (get id from running !cat without args)")
    embed.add_field(name="!send-cat", value="Send someone in the server a cat image, \nargs:\n id: The cat to send (get id from running !cat without args)")
    await ctx.send(embed=embed)
    
@kick.error #Define what happens if user does not have kick permission
async def error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=discord.Color.dark_red())
        embed.add_field(name="Error", value="You dont have the permissions required for this (kick_members)!")
        await ctx.send(embed=embed)

@say.error #Define what happens if user does not have manage_guild permission
async def error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(color=discord.Color.dark_red()) #Set up embed
        embed.add_field(name="Error", value="You dont have the permissions required for this (manage_guild)!")
        await ctx.send(embed=embed) #Send embed
client.run(token['token'], log_handler=None) #Start bot