import os
import discord

client = discord.Client()

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
    await message.channel.send("Hello {}".format(message.author.name))

  #creating a channel
  if message.content.startswith("$cc"):
    await message.guild.create_text_channel('cool-channel')
    await message.channel.set_permissions(message.guild.default_role, send_messages=False)

  #assgining a member to an existen role
  if message.content.startswith("$rr"):
    user = message.author
    role = discord.utils.get(user.guild.roles, name="Test")
    await user.add_roles(role)


client.run(os.getenv('TOKEN'))
