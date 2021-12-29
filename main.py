from enum import IntEnum
from typing import Optional
import discord
from discord import activity
from discord import guild
from discord.embeds import Embed
from discord.enums import ActivityType, DefaultAvatar
from discord.ext.commands.core import has_permissions
from discord.ext.commands.flags import F
from discord.guild import Guild
from discord.mentions import A
from discord.ui import Button, View
from discord.ext import commands
import random
import json



import praw

from discord.utils import valid_icon_size
from praw.reddit import Submission

import randfacts

token = ""



prefixes = ['>', '.', '-', ',', '!']


bot = commands.Bot(command_prefix=prefixes , intents=discord.Intents.all())
bot.remove_command('help')



reddit = praw.Reddit(client_id='', #go to reddit developers website to get one
                     client_secret='', #go to reddit developers website to get one
                     user_agent='Oxygen',
                     check_for_async= False)


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle , activity=discord.Activity(type=discord.ActivityType.watching, name=f"{str(len(bot.guilds))} Servers!"))
    print("Logged in as \n{0.user}".format(bot))
    print("-------------------------------------------------")

@bot.event
async def on_member_join(member):
    guild = member.guild
    await member.send(f'Welcome to **{guild}**')


@bot.command()
@commands.has_permissions(administrator=True)
async def sotd(ctx, channel: discord.TextChannel):
    em = discord.Embed(title="Song Of The Day <a:pepedance:920462135774027816>", description="**[Chamomile - Khalil?](https://open.spotify.com/track/6KS2GSlCnTxWiVj3kpnZt5?si=d13697fe60714f49)**")
    em.add_field(name="Feedback:", value="**Isn't that an animal?**", inline=True)
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
        await member.edit(roles=[mutedRole])
        await member.add_roles(mutedRole, reason=reason)
        await member.send(f'You have been muted from {guild.name}! \n Reason: {reason}')




@bot.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
   member_roles = member.roles
   guild = ctx.guild
   mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
   if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")
   else:
       
       await member.remove_roles(mutedRole)
       giveroles = discord.utils.get(ctx.guild.roles, member_roles)
       await  member.add_roles(giveroles)
       embed = discord.Embed(title="✅ Unmuted!", description=f"Unmuted {member.mention}",colour=discord.Colour.light_gray())
       await ctx.send(embed=embed)
       await member.send(f"you have unmuted from: {ctx.guild.name}")



@bot.command()
async def ping(ctx):
    embed = discord.Embed(title="Pong :ping_pong:", description = f"My latency is: {round(bot.latency * 1000)}ms", color=0x5d63c0)
    embed.set_footer(text= f'Requested By {ctx.author}', icon_url=ctx.author.avatar)
    await ctx.send(embed = embed)
    

@bot.command(aliases=['whois'])
async def userinfo(ctx,member: discord.Member = None):
   guild = ctx.guild
   if member == None:
        member = ctx.author  

   roles = " ".join([role.mention for role in member.roles if role.name != "@everyone"])

   if bot.user == ctx.guild.me.top_role:
        await ctx.send(f"**Sorry But Due To Insufficient permissions, i cannot check ``{member}`` user info!**")
   else:
       if not member.avatar:
            embed = discord.Embed(title=f"Info About ``{member}``", description=f"-----------------------------------------------------------")
            embed.add_field(name=f"{member} was created at:", value=f"``{member.created_at.date()}``".replace("-", "/"), inline=False)
            embed.add_field(name=f"{member}'s User ID:", value=f"``{member.id}``", inline=False)
            embed.add_field(name=f"{member} Join Server Date:", value=f"``{member.joined_at.date()}``".replace("-", "/"), inline=False)
            embed.add_field(name=f"{member}'s Roles:", value=f"{roles}",inline=False)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url = ctx.author.avatar)
            await ctx.send(embed=embed)
       else:
            embed = discord.Embed(title=f"Info About ``{member}``", description=f"-----------------------------------------------------------")
            embed.set_thumbnail(url=member.avatar)
            embed.add_field(name=f"{member} was created at:", value=f"``{member.created_at.date()}``".replace("-", "/"), inline=False)
            embed.add_field(name=f"{member}'s User ID:", value=f"``{member.id}``", inline=False)
            embed.add_field(name=f"{member} Join Server Date:", value=f"``{member.joined_at.date()}``".replace("-", "/"), inline=False)
            embed.add_field(name=f"{member}'s Roles:", value=f"{roles}",inline=False)
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
async def ban(ctx, member:discord.Member=None, *, reason=None):    
    if member == None:
        await ctx.send("``Who Are You Banning?``")
    else:
        if member == bot.user:
            await ctx.send("``You Cannot Ban Me!``")
        else:
            if member == ctx.author:
                await ctx.send('``You Cannot Ban Yourself!``')
            else:    
                if reason == None:
                    reason="No Reason Specified" 

                embed = discord.Embed(title=f"succesfully banned {member.name} from this server", description=f"Reason: {reason}\nBy: {ctx.author.mention}")    

                await member.ban(reason=reason)
                await member.send(f'``You Have Been Banned From {ctx.guild.name} for`` \n``{reason}``')
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
    embed.add_field(name="``Ban``, ``Unban``, ``Purge``, ``Mute``, ``Unmute``, ``kick``", value="**:video_game: __Fun__**", inline=False)
    embed.add_field(name="``nick``, ``howgay``, ``howsus``, ``facts``, ``memes``, ``osugame``, ``8ball``, ``banf``, ``spacify``", value="**📦 __Misc__**")
    embed.add_field(name="``userinfo``, ``server``, ``ping``, ``help``, ``invite``, ``serverinfo``, ``banner``", value="__*More Coming Soon!*__", inline=False)
   
    await ctx.send(embed=embed) 

@bot.command(aliases=['nickname', 'changenick', 'changenickname'])
async def nick(ctx, member:discord.Member=None):
   
    nick_file = open("nick.json", "r") # opens the nick file in "read" mode
    nicks = json.loads(nick_file.read()) # loads the json
    nick_file.close() # closes the nick file
    
    nick_choice = random.choice(nicks['nicks'])

    if member == None:
        member = ctx.author
    
    embed = discord.Embed(title=f"Changed Nickname for {member} to", description=f"``{nick_choice}``")
    
   
    if member == bot.user:
        await ctx.send('You cannot change my nickname!')
    else:
        if ctx.author == member:
        
            await member.edit(nick=nick_choice)
            await ctx.send(embed=embed)
        else:
            if  ctx.author.guild_permissions.manage_nicknames == False:
                await ctx.send("``You cant change other's nicknames!``")
            else:
                await member.edit(nick=nick_choice)
                await ctx.send(embed=embed)



@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="You Can Add Oxygen With This Link", description=f'[**oauth link**](https://discord.com/api/oauth2/authorize?client_id=912967056557756426&permissions=137841961990&scope=bot)')
    await ctx.send(embed=embed)

@bot.command()
async def prefixes(ctx):
    embed = discord.Embed(title="My Global Prefixes Are", description=f"``'>', '.', '-', ',', '!'``")
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"Server Info For {guild}", description="----------------------------------", timestamp=ctx.message.created_at)
    embed.set_thumbnail(url=guild.icon)
    embed.add_field(name="Number Of Channels", value=len(ctx.guild.channels), inline=False)
    embed.add_field(name="Number Of Roles", value=len(ctx.guild.roles), inline=False)
    embed.add_field(name="Number of Boosters:", value=guild.premium_subscription_count, inline=False)
    embed.add_field(name="Member Count", value=guild.member_count, inline=False)
    embed.add_field(name="Date Of Creation", value=guild.created_at.date(), inline=False)
    embed.add_field(name="Owner Of Server", value=guild.owner, inline=False)
    embed.add_field(name="Server ID", value=guild.id)
    embed.set_footer(text=f"Requested By {ctx.author}")
    await ctx.send(embed=embed)


@bot.command(aliases=['fact', 'randomfact'])
async def facts(ctx):
    facts = randfacts.get_fact()

    embed = discord.Embed(title="Random Fact Generator!", description=f"``{facts}``")
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar)
    await ctx.send(embed=embed)


@bot.command(aliases=['meme'])
async def memes(ctx):
    meme_submissions = reddit.subreddit('meme').hot()
    post_to_pick = random.randint(1,50)
    for i in range(0, post_to_pick):
        Submission = next(x for x in meme_submissions if not x.stickied)

    embed = discord.Embed(title="Random Memes:", description=f"**[{Submission.title}]({Submission.url})**")
    embed.set_image(url=Submission.url)    
    await ctx.send(embed=embed)


@bot.command()
async def spacify(ctx, message=None):
    
    

    if message == None:
        await ctx.send("You Didn't Give Me A Message!")
    else:
       message = message.replace('',' ')
       message = message.replace('`', '\`')
       message = message.replace("*", '\*')
       message = message.replace("\\","\\\\")

       await ctx.send(message)
    
@bot.command()
@commands.has_permissions(ban_members=True)
async def testing(ctx):
    await ctx.send("Just Testing Some Things! \n Don't mind me!")

@bot.command()
async def christmas(ctx):
    await ctx.send(f"Merry Christmas {ctx.author.mention} \nSorry There Wasn't more to this.\ni was gonna make this command a christmas reddit one but there aren't any christmas subreddits lol")


@bot.command()
async def osugame(ctx):
    osu_submission = reddit.subreddit('osugame').hot()
    post_to_pick = random.randint(1,30)
    for i in range(0, post_to_pick):
        submission = next(x for x in osu_submission if not x.stickied)

    embed = discord.Embed(title="top osu posts:", description=f"**[{submission.title}](https://reddit.com{submission.permalink})**")
    embed.set_image(url=submission.url)    
    await ctx.send(embed=embed)

@bot.command(aliases=["8ball"])
async def _8ball(ctx, question=None,question2=None, question3=None, question4=None):
    if question == None:
        await ctx.send("You Need To Give Me A Question!")
    else:
        if question4 != None:
            _8ball_file = open("responses.json", "r")
            responses = json.loads(_8ball_file.read())
            _8ball_file.close()
            _8ball_choice = random.choice(responses['responses'])
        
            message = f"🎱**Question:** {question} {question2} {question3} {question4} \n**Answer:** {_8ball_choice}"
            await ctx.send(message)    
        else:
            if question2 and question3== None:
                _8ball_file = open("responses.json", "r")
                responses = json.loads(_8ball_file.read())
                _8ball_file.close()
                _8ball_choice = random.choice(responses['responses'])
        
                message = f"🎱**Question:** {question}\n**Answer:** {_8ball_choice}"
                await ctx.send(message)
            else:
                _8ball_file = open("responses.json", "r")
                responses = json.loads(_8ball_file.read())
                _8ball_file.close()
                _8ball_choice = random.choice(responses['responses'])
        
                message = f"🎱**Question:** {question} {question2} {question3} \n**Answer:** {_8ball_choice}"
                await ctx.send(message)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    if member == None:
        await ctx.send("Who are you kicking?")
    else:
        if member == ctx.author:
            await ctx.send('``You Cannot kick Yourself!``')
        if reason == None:
            reason="No Reason Specified"

        embed = discord.Embed(title=f"Successfully kicked {member}", description=f"Reason: {reason}")   
        await member.kick(reason=reason)
        await member.send(f'``You Have Been Kicked From {ctx.guild.name} for`` \n ``{reason}``')
        await ctx.send(embed=embed)


@bot.command()
async def banf(ctx, member:discord.Member=None, *, reason=None):
    
    if member == bot.user:
        await ctx.send("BaNf Me AnD i WiLl ChOp OfF yOuR bAlLs!!!")
    else:
        if member == None:
            await ctx.send("WHo ArE yOu BaNfInG?")
        else: 
            if member == ctx.author:
                await ctx.send('``YoU cAnNoT bAnF yOuRsElF!!!``')
            else:
                if reason == None:
                    reason="LmAo GeT bAnFeD!!!"
                embed = discord.Embed(title=f"BaNfEd {member}", description=f"ReAsOn: {reason}")   
                await ctx.send(embed=embed)  


@bot.command()
async def banner(ctx, member:discord.Member=None):
    if member == None:
        member = ctx.author

    user = await bot.fetch_user(member.id)
    banner_url = user.banner.url

    embed = discord.Embed(title=f"Here's ``{member}``'s Banner")
    embed.set_image(url=f"{banner_url}")
    embed.set_footer(text= f'Requested By {ctx.author}', icon_url=ctx.author.avatar)
    
    await ctx.send(embed=embed)




bot.run(token)  
