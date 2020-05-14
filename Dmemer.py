import discord
import psycopg2
import os
from itertools import cycle
from discord.ext import commands, tasks
 
bot = commands.Bot(command_prefix='n!')
#Status Change
status = cycle(['Looking at the records', 'transferring money', 'Waiting for drama'])
@tasks.loop(seconds=2)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(status)))
@bot.event
async def on_ready():
    change_status.start()
    print('Ready.')

@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)} ms")

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
@bot.command()
async def init(ctx):
	  cur.execute("DROP TABLE IF EXISTS data")
	  cur.execute("CREATE TABLE data (id TEXT, amount INTEGER)")
	  for guild in bot.guilds:
	      for member in guild.members:
	      	cur.execute(f"INSERT INTO data VALUES ({member.id}), (15000) ")
	      	await ctx.send(f"Member {member.name}{member.discriminator} has been added to the database")
	  conn.commit()
	  
@bot.command()
async def rich(ctx):
	for guild in bot.guilds:
	  for member in guild.members:
	      cur.execute(f"SELECT * FROM data WHERE id = {member.id}")
	      record = cur.fetchall()
	      for row in record:
	      	print("ID: ", row[0])
	      	print("Amount: " row[1])

token = os.environ.get('BOT_TOKEN')
bot.run(token)
