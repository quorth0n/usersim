import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from simulator import User

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


bot = commands.Bot(command_prefix="$")


@bot.command()
async def sim(ctx, user: discord.User):
    messages = user.history(limit=1000)
    await ctx.send("Got messages!")
    sim_msg = User().get_markov(messages)
    await ctx.send(sim_msg)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))


bot.run(DISCORD_TOKEN)
