import discord

import time

import os
from discord.ext.commands.core import command
import psutil
import aiohttp

from discord.ext import commands

from utils import http, cache, default



import random

class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command()
    async def ping(self,ctx):
        ramUsage = self.process.memory_full_info().rss / 1024**2
        embed = discord.Embed(title="Pong :ping_pong:", description = f"My latency is: ``{round(self.bot.latency * 1000)}ms``\nRam Usage: ``{ramUsage:.2f} MB``", color=0x5d63c0)
        embed.set_footer(text= f'Requested By {ctx.author}', icon_url=ctx.author.avatar)
        await ctx.send(embed = embed)   

    @commands.command()
    async def covid(self, ctx, *, country: str):
        """Covid-19 Statistics for any countries"""
        async with ctx.channel.typing():
            r = await http.get(f"https://disease.sh/v3/covid-19/countries/{country.lower()}", res_method="json")

            if "message" in r:
                return await ctx.send(f"The API returned an error:\n{r['message']}")

            json_data = [
                ("Total Cases", r["cases"]), ("Total Deaths", r["deaths"]),
                ("Total Recover", r["recovered"]), ("Total Active Cases", r["active"]),
                ("Total Critical Condition", r["critical"]), ("New Cases Today", r["todayCases"]),
                ("New Deaths Today", r["todayDeaths"]), ("New Recovery Today", r["todayRecovered"])
            ]

            embed = discord.Embed(
                description=f"The information provided was last updated <t:{int(r['updated'] / 1000)}:R>"
            )

            for name, value in json_data:
                embed.add_field(
                    name=name, value=f"{value:,}" if isinstance(value, int) else value
                )

            await ctx.send(
                f"**COVID-19** statistics in :flag_{r['countryInfo']['iso2'].lower()}: "
                f"**{country.capitalize()}** *({r['countryInfo']['iso3']})*",
                embed=embed
            )
    



    @commands.command(aliases=['servers', 'Servers', 'botservers'])
    async def server(self,ctx):
        embed=discord.Embed(title="Server Count", description=f"**I am in {str(len(self.bot.guilds))} servers <:chad:923554621597818901>**")
        await ctx.send(embed=embed)

    @commands.command(aliases=['whois'])
    @commands.guild_only()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """ Get user information """
        user = user or ctx.author

        show_roles = ", ".join(
            [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
        ) if len(user.roles) > 1 else "None"

        embed = discord.Embed(title=f"ℹ About **{user.id}**")
        embed.set_thumbnail(url=user.avatar)

        embed.add_field(name="Username", value=f"{user}", inline=False)
        embed.add_field(name="Nickname", value=user.nick if hasattr(user, "nick") else "None", inline=False)
        embed.add_field(name="Account created", value=default.date(user.created_at, ago=True), inline=False)
        embed.add_field(name="Joined this server", value=default.date(user.joined_at, ago=True), inline=False)
        embed.add_field(name="Roles", value=show_roles, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def invite(self,ctx):
        embed = discord.Embed(title="You Can Add Oxygen With This Link", description=f'[**oauth link**](https://discord.com/api/oauth2/authorize?client_id=912967056557756426&permissions=137841961990&scope=bot)')
        await ctx.send(embed=embed)

    @commands.command()
    async def prefixes(self,ctx):
        embed = discord.Embed(title="My Global Prefixes Are", description=f"``'>', '.', '-', ',', '!'``")
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self,ctx):
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


    @commands.command()
    async def help(self,ctx):
        embed=discord.Embed(title="💡List Of Commands", description="**:tools: __Moderation__**")
        embed.add_field(name="``Ban``, ``Unban``, ``Purge``, ``Mute``, ``Unmute``, ``kick``", value="**:video_game: __Fun__**", inline=False)
        embed.add_field(name="``nick``, ``howgay``, ``howsus``, ``facts``, ``memes``, ``osugame``, ``8ball``, ``banf``, ``snipe``, ``mood``. ``kys``", value="**🎵__Music__**",inline=False)
        embed.add_field(name="``join``, ``playfile``,``play``, ``yt``, ``stop``", value="**📦 __Misc__**")
        embed.add_field(name="``userinfo``, ``server``, ``ping``, ``help``, ``invite``, ``serverinfo``, ``banner``, ``av`` ,``source``, ``membercount``", value="__*More Coming Soon!*__", inline=False)
   
        await ctx.send(embed=embed) 


    @commands.command()
    async def banner(self,ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author

        user = await self.bot.fetch_user(member.id)
        banner_url = user.banner.url

        embed = discord.Embed(title=f"Here's ``{member}``'s Banner")
        embed.set_image(url=f"{banner_url}")
        embed.set_footer(text= f'Requested By {ctx.author}', icon_url=ctx.author.avatar)
    
        await ctx.send(embed=embed)

    @commands.command()
    async def source(self,ctx):  
        embed = discord.Embed(title="Source For Oxygen", description="https://github.com/callimarieYT/oxygen")
        await ctx.send(embed=embed)

    @commands.command(aliases=['avatar'])
    async def av(self,ctx, member:discord.Member=None):
        if member == None:
            member = ctx.author

        if member == self.bot:
            embed = discord.Embed(description=f"**[Avatar Link]({ctx.bot.user.avatar.url})**")      
            embed.set_author(name=f"{member}", icon_url=ctx.bot.user.avatar)
            embed.set_image(url=member.avatar.url)
            embed.set_footer(text="Yes i know this is exactly like dyno's avatar command.")
        else:
            embed = discord.Embed(description=f"**[Avatar Link]({member.avatar.url})**")      
            embed.set_author(name=f"{member}", icon_url=member.avatar.url)
            embed.set_image(url=member.avatar.url)
            embed.set_footer(text="Yes i know this is exactly like dyno's avatar command.")
        
            await ctx.send(embed=embed)

    @commands.command(aliases=['members'])
    async def membercount(self,ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Members", description=f"**{guild.member_count} Members**", timestamp=ctx.message.created_at)
        embed.set_footer(text="")
        await ctx.send(embed=embed)

    @commands.command()
    async def support(self,ctx):
        embed=discord.Embed(title=f"Official Support Server", description="https://discord.gg/YA4tJYdZfE")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))        

            