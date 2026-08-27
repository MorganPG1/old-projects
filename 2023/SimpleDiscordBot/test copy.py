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
        if message.content == "!user":
            embed = discord.Embed(color=discord.Color.random(),title="User info for" + message.author.name)
            embed.add_field(name="Username", value=message.author.name)
            embed.add_field(name="Nickname", value=message.author.nick)
            embed.add_field(name="ID", value=message.author.id)
            await message.channel.send(embed=embed)
        else:
            if message.content[0:5] == "!kick":
                user = message.content [6:100]
                print(user)
                


client.run(token['token'], log_handler=None)