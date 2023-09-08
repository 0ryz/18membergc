import discord, os
from discord.ext import commands
from colorama.initialise import init
from colorama import Fore, Style
import json

class COLORS:
    r = Fore.LIGHTRED_EX
    g = Fore.LIGHTGREEN_EX
    b = Fore.LIGHTBLUE_EX
    m = Fore.LIGHTMAGENTA_EX
    c = Fore.LIGHTCYAN_EX
    y = Fore.LIGHTYELLOW_EX
    w = Fore.RESET

def cls():
    # Clear console for Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # Clear console for macOS and Linux
    else:
        _ = os.system('clear')
    guilds = len(bot.guilds)
    botusr = str(bot.user)
    user = botusr.replace("#0", "")
    print(f'''
                                    {COLORS.b} ____                  ____   ____ 
                                    {COLORS.b}|  _ \  _ __   ___    / ___| / ___|
                                    {COLORS.b}| |_) || '__| / _ \  | |  _ | |    
                                    {COLORS.b}|  __/ | |   | (_) | | |_| || |___ 
                                    {COLORS.b}|_|    |_|    \___/   \____| \____|
                                   
                                     
                                    {COLORS.r}------------------------------------

                            {Fore.RESET}Logged in as {user}
                            ID: {bot.user.id}
                            Prefix: !
                            Servers: {guilds}

                                              {COLORS.m}Skidded by ryz{Fore.RESET}
''')

with open("config.json", "a+") as f:
    e = json.load(f)

if e["token"] != "":
    TOKEN = e["token"]
else:
    TOKEN = input("Enter your token: ")
    e["token"] = TOKEN
    with open("config.json", "w") as f:
        json.dump(e, f)

bot = commands.Bot(command_prefix='!')

global groupchat1_id
global groupchat2_id

def gcs():
    with open("config.json", "a+") as f:
        e = json.load(f)
        if e["groupchat1_id"] != "" and e["groupchat2_id"] != "":
            groupchat1_id = e["groupchat1_id"]
            groupchat2_id = e["groupchat2_id"]
        else:
            groupchat1_id = input("gc 1 id: ")
            groupchat2_id = input("gc 2 id: ") ################ AAAAAAAAAAA kil self
            e["groupchat1_id"] = groupchat1_id
            e["groupchat2_id"] = groupchat2_id
            with open("config.json", "w") as f:
                json.dump(e, f)

gcs()

@bot.event
async def on_ready():
    cls()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.channel.id == groupchat1_id:
        groupchat2 = bot.get_channel(groupchat2_id)

        content = message.content
        if message.attachments:
            attachment_link = message.attachments[0].url
            content += f"\nAttachment: {attachment_link}"

        if message.reference and message.reference.cached_message:
            reply_author = message.reference.cached_message.author.name
            reply_author_id = message.reference.cached_message.author.id
            content = f'(Replying to [{reply_author}](discord://-/users/{reply_author_id}))  {content}'
            

        await groupchat2.send(f'[{message.author.name}](discord://-/users/{message.author.id}):  {content}')
    elif message.channel.id == groupchat2_id:
        groupchat1 = bot.get_channel(groupchat1_id)

        content = message.content
        if message.attachments:
            attachment_link = message.attachments[0].url
            content += f"\nAttachment: {attachment_link}"

        if message.reference and message.reference.cached_message:
            reply_author = message.reference.cached_message.author.name
            reply_author_id = message.reference.cached_message.author.id
            content = f'(Replying to [{reply_author}](discord://-/users/{reply_author_id}))  {content}'

        await groupchat1.send(f'[{message.author.name}](discord://-/users/{message.author.id}):  {content}')
        
    await bot.process_commands(message)

@bot.command()
async def reply(ctx, *, message):
    if ctx.channel.id == groupchat1_id:
        groupchat2 = bot.get_channel(groupchat2_id)
        await groupchat2.send(f'{ctx.author.name} (replying to {ctx.message.reference.cached_message.author.name}): {message}')
    elif ctx.channel.id == groupchat2_id:
        groupchat1 = bot.get_channel(groupchat1_id)
        await groupchat1.send(f'{ctx.author.name} (replying to {ctx.message.reference.cached_message.author.name}): {message}')

bot.run(TOKEN)
