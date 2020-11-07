# Imports
import discord
from discord.ext import commands, tasks
import os
import random
from time import sleep
from itertools import cycle
import json

os.chdir("C:\\Users\\HP\\Desktop\\EVObot")

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents=intents)
status = cycle(['EVO by HYKANTUS', '.help'])


# Main tasks
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle)
    print('Ready!')
    print('--------------------------------------------------')
    print(f'Ping = {round(client.latency * 1000)}ms')
    print('--------------------------------------------------')
    change_status.start()


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


# Economy
mainshop = [{"name": "Rolex", "price": 100000, "description": "An extremely expensive watch that you can't even read."},
            {"name": "Disco ball", "price": 1000, "description": "You know what time it is? Its DISCO TIME!"},
            {"name": "Gaming PC", "price": 10000,
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


@client.command(aliases=["give", "transfer"])
async def send(ctx, member: discord.Member, amount: int = 0):
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
    await update_bank(ctx.author, -1 * amount, "bank")
    await update_bank(member, amount, "bank")

    em = discord.Embed(title=f"{ctx.author.name} sent {amount} coins to {member}!", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command()
async def slots(ctx, amount=None):
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
        em = discord.Embed(title=f"{member} has less than 500 coins. It's not worth it.", colour=discord.Color.blurple())
        await ctx.send(embed=em)
        return

    earnings = random.randrange(0, bal[0])

    await update_bank(ctx.author, earnings)
    await update_bank(member, -1 * earnings)

    em = discord.Embed(title=f"{ctx.author.name} robbed {member} for {earnings} coins!", colour=discord.Color.blurple())
    await ctx.send(embed=em)


@client.command(aliases=["store", "boutique"])
async def shop(ctx):
    em = discord.Embed(title="Shop", color=0x9089da)
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        em.add_field(name=name, value=f"__**Price**__ \n {price} coins \n __**Description:**__ \n {description}", inline=False)
    await ctx.send(embed=em)


@client.command()
async def buy(ctx, item, amount=1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            em = discord.Embed(title=f"That item does not exist!", colour=discord.Color.blurple())
            await ctx.send(embed=em)
            return
        if res[1] == 2:
            em = discord.Embed(title=f"Error: Insufficient funds to buy {amount} {item}",
                               colour=discord.Color.blurple())
            await ctx.send(embed=em)
            return

    await ctx.send(f"You just bought {amount} {item}")


@client.command(aliases=["inventory", "satchel"])
async def bag(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []

    em = discord.Embed(title="Bag")
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


# Join/leave print
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server!')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server!')


# Commands
@client.command()
async def ping(ctx):
    em = discord.Embed(title=f'Ping = {round(client.latency * 1000)}ms',
                       colour=discord.Color.blurple())
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
    em = discord.Embed(title=f'{discord.Member} has been banned, Reason {reason}',
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
            em = discord.Embed(title=f'Unbanned {user.mention}',
                               colour=discord.Color.blurple())
            await ctx.guild.unban(user)
            await ctx.send(embed=em)
    return


# Token
client.run('NzcyMzA3OTg5NTM3MDk1Njgw.X54x3Q.YLNyCMHlWr8BhHhhbtAEIw31cq0')
