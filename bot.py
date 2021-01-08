# Imports
import asyncio
import datetime
import json
import os
import random
from itertools import cycle
import collection as collection
import wikipedia
from chatbot import Chat, register_call
import discord
from discord.ext import tasks
from discord.ext import commands
from datetime import datetime
from time import sleep
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from pathlib import Path
from dotenv import load_dotenv

# BAT file
"""
import tkinter as tk
root = tk.Tk()

canvas1 = tk.Canvas(root, width=300, height=300)
canvas1.pack()

button1 = tk.Button(root, text='Exit', command=root.destroy)
canvas1.create_window(150, 150, window=button1)

root.mainloop()
"""

# text generator: Imports / file path (64x bit only)
"""
from typing import List
import requests
import string
import requests
import time, threading
from textgenrnn import textgenrnn
from pathlib import Path

my_file = Path('/textgenrnn_weights.hdf5')
"""

os.chdir("C:\\Users\\HP\\Desktop\\EVObot")

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
status = cycle(['EVO by HYKANTUS', '.help', '.invite'])
client.remove_command("help")


# Main tasks
@client.event
async def on_ready():
    print('Ready!')
    print('--------------------------------------------------')
    print(f'Ping = {round(client.latency * 1000)}ms')
    print('--------------------------------------------------')
    change_status.start()


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Streaming(name=(next(status)),
                                                            url='https://www.twitch.tv/hyk_evobot'))


# Join/leave message
@client.event
async def on_member_join(ctx, member):
    em = discord.Embed(title=f"{member} just left the server.", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.event
async def on_member_remove(ctx, member):
    em = discord.Embed(title=f"{member} just left the server.", colour=discord.Color.blurple())
    await ctx.send(embed=em)


# Help
@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="Help", description="use `.help <command>` for more information on a specific command.",
                       color=discord.Color.blurple())

    em.add_field(name="Moderation",
                 value="kick, ban, unban, channel_clone, channel_delete, clear, nuke, prefix, modmail",
                 inline=True)
    em.add_field(name="Fun", value="8ball, chatbot, say, spam", inline=False)
    em.add_field(name="Economy",
                 value="balance, beg, gamble, deposit, withdraw, give, rob, shop, inventory, buy, sell, leaderboard",
                 inline=True)
    em.add_field(name="Miscellaneous", value="ping, invite, timer", inline=False)

    await ctx.send(embed=em)


# Help moderation
@help.command()
async def kick(ctx):
    em = discord.Embed(title="Kick", description="Kicks member from guild", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="kick <member> [reason]")
    await ctx.send(embed=em)


@help.command()
async def ban(ctx):
    em = discord.Embed(title="Ban", description="Bans member from guild", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="ban <member> [reason]")
    await ctx.send(embed=em)


@help.command()
async def unban(ctx):
    em = discord.Embed(title="Unnban", description="unbans member from guild", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="unban <member_name>#[tag]")
    await ctx.send(embed=em)


@help.command()
async def channel_clone(ctx):
    em = discord.Embed(title="channel_clone", description="Clones a channel", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="channel_clone #<channel_name>")
    await ctx.send(embed=em)


@help.command()
async def channel_delete(ctx):
    em = discord.Embed(title="channel_delete", description="Deletes a channel", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="channel_clone #<channel_name>")
    await ctx.send(embed=em)


@help.command()
async def clear(ctx):
    em = discord.Embed(title="Clear", description="Clears a set amount of messages", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="clear [message_amount]")
    await ctx.send(embed=em)


@help.command()
async def nuke(ctx):
    em = discord.Embed(title="Nuke", description="Removes all messages on a given channel",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="nuke #<channel_name>")
    await ctx.send(embed=em)


@help.command()
async def modmail(ctx):
    em = discord.Embed(title="Mod Mail",
                       description="Sends a DM to a specific member or role (Syntax must be used in a private channel named 'mod-mail'",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="modmail @(role-mention) [message]")
    await ctx.send(embed=em)


# Help fun
@help.command(aliases=["8ball"])
async def _8ball(ctx):
    em = discord.Embed(title="8ball", description="Answers a given question", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="8ball [question]")
    await ctx.send(embed=em)


@help.command(aliases=["cb", "chat", "chatb", "cbot", "talk", "talkbot"])
async def chatbot(ctx):
    em = discord.Embed(title="Chatbot", description="Simple chatbot A.I", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="chatbot [your_message]")
    await ctx.send(embed=em)


@help.command(aliases=["say_spam", "spam_say"])
async def spam(ctx):
    em = discord.Embed(title="Spam", description="Spams a text string by amount of messages specified",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="spam [amt of messages to spam] (message to spam)")
    await ctx.send(embed=em)


# Help miscellaneous
@help.command()
async def ping(ctx):
    em = discord.Embed(title="Ping", description="Checks ping connection to client in ms",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="ping")
    await ctx.send(embed=em)


@help.command()
async def invite(ctx):
    em = discord.Embed(title="Ping", description="Gives a link to invite the bot to your own server",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="invite")
    await ctx.send(embed=em)


# Help economy
@help.command()
async def balance(ctx):
    em = discord.Embed(title="Balance", description="Shows wallet and bank amount", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="balance")
    await ctx.send(embed=em)


@help.command()
async def beg(ctx):
    em = discord.Embed(title="Beg", description="Gives a random amount of coins which will be added to your wallet",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="beg")
    await ctx.send(embed=em)


@help.command()
async def gamble(ctx):
    em = discord.Embed(title="Gamble",
                       description="Plays a slots game which doubles the amount of coins inputted. If the game is lost, the coins will not be refunded",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="gamble [coin_amount]")
    await ctx.send(embed=em)


@help.command()
async def deposit(ctx):
    em = discord.Embed(title="Deposit", description="Deposits coins from wallet to the bank",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="deposit [coin_amount]")
    await ctx.send(embed=em)


@help.command()
async def withdraw(ctx):
    em = discord.Embed(title="Withdraw", description="Withraws coins from bank and puts it into the wallet",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="withdraw [coin_amount]")
    await ctx.send(embed=em)


@help.command()
async def give(ctx):
    em = discord.Embed(title="Give", description="Gives a specified amount of coins to a given user",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="give @[username]#[tag] [coin_amount]")
    await ctx.send(embed=em)


@help.command()
async def rob(ctx):
    em = discord.Embed(title="Rob", description="Robs a specific user for a random amount of coins",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="rob @[username]#[tag]")
    await ctx.send(embed=em)


@help.command()
async def shop(ctx):
    em = discord.Embed(title="Shop", description="Displays the shop with name, price, and description",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="shop")
    await ctx.send(embed=em)


@help.command()
async def inventory(ctx):
    em = discord.Embed(title="Inventory", description="Shows inventory", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="inventory")
    await ctx.send(embed=em)


@help.command()
async def buy(ctx):
    em = discord.Embed(title="Buy", description="Buys an item from the shop", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="buy [item_name] [amount]")
    await ctx.send(embed=em)


@help.command()
async def sell(ctx):
    em = discord.Embed(title="Sell", description="Sells an item from your inventory", colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="sell [item_name] [amount]")
    await ctx.send(embed=em)


@help.command()
async def leaderboard(ctx):
    em = discord.Embed(title="Leaderboard", description="Shows richest users (descending)",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="leaderboard")
    await ctx.send(embed=em)


@help.command()
async def timer(ctx):
    em = discord.Embed(title="Timer",
                       description="Starts a timer and mentions the user who has run the command when the timer has finished",
                       colour=discord.Color.blurple())
    em.add_field(name="**Syntax**", value="timer [mins(in numbers)]")
    await ctx.send(embed=em)


# Commands
@client.command()
async def ping(ctx):
    em = discord.Embed(title=f'Ping = {round(client.latency * 1000)}ms',
                       colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command()
async def invite(ctx):
    em = discord.Embed(title=f"Invite link requested by {ctx.author.name}",
                       description="Click [**here**](https://discord.com/api/oauth2/authorize?client_id=772307989537095680&permissions=8&scope=bot) to add this bot to your server",
                       colour=discord.Colour.blurple())
    await ctx.send(embed=em)


@client.command(aliases=['8ball', '8b', '8bl', 'eightball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain.',
                 'It is decidedly so.',
                 'Without a doubt.',
                 'Yes - definitely.',
                 'You may rely on it.',
                 'As I see it, yes.',
                 'Most likely.',
                 'Outlook good.',
                 'Yes.',
                 'Signs point to yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again.',
                 'Do not count on it.',
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    em = discord.Embed(title=f'Question: {question}\nAnswer: {random.choice(responses)}',
                       colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command(aliases=['purge'])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    em = discord.Embed(title=f'Deleting. . .',
                       colour=discord.Color.blurple())
    await ctx.send(embed=em)
    await ctx.channel.purge(limit=amount + 2)


@clear.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title=f'Error: Missing argument(s): amount of messages',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)


@client.command()
@commands.has_permissions(manage_messages=True)
async def nuke(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit()))
    existing_channel = client.get_channel(channel_id)
    if existing_channel is not None:
        await existing_channel.clone(reason="Has been nuked")
        em = discord.Embed(title=f'Nuked!',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
        await existing_channel.delete()
        await ctx.send(embed=em)
    else:
        if existing_channel is not None:
            await existing_channel.clone(reason="Has been nuked")
        em = discord.Embed(title=f'No channel named {channel_name} was found',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)


@nuke.error
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        em = discord.Embed(title=f'Error: Missing argument(s): channel name',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)


@client.command(aliases=['channel_duplicate'])
@commands.has_permissions(manage_channels=True)
async def channel_clone(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit()))
    existing_channel = client.get_channel(channel_id)
    if existing_channel is not None:
        await existing_channel.clone(reason="Has been cloned")
        em = discord.Embed(title=f'Cloned!',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
        await ctx.send(f'Cloned!')
    else:
        em = discord.Embed(title=f'Error: No channel called {channel_name} found',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)


@client.command(aliases=['channel_remove'])
@commands.has_permissions(manage_channels=True)
async def channel_delete(ctx, channel_name):
    channel_id = int(''.join(i for i in channel_name if i.isdigit()))
    existing_channel = client.get_channel(channel_id)
    if existing_channel is not None:
        em = discord.Embed(title=f'{channel_name} has been deleted!',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
    else:
        em = discord.Embed(title=f'Error: No channel called {channel_name} found',
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    em = discord.Embed(title=f'{discord.Member} has been kicked, Reason {reason}',
                       colour=discord.Color.blurple())
    await member.kick(reason=reason)
    await ctx.send(embed=em)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    em = discord.Embed(title=f'{member} has been banned \nReason: {reason}',
                       colour=discord.Color.blurple())
    await member.ban(reason=reason)
    await ctx.send(embed=em)


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            em = discord.Embed(title=f'Unbanned {member_name}',
                               colour=discord.Color.blurple())
            await ctx.guild.unban(user)
            await ctx.send(embed=em)
    return


@client.command(pass_context=True)
async def timer(ctx, seconds: int, member: discord.Member = None):
    embed = discord.Embed(title=f'Timer', colour=discord.Colour.blurple())

    end = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)

    embed.add_field(name="Timer set for:", value=f"{seconds} seconds")
    embed.add_field(name="React with:", value=f"⏱")
    embed.set_footer(text=f"Command called by {ctx.author}", icon_url=ctx.author.avatar_url)

    my_msg = await ctx.send(embed=embed)
    await my_msg.add_reaction("⏱")
    await asyncio.sleep(seconds)
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    em = discord.Embed(title=f"Timer has ended, {ctx.author.mention}")
    await ctx.send(embed=em)


@client.command(aliases=["repeat"])
async def say(ctx, *text):
    await ctx.channel.purge(limit=1)
    sleep(0.1)
    text = " ".join(text)
    await ctx.send(text)


@client.command(aliases=["say_spam", "spam_say"])
async def spam(ctx, int: int, *, word):
    await ctx.channel.purge(limit=1)
    sleep(0.1)
    for i in range(int):
        await ctx.send(word)


# Economy
mainshop = [{"name": "rolex", "price": 100000, "description": "An extremely expensive watch that you can't even read."},
            {"name": "discoball", "price": 1000, "description": "You know what time it is? Its DISCO TIME!"},
            {"name": "computer", "price": 10000,
             "description": "A beast of a gaming PC. But obviously, you use it for Among us and Geometry Dash"}]


@client.command(aliases=["bal"])
async def balance(ctx):
    await open_account(ctx.author)
    user = ctx.author

    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    em = discord.Embed(title=f"{ctx.author.name}'s balance", colour=discord.Color.blurple())
    em.add_field(name="Wallet balance", value=wallet_amt)
    em.add_field(name="Bank balance", value=bank_amt)
    await ctx.send(embed=em)


@client.command()
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()

    user = ctx.author

    earnings = random.randrange(10, 500)

    person = ('HYKANTUS', 'Mr Beast', 'PewDiePie', 'T-series', 'Casey Neistat', 'Jacksfilms')

    em = discord.Embed(title=f"{random.choice(person)} just gave {ctx.author.name} {earnings} coins!",
                       colour=discord.Color.blurple())
    await ctx.send(embed=em)

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f)


async def update_bank(user, change=0, mode="wallet"):
    await open_account(user)
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return [users[str(user.id)]['wallet'], users[str(user.id)]['bank']]


@client.command(aliases=["with"])
async def withdraw(ctx, amount=None):
    if amount is None:
        await ctx.send("Error: Missing argument(s): amount of money")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount == 0:
        em = discord.Embed(title=f"Error: Insufficient funds",
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    if amount < bal[0]:
        em = discord.Embed(title=f"Error: Amount is not positive",
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return

    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1 * amount, "bank")

    em = discord.Embed(title=f"{ctx.author.name} withdrew {amount} coins!",
                       colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command(aliases=["dep"])
async def deposit(ctx, amount: int = 0):
    if amount == 0:
        await ctx.send("Error: Missing argument(s): amount of money")
        return
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        em = discord.Embed(title=f"Error: Insufficient funds", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    if amount < 0:
        em = discord.Embed(title=f"Error: Amount is not positive", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    await update_bank(ctx.author, -1 * amount)
    await update_bank(ctx.author, amount, "bank")

    em = discord.Embed(title=f"{ctx.author.name} deposited {amount} coins to the bank!", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command(aliases=["send", "transfer"])
async def give(ctx, member: discord.Member, amount: int = 0):
    await open_account(ctx.author)
    await open_account(member)
    if amount == 0:
        await ctx.send("Error: Missing argument(s): amount of money")
        return
    bal = await update_bank(ctx.author)
    if amount == "all":
        amount = bal[0]

    amount = int(amount)
    if amount > bal[0]:
        em = discord.Embed(title=f"Error: Insufficient funds", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    if amount < 0:
        em = discord.Embed(title=f"Error: Amount is not positive", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    await update_bank(ctx.author, -1 * amount, "wallet")
    await update_bank(member, amount, "wallet")

    em = discord.Embed(title=f"{ctx.author.name} sent {amount} coins to {member}!", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command()
async def gamble(ctx, amount=None):
    await open_account(ctx.author)
    await open_account(ctx.author)
    if amount == 0:
        await ctx.send("Error: Missing argument(s): amount of money")
        return
    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        em = discord.Embed(title=f"Error: Insufficient funds", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return
    if amount < 0:
        em = discord.Embed(title=f"Error: Amount is not positive", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return

    final = []
    for i in range(3):
        a = random.choice(["X", "O", "Q"])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
        await update_bank(ctx.author, 2 * amount)
        em = discord.Embed(title=f"You win!", colour=discord.Color.blurple())
        await ctx.send(embed=em)
    else:
        await update_bank(ctx.author, -1 * amount)
        em = discord.Embed(title=f"You lose.", colour=discord.Color.blurple())
        await ctx.send(embed=em)


@client.command(aliases=["steal"])
async def rob(ctx, member: discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    if bal[0] < 500:
        em = discord.Embed(title=f"{member} has less than 500 coins. It's not worth it.",
                           colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return

    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author, earnings)
    await update_bank(member, -1 * earnings)

    em = discord.Embed(title=f"{ctx.author.name} robbed {member} for {earnings} coins!", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command(aliases=["store", "boutique"])
async def shop(ctx):
    em = discord.Embed(title="Shop", colour=discord.Color.blurple())
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name=name, value=f"**Price** \n {price} coins \n **Description:** \n {description}",
                     inline=False)
    await ctx.send(embed=em)


@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            embedded = discord.Embed(title=f"Item does not exist, {ctx.author.name}")
            await ctx.send(embed=embedded)
            return
        if res[1] == 2:
            embed = discord.Embed(
                title=f"{ctx.author.name}, you don't have enough money in your wallet to buy {amount} {item}",
                colour=discord.Colour.blurple())
        await ctx.send(embed=embed)
        return
    em = discord.Embed(title=f"You just bought {amount} {item}", colour=discord.Colour.blurple())
    await ctx.send(embed=em)


@client.command(aliases=["bag", "satchel"])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Inventory", colour=discord.Color.blurple())
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        em.add_field(name=name, value=amount)

    await ctx.send(embed=em)


async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ is None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t is None:
            obj = {"item": item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"] = [obj]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")

    return [True, "Worked"]


@client.command()
async def sell(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            em = discord.Embed(title=f"That item does not exist", colour=discord.Colour.blurple())
            await ctx.send(embed=em)
            await ctx.send("That Object isn't there!")
            return
        if res[1] == 2:
            em = discord.Embed(title=f"You don't have {amount} {item} in your inventory",
                               colour=discord.Colour.blurple())
            await ctx.send(embed=em)
            await ctx.send(f"You don't have {amount} {item} in your bag.")
            return
        if res[1] == 3:
            em = discord.Embed(title=f"You don't have this item({item}) in your inventory",
                               colour=discord.Colour.blurple())
            await ctx.send(embed=em)
            return
        em = discord.Embed(title=f"{ctx.author.name} just sold {amount} {item}", colour=discord.Colour.blurple())
    await ctx.send(embed=em)


async def sell_this(user, item_name, amount, price=None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price == None:
                price = 0.9 * item["price"]
            break

    if name_ == None:
        return [False, 1]

    cost = price * amount

    users = await get_bank_data()

    bal = await update_bank(user)

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False, 2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            return [False, 3]
    except:
        return [False, 3]

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost, "wallet")

    return [True, "Worked"]


@client.command(aliases=["lb", "rich", "networth", "nw"])
async def leaderboard(ctx, x=1):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total, reverse=True)

    em = discord.Embed(title=f"Top {x} Richest People",
                       description="Based on Net Worth",
                       colour=discord.Colour.blurple())
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name=f"{index}. {name}", value=f"{amt}", inline=False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed=em)


# open_account and get_bank_data
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)
    return True


async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users


# Giveaways
def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]


@client.command(aliases=["gw", "gwstart", "gwbegin", "giveawaystart", "giveaway_start", "giveaway", "gbegin"])
@commands.has_role("giveaways")
async def gstart(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

    questions = ["Which channel should it be hosted in?",
                 "What should be the duration of the giveaway? (s|m|h|d)",
                 "What is the prize of the giveaway?"]

    answers = []

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)

        try:
            msg = await client.wait_for('message', timeout=15.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


@client.command()
@commands.has_role("giveaways")
async def reroll(ctx, channel: discord.TextChannel, id_: int):
    try:
        new_msg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations! The new winner is {winner.mention}.!")


# AI Chatbot
@register_call("whoIs")
def who_is(query, session_id="general"):
    try:
        return wikipedia.summary(query)
    except Exception:
        for new_query in wikipedia.search(query):
            try:
                return wikipedia.summary(new_query)
            except Exception:
                pass
    return "I don't know " + query


template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chatbottemplate.template")
chat = Chat(template_file_path)


@client.command(aliases=["cb", "chat", "chatb", "cbot", "talkbot", "talkb", "tbot", "tb"], pass_context=True)
async def chatbot(ctx, *, message):
    result = chat.respond(message)
    if len(result) <= 2048:
        embed = discord.Embed(title="ChatBot", description=result, color=discord.Colour.blurple())
        await ctx.send(embed=embed)
    else:
        embedList = []
        n = 2048
        embedList = [result[i:i + n] for i in range(0, len(result), n)]
        for num, item in enumerate(embedList, start=1):
            if num == 1:
                embed = discord.Embed(title="Chatbot AI", description=item, color=discord.Colour.blurple())
                embed.set_footer(text="page {}".format(num))
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=item, color=discord.Colour.blurple())
                embed.set_footer(text="page {}".format(num))
                await ctx.send(embed=embed)


# text generator: Code(64x bit only)
"""
@client.command()
async def textgenerator(ctx):
    await client.wait_until_ready()
    while not client.is_closed():
        if my_file.exists():
            t = textgenrnn('textgenrnn_weights.hdf5')
        else:
            t = textgenrnn()
            t.train_from_file('index'
                              '++++++.txt', num_epochs=1)
            generation = (t.generate(1, temperature=0.5, return_as_list=True, )[0])
            embed = discord.Embed(title="AI text generator", description=generation, color=discord.Colour.blurple())
            embed.set_footer(text="Based on: Holes by Luis Sarchar")
            await ctx.send(embed=embed)
await asyncio.sleep(1800)
client.loop.create_task(textgenerator())
"""

# Swear detector

"""
# API key = https://rapidapi.com/neutrinoapi/api/bad-word-filter
api_key = "f2026727demsha99e60c44e31e34p133c2bjsn5378ad9fd1cb"

TOKEN = "NzcyMzA3OTg5NTM3MDk1Njgw.X54x3Q.V0H_vtFQn2I5uy_BGbzSg_4sOWQ"

hello = ["hi", "hi there", "hello", "hello there", "hi evo", "hi evobot", "hello evo", "hello evobot"]
damn = ["damn bro", "damn bro."]
evo = ["evo", "evobot", "EVO", "EVObot", "EVOBOT"]


@client.event
async def on_message(message):
    if message.content in evo:
        await message.channel.send(
            'Hello! My name is EVObot (Developed by HYKANTUS). \nPlease do `.help` to see what I can do.\nInvite me to your own server by doing `.invite`')

    if message.content in damn:
        await message.channel.send('you got the whole squad laughing.')

    if message.content in hello:
        await message.channel.send('Hello')

    url = "https://neutrinoapi-bad-word-filter.p.rapidapi.com/bad-word-filter"

    payload = f"censor-character=*&content={message.content}"
    headers = {'content-type': "application/x-www-form-urlencoded", 'x-rapidapi-key': api_key,
               'x-rapidapi-host': "neutrinoapi-bad-word-filter.p.rapidapi.com"}

    response = requests.request("POST", url, data=payload, headers=headers)

    if '"is-bad":true' in response.text:
        await message.delete()
        em = discord.Embed(title=f"@{message.author} just swore!", color=discord.Colour.blurple())
        await message.channel.send(embed=em)"""


# Mod mail
@client.event
async def on_message(message):
    empty_array = []

    if message.author == client.user:
        return
    if str(message.channel.type) == "public":
        if message.attachments != empty_array:
            files = message.attachments
            await message.send("[" + message.author.display_name + "]")

            for file in files:
                await message.send(file.url)
        else:
            await message.send("[" + message.author.display_name + "] " + message.content)

    elif str(message.channel) == "dm" and message.content.startswith("."):
        member_object = message.mentions[0]
        if message.attachments != empty_array:
            files = message.attachments
            await member_object.send("From:" + message.author.display_name)

            for file in files:
                await member_object.send(file.url)
        else:
            index = message.content.index(" ")
            string = message.content
            mod_message = string[index:]
            await member_object.send("From:" + message.author.display_name + "\n" + mod_message)


# AFK
"""
@client.group(invoke_without_command=True)
async def afk(ctx):
    em = discord.Embed(title="AFK", description="Do ```.afk on``` or ```.afk off```",
                       color=discord.Color.blurple())
    await ctx.send(embed=em)


@afk.command()
async def on(ctx):
    current_nick = ctx.author.nick
    em = discord.Embed(title=f"{ctx.author.mention} is now AFK.", colour=discord.Colour.blurple())
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"[AFK] {ctx.author.name}")
    await ctx.author.edit(nick=current_nick)


@afk.command()
async def off(ctx):
    current_nick = ctx.author.nick
    em = discord.Embed(title=f"{ctx.author.mention} is no longer AFK.", colour=discord.Colour.blurple())
    await ctx.send(embed=em)
    await ctx.author.edit(nick=f"{ctx.author.name}")
    await ctx.author.edit(nick=current_nick)
"""
"""
afkdict = {}


@client.command()
async def afk(ctx, message):
    global afkdict

    # remove member from afk dict if they are already in it
    if ctx.message.author in afkdict:
        afkdict.pop(ctx.message.author)
        await ctx.send('you are no longer afk')


    else:
        afkdict[ctx.message.author] = message
        await ctx.send(f"You are now afk with message - {message}")


@client.event
async def on_message(message):
    global afkdict

    # check if mention is in afk dict
    for member in message.mentions:  # loops through every mention in the message
        if member != message.author:  # checks if mention isn't the person who sent the message
            if member in afkdict:  # checks if person mentioned is afk
                afkmsg = afkdict[member]  # gets the message the afk user set
                await message.channel.send(
                    f" {member} is afk - {afkmsg}")  # send message to the channel the message was sent to
"""

client.run('NzcyMzA3OTg5NTM3MDk1Njgw.X54x3Q.V0H_vtFQn2I5uy_BGbzSg_4sOWQ')
