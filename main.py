import discord
from discord import activity
from discord.embeds import Embed
from discord.enums import ActivityType
from discord.ui import Button, View
from discord.ext import commands
import random


token = "OTEyOTY3MDU2NTU3NzU2NDI2.YZ3o1A.Jp-cyPdENu4bG_y-sEl16iMYp2o"

bot = commands.Bot(command_prefix=">", intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle , activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} Servers | we need more "))
    print("Logged in as \n{0.user}".format(bot))
    print("-------------------------------------------------")


@bot.command()
@commands.has_permissions(administrator=True)
async def sotd(ctx, channel: discord.TextChannel):
    em = discord.Embed(title="Song Of The Day <a:pepedance:920462135774027816>", description="**[40 days - Andrew Garden](https://open.spotify.com/track/3qve4a8uPsuWrZrkmtO9Dq?si=1425da64dd3644d4)**")
    em.add_field(name="Feedback:", value="**Indeed, 40 days does feel like years**", inline=True)
    await channel.send(embed=em)

@sotd.error
async def sotd_error(ctx, error):
    channel = bot.get_channel(922807631784050698)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<a:siren:922358771735461939> You can't use this command! Command requires ``Adminstrator`` Permissions!! <a:siren:922358771735461939>")
        await channel.send(f"Command ``sotd`` was attempted \n User Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------")


@bot.command(aliases=['BotUpdate', 'Update', 'Botnews', 'botnews', 'update'])  
@commands.has_permissions(administrator=True)
async def botupdate(ctx,channel: discord.TextChannel):
    embed = discord.Embed(title=f"New Update", description="New Commands ✅")
    embed.add_field(name="**__Moderation__**", value="2 New Commands ✅")
    embed.add_field(name=" - Mute", value=" Usage: ``>mute @anyone Reason``", inline=False)
    embed.add_field(name=" - Unmute", value="Usage: ``>unmute @anyone`` ", inline=False)
    embed.add_field(name="**__General__**", value="New command ✅")
    embed.add_field(name=" - Ping Command", value="Usage: ``>ping``", inline=False)
    embed.set_footer(text="Updated 12/19/21")
    await channel.send(f"<a:siren:922358771735461939> BOT NEWS  || {ctx.message.guild.default_role} || <a:siren:922358771735461939> ")
    await channel.send(embed=embed)

@botupdate.error
async def botupdate_error(ctx, error):
    channel = bot.get_channel(922807631784050698)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<a:siren:922358771735461939> You can't use this command! Command requires ``Adminstrator`` Permissions!! <a:siren:922358771735461939>")
        await channel.send(f"Command ``botupdate`` was attempted \n User Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------")


#Moderation Section
@bot.command(description="Mutes Member")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
        
        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        
    embed =  discord.Embed(title="❌ Muted", description=f"{ctx.author.mention} Muted {member.mention}", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f'You have been muted from {guild.name}! \n Reason: {reason}')




@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   guild = ctx.guild
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
   
   await member.remove_roles(mutedRole)
   await member.send(f" you have unmuted from: {ctx.guild.name}")
   embed = discord.Embed(title="✅ Unmuted!", description=f"Unmuted {member.mention}",colour=discord.Colour.light_gray())
   await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong :ping_pong:", description = f"My latency is: {round(bot.latency * 1000)}ms", color=0x5d63c0)
    embed.set_footer(text= f'Requested By {ctx.author}')
    await ctx.send(embed = embed)
    

@bot.command(aliases=['whois'])
async def userinfo(ctx,member: discord.Member = None):
   if member == None:
        member = ctx.author  

   embed = discord.Embed(title=f"Info About ``{member}``", description=f"-----------------------------------------------------------")
   embed.set_thumbnail(url=member.avatar.url)
   embed.add_field(name=f"{member} was created at:", value=f"``{member.created_at.date()}``".replace("-", "/"), inline=False)
   embed.add_field(name=f"{member}'s User ID:", value=f"``{member.id}``", inline=False)
   embed.add_field(name=f"{member} Join Server Date", value=f"``{member.joined_at.date()}``".replace("-", "/"), inline=False)
   embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar)

   await ctx.send(embed=embed)     


@bot.command(aliases=['servers', 'Servers', 'botservers'])
async def server(ctx):
    embed=discord.Embed(title="Server Count", description="Amount Of Servers Bot Is In")
    embed.add_field(name=f"I'm in: ", value=f"**{str(len(bot.guilds))} Servers**", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def howgay(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    embed=discord.Embed(title="how gay are you!!!", description=f"**{member.mention} is {random.randint(0,100)}% homosexual🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈**")
    embed.set_image(url='https://media.discordapp.net/attachments/814362660622958644/913686144753991710/FCuz4ydWYAM9oaZ.jpg')
    await ctx.send(embed=embed) 

@bot.command(aliases=['howsussy', 'howsussybaka'])
async def howsus(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    CHOICES = ['``yeah`` <a:noooo:910736617529036830>', '``no ``<:gary:913247181106995271>', '``maybe ``<:maybe:923015512630382623>']

    embed=discord.Embed(title=f"**Is The User {member} Sussy???**", description=f"\u200b")
    embed.add_field(name=f"**The Answer Is:** \u200b", value=f"**\u200b {random.choice(CHOICES)}** ")
    embed.set_image(url="https://raw.githubusercontent.com/callimarieYT/CalliWebsite/main/unnamed_1.png")
    embed.set_footer(text=f"Requested By {member}", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)
 
@bot.command(aliases=['clear'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit: int):
    await ctx.channel.purge(limit=limit)
    embed=discord.Embed(title="Cleared", description=f"**``{limit} Messages``**")
    embed.set_footer(text=f'Requested By {ctx.author}', icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)

@purge.error
async def purge_error(ctx, error):
    channel = bot.get_channel(922807631784050698)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<a:siren:922358771735461939> You can't use this command! Command requires ``Manage Messages`` Permissions! <a:siren:922358771735461939>")
        await channel.send(f"Command ``purge`` was attempted \n User Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------") 

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    if reason == None:
        reason="No Reason Specified" 

    
    await member.ban(reason=reason)
    await member.send(f'You Have Been Banned From {ctx.guild.name} for \n {reason}')
    embed = discord.Embed(title=f"succesfully banned {member.name} from this server", description=f"Reason: {reason}\nBy: {ctx.author.mention}")  
    await ctx.send(embed=embed)
   

   



@ban.error
async def ban_error(ctx, error):
    channel = bot.get_channel(922807631784050698)   
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"<a:siren:922358771735461939> You can't use this command! Command requires ``Ban Members`` Permissions! <a:siren:922358771735461939>")
        await channel.send(f"Command ``Ban`` was attempted \n User Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------") 

@bot.command()
async def unban(ctx, *, user=None):

    try:
        user = await commands.converter.UserConverter().convert(ctx, user)
    except:
        await ctx.send("Error: user could not be found!")
        return

    try:
        bans = tuple(ban_entry.user for ban_entry in await ctx.guild.bans())
        if user in bans:
            await ctx.guild.unban(user, reason="Responsible moderator: "+ str(ctx.author))
        else:
            await ctx.send("User not banned!")
            return

    except discord.Forbidden:
        await ctx.send("I do not have permission to unban!")
        return

    except:
        await ctx.send("Unbanning failed!")
        return

    embed=discord.Embed(title="Successfully unbanned", description=f"{user.mention}")
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(title="Commands can be found here", description="\n**http://hacked-my.email/discord.html** I own the website btw")
    await ctx.send(embed=embed)
 






bot.run(token)