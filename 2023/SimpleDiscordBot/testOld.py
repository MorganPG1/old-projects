import discord
from json_handler import other as jsonToken
client = discord.Client(intents=discord.Intents.all())
token = jsonToken.get_token()

@client.event
async def on_ready():
    print("connected")
@client.event
async def on_message(message):
    if message.author != client.user:
       
       await message.channel.send(message.author.name + ": "+message.content)

client.run(token['token'], log_handler=None)