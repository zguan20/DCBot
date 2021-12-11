import os
import random
import discord
from discord.ext import commands

import main

player = 0

client = discord.Client()
bot = commands.Bot(command_prefix='$')
aa = [1,2,3,4,5,6]

random.shuffle(aa)

print(aa)


@client.event
async def on_ready():
  print("logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  # await message.channel.send(message.author)
  #responding to a message
  if message.content.startswith("$hello"):
    main.player = message.author
    await message.channel.send("Hello {}".format(message.author.id))

  #creating a channel
  if message.content.startswith("$cc"):
    await message.guild.create_text_channel('cool-channel')
    await message.channel.set_permissions(message.guild.default_role, send_messages=False)

  #assgining a member to an existen role
  if message.content.startswith("$rr"):
    user = message.author
    role = discord.utils.get(user.guild.roles, name="Test")
    await user.add_roles(role)


  if message.content.startswith("$id"):
    serverID = 918987327131492382
    theServer = client.get_guild(serverID)
    i = await theServer.fetch_member(209188548941709312)
    channel = client.get_channel(919017619779096576)
    await i.move_to(channel)
    print(i)
    print(i.id)

  if message.content.startswith("$move"):
    channel = client.get_channel(919017619779096576)
    print(channel)
    # user = discord.utils.get(bot.get_all_members(), id=209188548941709312)
    # print(user)
    # print(player.name)
    await player.move_to(channel)






client.run(os.environ['TOKEN'])


