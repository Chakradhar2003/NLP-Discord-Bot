import discord
from discord.ext import commands
from discord import Member
from discord.ext.commands import has_permissions,MissingPermissions
import requests

token = "MTI3NDgzMDcwNzg1OTkxOTAwOQ.G_gwxl.U4M9R3YCZwUau6lnJY8AqJIMD7zixXrKZZxdaY"
bot=commands.Bot(command_prefix="!",intents=discord.Intents.all())
threshold = 50

@bot.event
async def on_ready():
    print("Success: Bot is online")

@bot.event
async def on_message(msg):
    if msg.author!=bot.user:
        message_content = msg.content
        
        if(len(message_content.strip())==0):
            return
        
        # Checking for spam data
        data = {'input_value':message_content}
        response = requests.post(url, json=data)
        url = 'http://127.0.0.1:5000/compute'
        if response.status_code == 200:
            result = response.json()
            if result['result'] == "spam":
                await msg.delete()
                await msg.channel.send("Don't send that again otherwise there will be actions")
                user_mention = msg.author.mention
                await msg.channel.send(f"Hello {user_mention}!, Please don't spam")
                return 
        else:
            print(f"Failed to call API. Status code: {response.status_code}, Error: {response.text}")
        

        # Checking for toxicity
        data = {'input_value':message_content}
        response = requests.post(url, json=data)
        url = 'http://127.0.0.1:5000/compute'
        toxicity=0
        if response.status_code == 200:
            result = response.json()
            toxicity = int(result['result']) 
        else:
            print(f"Failed to call API. Status code: {response.status_code}, Error: {response.text}")
        
        if(toxicity<threshold):
            return
        
        # Personal Warning
        if threshold<=toxicity<=0.6 :
            # Send a direct warning to the user
            await msg.author.send("Hello! This is a warning for the recent message sen't by you.")
        
        # sending three warning messages
        elif 0.6<toxicity<=0.8 :
        
        # Create logic for data retriveal from Mongo DB 
            await msg.delete()
            await msg.channel.send("Don't send that again otherwise there will be actions")
    await bot.process_commands(msg)

@bot.command()
async def hello(ctx):
    username = ctx.message.author.mention
    await ctx.send("Hello "+ username)

bot.run(token)


# intents = discord.Intents.default()
# intents.message_content = True 
# client = discord.Client(intents=intents)

# @client.event
# async def on_ready():
#     print(f"Bot logged as {client.user}")

# @client.event
# async def on_message(msg):
#     if msg.author!=client.user:
#         if msg.content.lower().startswith("?hi"):
#             await msg.channel.send(f"Hi, {msg.author.display_name}")

# client.run(token)

