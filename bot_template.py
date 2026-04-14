import discord
from discord.ext import commands
import sys

# السيرفر بيمرر التوكن لهذا الملف كـ "Argument"
TOKEN = sys.argv[1] 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_content="!", intents=intents)

@bot.event
async def on_ready():
    print(f'تم تشغيل البوت بنجاح: {bot.user.name}')

# هنا تقدر تضيف أوامر عامة لكل البوتات اللي بتستضيفها
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! البوت شغال 24 ساعة على سيرفرك")

try:
    bot.run(TOKEN)
except Exception as e:
    print(f"خطأ في التوكن: {e}")
