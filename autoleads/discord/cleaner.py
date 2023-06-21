import discord
from discord.ext import commands

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

bot.run('your-token-here')
