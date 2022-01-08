import discord

from discord.ext import commands

import random
from discord.ext.commands.core import command

import praw

import randfacts
import json


import asyncio

reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='',
                     check_for_async= False)



class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def howgay(self,ctx, member:discord.Member = None):    
        IMG_CHOICES = ['https://raw.githubusercontent.com/callimarieYT/CalliWebsite/main/unnamed_1.png', 'https://cdn.discordapp.com/attachments/917008192892977232/923233802074095616/pony.gif', 'https://cdn.discordapp.com/attachments/917008192892977232/923233331750006804/F35A8FAE-91D4-4C56-A77F-C8770349D386.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585698743848960/1639974673621.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585702858489876/IMG_7525.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585713612685312/IMG_7515.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585864708272138/IMG_7508.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585885075804190/FFTEwb5XoAEUYzm.jpg','https://cdn.discordapp.com/attachments/904887116381700147/923585946207793262/565758E6-3785-47F0-8DC7-CB4A6C9E11D1.gif', 'https://media.discordapp.net/attachments/907282095221665835/918919536886030406/caption.gif']
        if member == None:
            member = ctx.author

        embed=discord.Embed(title="how gay are you!!!", description=f"**{member.mention} is {random.randint(0,100)}% homosexual🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈🏳️‍🌈**")
        embed.set_image(url=random.choice(IMG_CHOICES))
        await ctx.send(embed=embed)    

    @commands.command(aliases=['howsussy', 'howsussybaka'])
    async def howsus(self,ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        IMG_CHOICES = ['https://raw.githubusercontent.com/callimarieYT/CalliWebsite/main/unnamed_1.png', 'https://cdn.discordapp.com/attachments/917008192892977232/923233802074095616/pony.gif', 'https://cdn.discordapp.com/attachments/917008192892977232/923233331750006804/F35A8FAE-91D4-4C56-A77F-C8770349D386.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585698743848960/1639974673621.jpg', 'https://cdn.discordapp.com/attachments/904887116381700147/923585702858489876/IMG_7525.png', 'https://cdn.discordapp.com/attachments/904887116381700147/923585713612685312/IMG_7515.jpg','https://cdn.discordapp.com/attachments/904887116381700147/923585864708272138/IMG_7508.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585885075804190/FFTEwb5XoAEUYzm.jpg', 'https://media.discordapp.net/attachments/839929143512137758/918655740716134400/A2C66C28-91A6-4802-978A-FB4B2ECF2414.gif', 'https://cdn.discordapp.com/attachments/904887116381700147/923585946207793262/565758E6-3785-47F0-8DC7-CB4A6C9E11D1.gif', 'https://media.discordapp.net/attachments/907282095221665835/918919536886030406/caption.gif']
        CHOICES = ['``yeah`` <a:noooo:910736617529036830>', '``no ``<:gary:913247181106995271>', '``maybe ``<:maybe:923015512630382623>']

        embed=discord.Embed(title=f"**Is The User {member} Sussy???**", description=f"\u200b")
        embed.add_field(name=f"**The Answer Is:** \u200b", value=f"**\u200b {random.choice(CHOICES)}** ")
        embed.set_image(url=f"{random.choice(IMG_CHOICES)}")
        embed.set_footer(text=f"Requested By {member}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['nickname', 'changenick', 'changenickname'])
    async def nick(self,ctx, member:discord.Member=None):
        nick_file = open("nick.json", "r") # opens the nick file in "read" mode
        nicks = json.loads(nick_file.read()) # loads the json
        nick_file.close() # closes the nick file
    
        nick_choice = random.choice(nicks['nicks'])

        if member == None:
            member = ctx.author
    
        embed = discord.Embed(title=f"Changed Nickname for {member} to", description=f"``{nick_choice}``")
    
   
        if member == self.bot.user:
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


    @commands.command(aliases=['fact', 'randomfact'])
    async def facts(self,ctx):
        facts = randfacts.get_fact()

        embed = discord.Embed(title="Random Fact Generator!", description=f"``{facts}``")
        embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['meme'])
    async def memes(self,ctx):
        meme_submissions = reddit.subreddit('meme').hot()
        post_to_pick = random.randint(1,50)
        for i in range(0, post_to_pick):
            Submission = next(x for x in meme_submissions if not x.stickied)

        embed = discord.Embed(title="Random Memes:", description=f"**[{Submission.title}]({Submission.url})**")
        embed.set_image(url=Submission.url)    
        await ctx.send(embed=embed)

    @commands.command()
    async def osugame(self,ctx):
        osu_submission = reddit.subreddit('osugame').hot()
        post_to_pick = random.randint(1,30)
        for i in range(0, post_to_pick):
            submission = next(x for x in osu_submission if not x.stickied)

        embed = discord.Embed(title="top osu posts:", description=f"**[{submission.title}](https://reddit.com{submission.permalink})**")
        embed.set_image(url=submission.url)    
        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball"])
    async def _8ball(self,ctx, question,question2=None, question3=None, question4=None):
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
                if question3 != None:
                    _8ball_file = open("responses.json", "r")
                    responses = json.loads(_8ball_file.read())
                    _8ball_file.close()
                    _8ball_choice = random.choice(responses['responses'])
        
                    message = f"🎱**Question:** {question} {question2} {question3}\n**Answer:** {_8ball_choice}"
                    await ctx.send(message)
                else:
                    if question2 != None:
                        _8ball_file = open("responses.json", "r")
                        responses = json.loads(_8ball_file.read())
                        _8ball_file.close()
                        _8ball_choice = random.choice(responses['responses'])
        
                        message = f"🎱**Question:** {question} {question2} \n**Answer:** {_8ball_choice}"
                        await ctx.send(message)
                    else:
                        if question != None:
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
        
                            message = f"🎱**Question:** {question} {question2}\n**Answer:** {_8ball_choice}"
                            await ctx.send(message)
        

    @commands.command()
    async def banf(self,ctx, member:discord.Member=None, *, reason=None):
        if member == self.bot.user:
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


    snipe_message_content = None
    snipe_message_author = None
    snipe_message_id = None

    @commands.Cog.listener()
    async def on_message_delete(message):

        global snipe_message_content
        global snipe_message_author
        global snipe_message_id
        global snipe_message_avatar

        snipe_message_content = message.content
        snipe_message_author = message.author
        snipe_message_avatar = message.author.avatar
        snipe_message_id = message.id
        await asyncio.sleep(60)

        if message.id == snipe_message_id:
            snipe_message_author = None
            snipe_message_content = None
            snipe_message_id = None
            snipe_message_avatar = None

    @commands.command()
    async def snipe(self,message):
        if snipe_message_content == None:
            await message.channel.send("There Isn't Anything I Can Snipe!")
        else:
            embed = discord.Embed(title=f"Snipped {snipe_message_author}'s Message!", description=f"Message Snipped:   ``{snipe_message_content}``")
            embed.set_footer(text=f"Requested By {message.author.name}#{message.author.discriminator}", icon_url=snipe_message_avatar.url)
            await message.channel.send(embed=embed)
            return                 

    @commands.command()
    async def kys(self,ctx):
        await ctx.send("https://tenor.com/view/air-fryer-clearly-you-dont-own-an-air-fryer-you-probably-dont-own-an-air-fryer-you-should-kill-now-meme-dalauan-sparrow-gif-24167808")

    @commands.command()
    async def mood(self,ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author

        random_num = random.randint(0,100)

        if random_num == 100:
            message = f"LMAO your current mood is at {random_num}%, {ctx.author.mention}\nhttps://tenor.com/view/arangutan-monkey-dancing-gif-15130385"
            await ctx.send(message)

        if (random_num < 60) & (random_num > 50):
            message = f"LMAO your current mood is at {random_num}%, {ctx.author.mention}\n https://media.discordapp.net/attachments/686218895140716666/917100323473084456/computer__meltingA.gif"
            await ctx.send(message)


        
        message = f"LMAO your current mood is at {random_num}%, {ctx.author.mention}"
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Fun(bot))     
