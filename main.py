import discord
from discord import activity
from discord.embeds import Embed
from discord.enums import ActivityType
from discord.ext.commands.core import has_permissions
from discord.ui import Button, View
from discord.ext import commands
import random

from discord.utils import valid_icon_size


token = "OTEyOTY3MDU2NTU3NzU2NDI2.YZ3o1A.jjrZuFapNgDgIo7nfN_xCBDeF_E"

prefixes = ['>', '.', '-', ',', '!']

bot = commands.Bot(command_prefix=prefixes, intents=discord.Intents.all())
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
    
    if member == ctx.author:
        await ctx.send('you cannot mute yourself!')
    else:
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
    
   embed = discord.Embed(title="✅ Unmuted!", description=f"Unmuted {member.mention}",colour=discord.Colour.light_gray())
   
   if member != mutedRole:
       await ctx.send("This user isn't Muted!")
   else:
       await member.remove_roles(mutedRole)
       await ctx.send(embed=embed)
       await member.send(f"you have unmuted from: {ctx.guild.name}")
   


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
    embed=discord.Embed(title="Server Count", description=f"**I am in {str(len(bot.guilds))} servers <:chad:923554621597818901>**")
    await ctx.send(embed=embed)

@bot.command()
async def howgay(ctx, member:discord.Member = None):
    IMG_CHOICES = ['https://raw.githubusercontent.com/callimarieYT/CalliWebsite/main/unnamed_1.png', 'https://cdn.discordapp.com/attachments/917008192892977232/923233802074095616/pony.gif', 'https://cdn.discordapp.com/attachments/917008192892977232/923233331750006804/F35A8FAE-91D4-4C56-A77F-C8770349D386.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585698743848960/1639974673621.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585702858489876/IMG_7525.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585713612685312/IMG_7515.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585721581858876/IMG_7512.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585864708272138/IMG_7508.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585885075804190/FFTEwb5XoAEUYzm.jpg', 'https://media.discordapp.net/attachments/839929143512137758/918655740716134400/A2C66C28-91A6-4802-978A-FB4B2ECF2414.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585946207793262/565758E6-3785-47F0-8DC7-CB4A6C9E11D1.gif', 'https://media.discordapp.net/attachments/907282095221665835/918919536886030406/caption.gif']
    if member == None:
        member = ctx.author

    embed=discord.Embed(title="how gay are you!!!", description=f"**{member.mention} is {random.randint(0,100)}% homosexual🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈**")
    embed.set_image(url=random.choice(IMG_CHOICES))
    await ctx.send(embed=embed) 

@bot.command(aliases=['howsussy', 'howsussybaka'])
async def howsus(ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    IMG_CHOICES = ['https://raw.githubusercontent.com/callimarieYT/CalliWebsite/main/unnamed_1.png', 'https://cdn.discordapp.com/attachments/917008192892977232/923233802074095616/pony.gif', 'https://cdn.discordapp.com/attachments/917008192892977232/923233331750006804/F35A8FAE-91D4-4C56-A77F-C8770349D386.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585698743848960/1639974673621.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585702858489876/IMG_7525.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585713612685312/IMG_7515.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585721581858876/IMG_7512.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585864708272138/IMG_7508.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585885075804190/FFTEwb5XoAEUYzm.jpg', 'https://media.discordapp.net/attachments/839929143512137758/918655740716134400/A2C66C28-91A6-4802-978A-FB4B2ECF2414.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585946207793262/565758E6-3785-47F0-8DC7-CB4A6C9E11D1.gif', 'https://media.discordapp.net/attachments/907282095221665835/918919536886030406/caption.gif']
    CHOICES = ['``yeah`` <a:noooo:910736617529036830>', '``no ``<:gary:913247181106995271>', '``maybe ``<:maybe:923015512630382623>']

    embed=discord.Embed(title=f"**Is The User {member} Sussy???**", description=f"\u200b")
    embed.add_field(name=f"**The Answer Is:** \u200b", value=f"**\u200b {random.choice(CHOICES)}** ")
    embed.set_image(url=f"{random.choice(IMG_CHOICES)}")
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
    embed=discord.Embed(title="💡List Of Commands", description="**:tools: __Moderation__**")
    embed.add_field(name="``Ban``, ``Unban``, ``Purge``, ``Mute``, ``Unmute``", value="**:video_game: __Fun__**", inline=False)
    embed.add_field(name="``Nickname``, ``howgay``, ``howsus``", value="**📦 __Misc__**")
    embed.add_field(name="``userinfo``, ``server``, ``ping``, ``help``, ``invite``", value="__*More Coming Soon!*__", inline=False)
    await ctx.send(embed=embed) 

@bot.command(aliases=['nickname', 'changenick', 'changenickname'])
async def nick(ctx, member:discord.Member=None):
    CHOICES = ['nutbuster', 'buttnuter', 'Wooden Board', 'bozo', 'Arlo', 'Hubby', 'Wifey', 'Snake hoarder', 'Vietnam War Veteran 26', 'Poppins', 'Whatislife42', 'Hitchhiker ', 'Dumbass', 'Small plant', 'Medium plant', 'HUGE PLANT', 'Left shoe']
    nick=random.choice(CHOICES) 
    if member == None:
        member = ctx.author
    
    embed = discord.Embed(title=f"Changed Nickname for {member} to", description=f"``{nick}``")
   
    if ctx.author == member:
        
        await member.edit(nick=nick)
        await ctx.send(embed=embed)
    else:
        if ctx.author != commands.has_permissions(manage_nicknames=True):
            await ctx.send("``You cant change other's nicknames!``")
        else:
            if ctx.author != commands.has_permissions(manage_nicknames=False):
                await member.edit(nick=nick)
                await ctx.send(embed=embed)   
    

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="You Can Add Oxygen With This Link", description='**https://discord.com/api/oauth2/authorize?client_id=912967056557756426&permissions=137841961990&scope=bot**')
    await ctx.send(embed=embed)

@bot.command()
async def prefixes(ctx):
    embed = discord.Embed(title="My Global Prefixes Are", description=f"``'>', '.', '-', ',', '!'``")
    await ctx.send(embed=embed)



bot.run(token)
