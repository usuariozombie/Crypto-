from asyncio import tasks
from logging import fatal
from os import name
import discord
from pycoingecko import CoinGeckoAPI
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from datetime import datetime
from discord import Client, Intents, Embed
import random
import asyncio
import json

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = discord.Client(intents=discord.Intents.all())
bot = commands.Bot(command_prefix = get_prefix, description="No prefix needed.", case_insensitive=True)
cg = CoinGeckoAPI()
guild_ids = [yourserverid]

fiat_symbol_dict = {
    "usd" : "$",
    "inr" : "₹",
    "eur" : "€",
    "gbp" : "£",
    "jpy" : "¥",
    "cad" : "C$",
    "aud" : "A$",
    "mxn" : "MX$",
    "clp" : "CH$",
    "ars" : "AR$"
}

def getCryptoPrice(cryptoId, fiatId):
    return cg.get_price(ids=cryptoId, vs_currencies=fiatId)


def parsePriceJson(priceJson, fiat):
    str = ""
        
    for coin in priceJson:
        str += "{} price is ".format(coin.capitalize())
        for fiat in priceJson[coin]:
            str += "{} {:,.8f}".format(fiat_symbol_dict[fiat], priceJson[coin][fiat])
        str += ""
    
    return str

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    
    prefixes[str(guild.id)] = "$"

    with open ("prefixes.json", "r") as f:
        json.dump(prefixes, f)

bot.remove_command("help")

@bot.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

    embed=discord.Embed(name="PREFIX", color=discord.Color.random())
    embed.set_author(name=f"Prefix was changed to {prefix}", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    await ctx.send(embed=embed)

@bot.command()
async def ping(message):
    embed=discord.Embed(name="PING", color=discord.Color.random())
    embed.set_author(name=f"Crypto$ ping is {int(bot.latency * 1000)}ms", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    await message.send(embed=embed)

@bot.command()
async def crypto(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="This is the supported crypto list right now.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="Bitcoin", value="``id = bitcoin``", inline=False)
    embed.add_field(name="Ethereum", value="``id = ethereum``", inline=False)
    embed.add_field(name="Litecoin", value="``id = litecoin``", inline=False)
    embed.add_field(name="Dogecoin", value="``id = dogecoin``", inline=False)
    embed.add_field(name="Bitcoin Cash", value="``id = bitcoin-cash``", inline=True)
    embed.add_field(name="Cardano", value="``id = cardano``", inline=False)
    embed.add_field(name="Matic Network", value="``id = matic-network``", inline=False)
    embed.add_field(name="Amaten", value="``id = amaten``", inline=False)
    embed.add_field(name="Tether", value="``id = tether``", inline=False)
    embed.add_field(name="Solana", value="``id = solana``", inline=False)
    embed.add_field(name="Polkadot", value="``id = polkadot``", inline=False)
    embed.add_field(name="Uniswap", value="``id = uniswap``", inline=False)
    embed.add_field(name="Shiba Inu", value="``id = shiba-inu``", inline=False)
    embed.add_field(name="Binance Coin", value="``id = binancecoin``", inline=False)
    embed.add_field(name="Terra", value="``id = terra-luna``", inline=False)
    embed.add_field(name="Chainlink", value="``id = chainlink``", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def fiats(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="This is the supported crypto list right now.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="$US Dollars", value="``id = usd``", inline=False)
    embed.add_field(name="€Euro", value="``id = eur``", inline=False)
    embed.add_field(name="₹Indian Rupees", value="``id = inr``", inline=False)
    embed.add_field(name="£British Pound", value="``id = gbp``", inline=False)
    embed.add_field(name="¥Japanese Yen", value="``id = jpy``", inline=True)
    embed.add_field(name="C$Canadian Dollar", value="``id = cad``", inline=False)
    embed.add_field(name="A$Australian Dollar", value="``id = aud``", inline=False)
    embed.add_field(name="MX$Mexican Peso", value="``id = mxn``", inline=False)
    embed.add_field(name="CH$Chilean Peso", value="``id = clp``", inline=False)
    embed.add_field(name="AR$Argentine Peso", value="``id = ars``", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="Slash command list is:.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="/ping", value="``This command show the latency.``", inline=False)
    embed.add_field(name="/fiats", value="``The supported fiat list.``", inline=False)
    embed.add_field(name="/crypto", value="``The supported cryptocoin list.``", inline=False)
    embed.add_field(name="/price", value="``Real time price of every cryptocurrency.``", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def price(ctx, cryptoid, fiatid):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=(f'{parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}'), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@price.error
async def price_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("```diff\n-Error, remember to write it correctly c$price crypto fiat (example = c$price bitcoin eur)```")

slash = SlashCommand(bot, sync_commands=True)

@slash.slash(name="ping",description="``This command show the latency.``" , guild_ids=guild_ids)
async def ping(message: SlashContext):
    embed=discord.Embed(name="PING", color=discord.Color.random())
    embed.set_author(name=f"Crypto$ ping is {int(bot.latency * 1000)}ms", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    await message.send(embed=embed)


@slash.slash(name="crypto",description="``The supported cryptocoin list.``" , guild_ids=guild_ids)
async def crypto(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="This is the supported crypto list right now.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="Bitcoin", value="``id = bitcoin``", inline=False)
    embed.add_field(name="Ethereum", value="``id = ethereum``", inline=False)
    embed.add_field(name="Litecoin", value="``id = litecoin``", inline=False)
    embed.add_field(name="Dogecoin", value="``id = dogecoin``", inline=False)
    embed.add_field(name="Bitcoin Cash", value="``id = bitcoin-cash``", inline=True)
    embed.add_field(name="Cardano", value="``id = cardano``", inline=False)
    embed.add_field(name="Matic Network", value="``id = matic-network``", inline=False)
    embed.add_field(name="Amaten", value="``id = amaten``", inline=False)
    embed.add_field(name="Tether", value="``id = tether``", inline=False)
    embed.add_field(name="Solana", value="``id = solana``", inline=False)
    embed.add_field(name="Polkadot", value="``id = polkadot``", inline=False)
    embed.add_field(name="Uniswap", value="``id = uniswap``", inline=False)
    embed.add_field(name="Shiba Inu", value="``id = shiba-inu``", inline=False)
    embed.add_field(name="Binance Coin", value="``id = binancecoin``", inline=False)
    embed.add_field(name="Terra", value="``id = terra-luna``", inline=False)
    embed.add_field(name="Chainlink", value="``id = chainlink``", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="fiats",description="``The supported fiat list.``" , guild_ids=guild_ids)
async def fiats(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="This is the supported crypto list right now.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="$US Dollars", value="``id = usd``", inline=False)
    embed.add_field(name="€Euro", value="``id = eur``", inline=False)
    embed.add_field(name="₹Indian Rupees", value="``id = inr``", inline=False)
    embed.add_field(name="£British Pound", value="``id = gbp``", inline=False)
    embed.add_field(name="¥Japanese Yen", value="``id = jpy``", inline=True)
    embed.add_field(name="C$Canadian Dollar", value="``id = cad``", inline=False)
    embed.add_field(name="A$Australian Dollar", value="``id = aud``", inline=False)
    embed.add_field(name="MX$Mexican Peso", value="``id = mxn``", inline=False)
    embed.add_field(name="CH$Chilean Peso", value="``id = clp``", inline=False)
    embed.add_field(name="AR$Argentine Peso", value="``id = ars``", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="help", guild_ids=guild_ids)
async def help(ctx):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name="Slash command list is:.", icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    embed.add_field(name="/ping", value="``This command show the latency.``", inline=False)
    embed.add_field(name="/fiats", value="``The supported fiat list.``", inline=False)
    embed.add_field(name="/crypto", value="``The supported cryptocoin list.``", inline=False)
    embed.add_field(name="/price", value="``Real time price of every cryptocurrency.``", inline=False)
    await ctx.send(embed=embed)

@slash.slash(name="price", description="``Real time price of every cryptocurrency.``", guild_ids=guild_ids)
async def price(ctx, cryptoid, fiatid):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=(f'{parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}'), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)

@bot.command()
async def ualert(ctx, cryptoid, fiatid, amount):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=("Price alert was set correctly."), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.reply(embed=embed)
    while True:
        a = cg.get_price(ids=cryptoid, vs_currencies=fiatid)
        if float(a[f"{cryptoid}"][f"{fiatid}"]) >= float(amount):
            embed=discord.Embed(name="lol",description=f"``{cryptoid}`` has just passed ``{amount}``! Now {parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}",timestamp=datetime.utcnow())
            embed.set_author(name=("Price alert"), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
            embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
            embed.set_image(url="https://media.discordapp.net/attachments/896877291831959592/896877393392840755/ezgif-2-997863236c59.gif")
            await ctx.reply(embed=embed)
            break
        else:
            await asyncio.sleep(10)

@bot.command()
async def dalert(ctx, cryptoid, fiatid, amount):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=("Price alert was set correctly."), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.reply(embed=embed)
    while True:
        a = cg.get_price(ids=cryptoid, vs_currencies=fiatid)
        if float(a[f"{cryptoid}"][f"{fiatid}"]) <= float(amount):
            embed=discord.Embed(name="lol",description=f"``{cryptoid}`` has just fallen below ``{amount}``! Now {parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}",timestamp=datetime.utcnow())
            embed.set_author(name=("Price alert"), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
            embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
            embed.set_image(url="https://media.discordapp.net/attachments/896877291831959592/896877396869914624/ezgif-2-9e8e69a1e9ef.gif")
            await ctx.reply(embed=embed)
            break
        else:
            await asyncio.sleep(10)

@slash.slash(name="ualert", description="``Notifies you if a crypto price passes specified amount.``", guild_ids=guild_ids)
async def _ualert(ctx: SlashContext, cryptoid, fiatid, amount):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=("Price alert was set correctly."), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)
    while True:
        a = cg.get_price(ids=cryptoid, vs_currencies=fiatid)
        if float(a[f"{cryptoid}"][f"{fiatid}"]) >= float(amount):
            embed=discord.Embed(name="lol",description=f"``{cryptoid}`` has just passed ``{amount}``! Now {parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}",timestamp=datetime.utcnow())
            embed.set_author(name=("Price alert"), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
            embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
            embed.set_image(url="https://media.discordapp.net/attachments/896877291831959592/896877393392840755/ezgif-2-997863236c59.gif")
            await ctx.send(f"{ctx.author.mention}")
            await ctx.send(embed=embed)
            break
        else:
            await asyncio.sleep(10)

@slash.slash(name="dalert", description="``Notifies you if a crypto price falls below specified amount.``", guild_ids=guild_ids)
async def _dalert(ctx: SlashContext, cryptoid, fiatid, amount):
    embed=discord.Embed(timestamp=datetime.utcnow())
    embed.set_author(name=("Price alert was set correctly."), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
    embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
    await ctx.send(embed=embed)
    while True:
        a = cg.get_price(ids=cryptoid, vs_currencies=fiatid)
        if float(a[f"{cryptoid}"][f"{fiatid}"]) <= float(amount):
            embed=discord.Embed(name="lol",description=f"``{cryptoid}`` has just fallen below ``{amount}``! Now {parsePriceJson(getCryptoPrice(cryptoid, fiatid), fiatid)}",timestamp=datetime.utcnow())
            embed.set_author(name=("Price alert"), icon_url="https://cdn.discordapp.com/avatars/880792991671910420/2ed0bc90717fa677b2cad2d7f2964185.jpg?size=4096")
            embed.set_footer(text= f'Requested by {ctx.author.name}.', icon_url=ctx.guild.icon_url)
            embed.set_image(url="https://media.discordapp.net/attachments/896877291831959592/896877396869914624/ezgif-2-9e8e69a1e9ef.gif")
            await ctx.send(f"{ctx.author.mention}")
            await ctx.send(embed=embed)
            break
        else:
            await asyncio.sleep(10)


@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))

    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1

    await bot.change_presence(activity = discord.Activity(
        type = discord.ActivityType.watching,
        name = f"{servers} servers and {members} users"
    ))



async def ch_pr():
    await bot.wait_until_ready()

    servers = len(bot.guilds)
    members = 0
    for guild in bot.guilds:
        members += guild.member_count - 1
    
    statuses = [f"{servers} servers and {members} users.", "Analyzing Cryptocurrency Market.", "Slash Commands supported.", "My prefix is $"]

    while not bot.is_closed():
        status=random.choice(statuses)
        await bot.change_presence(activity=discord.Game(name=status))
        await asyncio.sleep(10)

bot.loop.create_task(ch_pr())

@bot.event
async def on_message(msg):
    try:
        if msg.mentions[0] == bot.user:
            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)
            
            pre = prefixes[str(msg.guild.id)]

            await msg.channel.send(f"My prefix is {pre}")
    except:
        pass

    await bot.process_commands(msg)

BOT_TOKEN ="yourtoken"
bot.run(BOT_TOKEN)
