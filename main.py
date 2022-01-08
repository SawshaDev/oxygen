import discord
from discord.ext import commands

import os


cogs_folder="./cogs"





token = ""



prefixes = ['>', '-', ',']


bot = commands.Bot(command_prefix=prefixes , intents=discord.Intents.all())
bot.remove_command('help')



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle , activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} Servers!"))
    print("Logged in as \n{0.user}".format(bot))
    print("-------------------------------------------------")


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')
    
  else:
    print(f'Unable to load {filename[:-3]}')


bot.run(token)  

