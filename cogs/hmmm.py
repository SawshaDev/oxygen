import discord

from discord.ext  import commands
from discord.embeds import Embed

import praw
import random

from praw.reddit import Submission


reddit = praw.Reddit(client_id='pua14mlzkyv5_ZfQ2WmqpQ',
                     client_secret='T5loHbaVD7m-RNMpFf0z24iOJsInwg',
                     user_agent='Oxygen',
                     check_for_async= False)


class hmmmm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """You will not ask. you will not ask/"""

    @commands.command()
    @commands.is_nsfw()
    async def nsfw(self,ctx):
        nsfw_submission = reddit.subreddit('nsfw').hot()
        post_to_pick = random.randint(1,30)
        for i in range(0, post_to_pick):
            submission = next(x for x in nsfw_submission if not x.stickied)

        embed = discord.Embed(title="Dirty Fucker", description=f"**[{submission.title}](https://reddit.com{submission.permalink})**",timestamp=ctx.message.created_at)
        embed.set_image(url=submission.url)    
        embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @nsfw.error
    async def nsfw_error(ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            await ctx.send("I Cannot Run This Command Without The Channel Being NSFW!")


    @commands.command()
    @commands.is_nsfw()
    async def rule34(self, ctx):
        rule34_submission = reddit.subreddit('rule34').hot()
        post_to_pick = random.randint(1,30)
        for i in range(0, post_to_pick):
            submission = next(x for x in rule34_submission if not x.stickied)

        embed = discord.Embed(title="Dirty Fucker", description=f"**[{submission.title}](https://reddit.com{submission.permalink})**",timestamp=ctx.message.created_at)
        embed.set_image(url=submission.url)    
        embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(hmmmm(bot))                    