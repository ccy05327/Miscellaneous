import discord

client = discord.Client()


@client.event
async def on_ready():
    print("Currently logged in as:", client.user)
    status = discord.Game("Full of energy!")
    await client.change_presence(status=discord.Status.online, activity=status)
    # idle = discord.Game("Snoozing...zzz")
    # await client.change_presence(status=discord.Status.idle, activity=idle)
    # dnd = discord.Game("Shuush, busy")
    # await client.change_presence(status=discord.Status.dnd, activity=dnd)
    # offline = discord.Game("You didn't see me~")
    # await client.change_presence(status=discord.Status.offline, activity=offline)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("bot"):
        temp = message.content.split(" ", 2)
        if len(temp) == 1:
            await message.channel.send("What do you want?")
        else:
            await message.channel.send(temp[1])
    if message.content.startswith("changeStatus"):
        temp = message.content.split(" ", 2)
        if len(temp) == 1:
            await message.channel.send("What do you want to change the status to?")
        else:
            status = discord.Game(temp[1])
            await client.change_presence(status=discord.Status.idle, activity=status)


client.run("OTc1NDcwOTMwNjA2MzA5NDQ2.GEg87P.DLaKoReJUTXJpGReHnIPf7g0_EMD60y5I5_0f0")
