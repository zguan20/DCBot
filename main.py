import os
import discord
import random
import time
import enum


client = discord.Client()


'''
Text Channels   919001388711825438
Voice Channels   919017619779096576
general   918987327131492384
General   918987327131492386
repos   918987327131492385
1号玩家   918987327131492387
'''

class id(enum.Enum):
    wolf = 1
    civilian = 2
    prophet = 3
    witch = 4
    hunter = 5

class skills(enum.Enum):
    king_wolf = 1
    wolf = 2
    prophet = 3
    witch = 4
    hunter = 5


idToChannels = {"groupChannel" : 919306850493677578,
                id.wolf : 919306750929305630}

idToRoles = {}

rooms = [919017619779096576, 919305506730954782, 919306040938487808,
         919306205212586065, 919306317376667650, 919306397118791690,
         919306467167858799, 919306605894455327, 919306683363229736]

'''
idToChannels = {
    id.wolf : 919306750929305630,
    1 : 919017619779096576,
    2 : 919305506730954782,
    3 : 919306040938487808,
    id.witch : 919306205212586065,
    id.hunter : 919306317376667650,
    id.prophet : 919306397118791690,
    "groupChannel" : 919306850493677578
}
'''

playersDict = {}

identityList = [id.wolf, id.wolf, id.wolf, id.civilian, id.civilian, id.civilian, id.prophet, id.witch, id.hunter]

class Player:
    def __init__(self, member):
        self.member = member
        self.identity = None
        self.survivalStatus = True
        self.skills = None
        self.skillsFlag = False
        self.vote = -1

requiredPlayerNum = 1
playersList = []
readyCount = 0
gameInProgress = False

num_hero = 3
num_civilian = 3
num_wolf = 3

channelsDict = {
    "Text Channels" : 9190013887118254384,
    "Voice Channels" : 919017619779096576,
    "general" : 918987327131492384,
    "General" : 918987327131492386,
    "repos" : 918987327131492385,
    "1号玩家" : 919017619779096576
}


serverID = 918987327131492382


# define the countdown func.
def countdown(t):
    while t:
        time.sleep(1)
        t -= 1
        print(t)

    print('Fire in the hole!!')


async def night():
    civilianCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = identityList[i]  # assign id to player

        #move players to their rooms
        if (identityList[i] != id.civilian):
            to_channel = client.get_channel(idToChannels[identityList[i]])
        else:
            to_channel = client.get_channel(idToChannels[civilianCounter])
        await playersList[i].member.move_to(to_channel)  # move to the corresponding channel

async def day():
    for i in range(0, len(playersList)):
        to_channel = client.get_channel(idToChannels["groupChannel"])
        await playersList[i].member.move_to(to_channel)  # move to the corresponding channel

async def startGame():

    global rooms
    random.shuffle(identityList)
    random.shuffle(identityList)
    random.shuffle(rooms)
    random.shuffle(rooms)
    global idToChannels

    civilianCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = identityList[i] #assign id to player

        if(identityList[i] != id.wolf): #already defined a room for wolf.
            if (identityList[i] != id.civilian):
                idToChannels[identityList[i]] = rooms[i];
                to_channel = client.get_channel(idToChannels[identityList[i]])
            else:
                idToChannels[civilianCounter] = rooms[i];
                to_channel = client.get_channel(idToChannels[civilianCounter])

        if identityList[i] == id.wolf:
            pass

        elif identityList[i] == id.prophet:
            pass

        elif identityList[i] == id.witch:
            pass

        elif identityList[i] == id.hunter:
            pass

        else: #civilian
            pass

        await playersList[i].member.move_to(to_channel)  # move to the corresponding channel



@client.event
async def on_ready():

    print('We have logged in as {0.user}'.format(client))

    theServer = client.get_guild(serverID)
    #get guild (server) -> [<Guild id=918987327131492382 name='狼人杀' shard_id=None chunked=False member_count=6>]
    server = client.guilds;
    users = client.users;

    print(server)
    print(users)
    print(theServer.roles)

    print("---")
    for i in client.get_all_members():
        print(i)

    #print("countdown:")
    # input time in seconds
    #t = input("Enter the time in seconds: ")

    # function call
    #countdown(int(t))


@client.event
async def on_message(message):

    theServer = client.get_guild(serverID)
    global gameInProgress
    global readyCount
    global playersList
    global playersDict
    global requiredPlayerNum
    authorID = message.author.id
    member = await theServer.fetch_member(authorID)

    if gameInProgress == False and readyCount <= requiredPlayerNum:

        if message.content.find("!ready") != -1:
            if(authorID not in playersDict):
                readyCount += 1
                playersDict[authorID] = member

            # await message.channel.send("Hi " + str(member) + " " + str(authorID)) # If the user says !hello we will send back hi
            await message.channel.send(
                str(member) + " is ready. Need " + str(requiredPlayerNum - readyCount) + " more players to start")



        if message.content.find("!unready") != -1:
            if authorID in playersDict:
                playersDict.pop(authorID)
                readyCount -= 1
                await message.channel.send(
                    str(member) + " is unready. Need " + str(requiredPlayerNum - readyCount) + " more players to start")

        if message.content.find("!start") != -1 and readyCount >= requiredPlayerNum:
            gameInProgress = True

            for key in playersDict.keys():
                playersList.append(Player(playersDict[key]))
            await message.channel.send("Game started")
            await startGame()

    if message.author.id in playersDict:
        if message.content.find("!day") != -1:
            await day()

        elif message.content.find("!night") != -1:
            await night()

        #if message.content.find("!reset_game") != -1:


    if message.content.find("!hello") != -1:
        authorID = message.author.id

        readyCount += 1
        member = await theServer.fetch_member(authorID)
        playersDict[authorID] = member

        playersList.append(Player(playersDict[authorID]))

        for e in playersList:
            print(str(readyCount) + " " + str(len(playersDict)) + " >> " + str(e.member.id))

        playersList[0].identity = id.wolf  # assign id to player

        to_channel = client.get_channel(idToChannels[id.wolf])
        await playersList[0].member.move_to(to_channel)  # move to the corresponding channel


    if message.content.find("!move") != -1:
        authorID = message.author.id
        theMember = await theServer.fetch_member(authorID)
        to_channel = client.get_channel(channelsDict["1号玩家"])
        await theMember.move_to(to_channel)


    if message.content.find("!cv") != -1:
        msg = message.content
        arg_list = msg.split(" ")

        for i in range(1, len(arg_list)):
            newChannel = await theServer.create_voice_channel(arg_list[i])
            print(newChannel)
            channelsDict[arg_list[i]] = newChannel.id



    if message.content.find("!del") != -1:
        msg = message.content
        arg_list = msg.split(" ")

        for i in range(1, len(arg_list)):
            del_channel_id = channelsDict[str(arg_list[i])]
            del_channel = client.get_channel(del_channel_id)
            await del_channel.delete()

    if message.content.find("*mute") != -1:
        await member.edit(mute=True)

    if message.content.find("*unmute") != -1:
        await member.edit(mute=False)



client.run(os.environ["TOKEN"])






