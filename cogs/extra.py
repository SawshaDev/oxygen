import discord

from discord.ext import commands

import json


async def open_muted(user):

  users = await get_muted_data()

  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["mute"] = 0

    


  with open("blacklist.json","w") as f:
    json.dump(users,f)
  return True

async def get_mute(user):
    
    await open_muted(user)
    users = await get_muted_data()

    wallet_amt = users[str(user.id)]['mute']
    return wallet_amt

async def get_muted_data():
  with open("blacklist.json") as f:
    users = json.load(f)

    return users


async def add_mute(user):
    
    await open_muted(user)
    
    users = await get_muted_data()

    users[str(user.id)]['mute'] += 1

    with open("blacklist.json","w") as f:
        json.dump(users, f)

async def remove_mute(user):
    
    await open_muted(user)
    
    users = await get_muted_data()

    users[str(user.id)]['mute'] -= 1

    with open("blacklist.json","w") as f:
        json.dump(users, f)

class Extra(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sotd(self,ctx, channel: discord.TextChannel):
        if await get_mute(ctx.author) != 0:
            await ctx.send("You are not allowed to use this command")
        else:
            em = discord.Embed(title="Song Of The Day <a:pepedance:920462135774027816>", description="**[Chamomile - Khalil?](https://open.spotify.com/track/6KS2GSlCnTxWiVj3kpnZt5?si=d13697fe60714f49)**")
            em.add_field(name="Feedback:", value="**Isn't that an animal?**", inline=True)
            await channel.send(embed=em)
    
    @sotd.error
    async def sotd_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"<a:siren:922358771735461939> You can't use this command! Command requires ``Adminstrator`` Permissions!! <a:siren:922358771735461939>")
            print(f"Command ``sotd`` was attempted \n User Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------")    




    @commands.command()
    @commands.has_permissions(administrator=True)
    async def blacklist(self,ctx,list=None,user:discord.Member=None, *,reason=None):
        sawsha = self.bot.get_user(894794517079793704)
        if user == sawsha:
            await ctx.send("You Cannot Blacklist The Owner Of Oxygen!")
            print(f"{ctx.author} attempted to blacklist {sawsha}!\nID == {ctx.author.id}")
        else:
            if user == self.bot.user:
                await ctx.send("Why are you trying to blacklist me?")
            else:
                if user == None:
                    await ctx.send("Please Specify Who You Are Blacklisting!")
    
                if user == ctx.author:
                    await ctx.send("You cannot blacklist yourself!")
                else:
                    if await get_mute(user) == 0:
                        await add_mute(user)
                        await ctx.send("{} has blacklisted {} for : {}".format(ctx.author.name, user.name, reason))
                    else:
                        await ctx.send("The person is already blacklisted.")
          
        
        

    @blacklist.error
    async def blacklist_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Do Not Have Sufficent Role/Permission To Run This Command!")
            print(f"Command blacklist was attempted \nUser Who Used It == {ctx.author}! \n ID == {ctx.author.id} \n -------------------------------------------------------")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unblacklist(self,ctx,user:discord.Member, *,reason=None):
        if await get_mute(user) != 0:
            await remove_mute(user)
            await ctx.send("{} has unblacklisted {}".format(ctx.author.name, user.name))
        else:
            await ctx.send("The person is already unblacklisted.")    




def setup(bot):
    bot.add_cog(Extra(bot))
                    