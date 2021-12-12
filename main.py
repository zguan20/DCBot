import os
import discord
import random
import time
import enum


client = discord.Client()


def geneOrder():
    i = random.randint(1, 9)
    # print(i)
    list = []
    for x in range(0, 9):
        list.append(i)
        i += 1
        if i == 10:
            i = 1
    return list


print(geneOrder())

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

class stage(enum.Enum):
    prophet_check = 1
    wolf_vote = 2
    witch_poision = 3
    witch_save = 4
    day = 5
    night = 6
    hunter_shoot = 7
    wolf_boom = 8
    none = 9

idToChannels = {"groupChannel" : 919306850493677578,
                id.wolf : 919306750929305630}


rooms = [919017619779096576, 919305506730954782, 919306040938487808,
         919306205212586065, 919306317376667650, 919306397118791690,
         919306467167858799, 919306605894455327, 919306683363229736]

textRooms = [919351644074946560, 919351790447755274, 919351993980563477,
             919351993980563477, 919352093469450250, 919363312007921724,
             919363378009497730, 919363475120222281, 919363753491980308]

playersDict = {}

identityList = [id.wolf, id.wolf, id.wolf, id.civilian, id.civilian, id.civilian, id.prophet, id.witch, id.hunter]

class Player:
    def __init__(self, member, number):
        self.number = number
        self.member = member
        self.identity = None
        self.survivalStatus = True
        self.skills = None
        self.skillsFlag = False
        self.vote = -1

daysCount = 1
stage = stage.none
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
        if identityList[i] == id.wolf:
            to_channel = client.get_channel(919306750929305630)
        else:
            to_channel = client.get_channel(rooms[i])
        if(playersList[i].survivalStatus is True):
            await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
            await playersList[i].member.edit(mute=False)

async def day():
    for i in range(0, len(playersList)):
        to_channel = client.get_channel(919306850493677578)
        if(playersList[i].survivalStatus is True):
            await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
            await playersList[i].member.edit(mute=True)

async  def notify():
    if stage is stage.prophet_check:
        for p in playersList:
            if p.identity is id.prophet:
                textChannel = client.get_channel(textRooms[p.number - 1])
                await textChannel.send(
                    "预言家，你要查验谁? 请按照格式\n!check playerNumber 来进行输入和查验\n请确保关闭输入法。",
                    tts=True)
            else:
                textChannel = client.get_channel(textRooms[p.number - 1])
                await textChannel.send(
                    "预言家正在进行查验",
                    tts=True)

async def startGame():

    global rooms
    random.shuffle(identityList)
    random.shuffle(identityList)
    # random.shuffle(rooms)
    # random.shuffle(rooms)
    global idToChannels

    civilianCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = identityList[i] #assign id to player
        cur_member = playersList[i].member
        print(cur_member.name)
        # print(playersList[i].number)

        if playersList[i].number == 1:
            role = discord.utils.get(cur_member.guild.roles, name="一号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="1号")
            # print(identityList[i])
        if playersList[i].number == 2:
            role = discord.utils.get(cur_member.guild.roles, name="二号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="2号")
            # print(identityList[i])
        if playersList[i].number == 3:
            role = discord.utils.get(cur_member.guild.roles, name="三号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="3号")
            # print(identityList[i])
        if playersList[i].number == 4:
            role = discord.utils.get(cur_member.guild.roles, name="四号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="4号")
            # print(identityList[i])
        if playersList[i].number == 5:
            role = discord.utils.get(cur_member.guild.roles, name="五号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="5号")
            # print(identityList[i])
        if playersList[i].number == 6:
            role = discord.utils.get(cur_member.guild.roles, name="六号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="6号")
            # print(identityList[i])
        if playersList[i].number == 7:
            role = discord.utils.get(cur_member.guild.roles, name="七号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="7号")
            # print(identityList[i])
        if playersList[i].number == 8:
            role = discord.utils.get(cur_member.guild.roles, name="八号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="8号")
            # print(identityList[i])
        if playersList[i].number == 9:
            role = discord.utils.get(cur_member.guild.roles, name="九号")
            await cur_member.add_roles(role)
            await playersList[i].member.edit(nick="9号")
            # print(identityList[i])

        idToChannels[civilianCounter] = rooms[i]
        to_channel = client.get_channel(rooms[i])

        if identityList[i] == id.wolf:
            to_channel = client.get_channel(919306750929305630)

        # if(identityList[i] != id.wolf): #already defined a room for wolf.
        #     if (identityList[i] != id.civilian):
        #         idToChannels[identityList[i]] = rooms[i]
        #         to_channel = client.get_channel(rooms[i])
        #     else:
        #         idToChannels[civilianCounter] = rooms[i]
        #         to_channel = client.get_channel(rooms[i])

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
    for i in client.get_all_channels():
        print(i)
        print(i.id)

    #print("countdown:")
    # input time in seconds
    #t = input("Enter the time in seconds: ")

    # function call
    #countdown(int(t))


@client.event
async def on_message(message):

    theServer = client.get_guild(serverID)
    global sendToDict
    global gameInProgress
    global readyCount
    global playersList
    global playersDict
    global requiredPlayerNum
    global stage
    authorID = message.author.id
    member = await theServer.fetch_member(authorID)

    if message.content.find("!day") != -1:
        await day()
        for i in range(0, requiredPlayerNum):
            await playersList[i].member.edit(mute=False)
            countdown(5)
            await playersList[i].member.edit(mute=True)

        await night()

    # elif message.content.find("!night") != -1:
    #     await night()

    if gameInProgress == False and readyCount <= requiredPlayerNum:

        if message.content.find("!ready") != -1:
            if(authorID not in playersDict):
                readyCount += 1
                playersDict[readyCount] = member

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
                playersList.append(Player(playersDict[key], key))
            await message.channel.send("Game started")
            await startGame()

            stage = stage.prophet_check


        if(stage is stage.prophet_check):
            t = 30
            msgsList = []
            for p in playersList:
                if p.identity is id.prophet:
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "预言家，你要查验谁? 请按照格式\n!check playerNumber 来进行输入和查验。\n例如: !check 1 代表你要查验1号玩家的身份。 请确保关闭输入法。",
                        tts=True)
                    msgsList.append( await textChannel.send("剩余时间: " + str(t)) )
                else:
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "预言家正在进行查验",
                        tts=True)
                    msgsList.append( await textChannel.send("剩余时间: " + str(t)) )



            while t > 0:
                #if (t % 10 == 0 and t > 10) or (t <= 5):
                time.sleep(1)
                t -= 1
                #await theMsg.edit(content="剩余时间: " + str(t))
                for eachMsg in msgsList:
                    await eachMsg.edit(content="剩余时间: " + str(t))

                #await send(content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None, reference=None, mention_author=None)
                #https://discordpy.readthedocs.io/en/latest/api.html?highlight=send#discord.TextChannel.send
                #await message.channel.send("剩余时间:" + str(t), delete_after=10)
                #print(t)
                #await message.channel.send(str(t))


    if message.author.id in playersDict:
        if message.content.find("!day") != -1:
            await day()

        elif message.content.find("!night") != -1:
            await night()

        #if message.content.find("!reset_game") != -1:

    if message.content.find("!check") != -1 and stage is stage.prophet_check:
        print(66666666)
        msg = message.content
        arg_list = msg.split(" ")
        if(len(arg_list) > 1):
            targetNum = int(arg_list[1])
            for player in playersList:
                if player.member == message.author:
                    if player.survivalStatus is True:  # and player.identity == id.prophet
                        await message.channel.send(
                            "Player " + str(targetNum) + "s identity is: " + str(playersList[targetNum - 1].identity))

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

    if message.content.find("!vote") != -1:
        msg = message.content
        arg_list = msg.split(" ")
        announc_channal = client.get_channel(919369647109836830)

        for player in playersList:
            target = playersList[int(arg_list[1]) - 1]
            if player.member == message.author:
                if player.survivalStatus is True and target.survivalStatus is True:
                    player.vote = target.number
                    await announc_channal.send("{}号 voted {}号".format(player.number, player.vote))

    if message.content.find("!countvote") != -1:
        votes = {
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: []
        }
        announc_channal = client.get_channel(919369647109836830)

        eliminator = 1
        flatVoteList = []
        for player in playersList:
            if player.survivalStatus is True:
                votes[player.vote].append(player.number)
        for key in votes.keys():
            if len(votes[key]) != 0:
                await announc_channal.send("{} : {}".format(key, votes[key]))

        for candidate, votersList in votes.items():
            if(len(votersList) == len(votes[eliminator])):
                if(eliminator not in flatVoteList):
                    flatVoteList.append(eliminator)
                if(candidate not in flatVoteList):
                    flatVoteList.append(candidate)

            elif(len(votersList) > len(votes[eliminator])):
                eliminator = candidate
                flatVoteList.clear()

        if(len(flatVoteList) > 1):
            await announc_channal.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
        else:
            await announc_channal.send(str(eliminator) + " is out")

            i = eliminator - 1
            playersList[i].survivalStatus = False
            await playersList[i].member.edit(mute=True)
            cur_member = playersList[i].member

            if playersList[i].number == 1:
                role = discord.utils.get(cur_member.guild.roles, name="一号")

            if playersList[i].number == 2:
                role = discord.utils.get(cur_member.guild.roles, name="二号")

            if playersList[i].number == 3:
                role = discord.utils.get(cur_member.guild.roles, name="三号")

            if playersList[i].number == 4:
                role = discord.utils.get(cur_member.guild.roles, name="四号")

            if playersList[i].number == 5:
                role = discord.utils.get(cur_member.guild.roles, name="五号")

            if playersList[i].number == 6:
                role = discord.utils.get(cur_member.guild.roles, name="六号")

            if playersList[i].number == 7:
                role = discord.utils.get(cur_member.guild.roles, name="七号")

            if playersList[i].number == 8:
                role = discord.utils.get(cur_member.guild.roles, name="八号")

            if playersList[i].number == 9:
                role = discord.utils.get(cur_member.guild.roles, name="九号")

            await playersList[i].remove_roles(role)

            role = discord.utils.get(cur_member.guild.roles, name="凉凉")
            await member.add_roles(role)


    if message.content.find("!del") != -1:
        msg = message.content
        arg_list = msg.split(" ")

        for i in range(1, len(arg_list)):
            del_channel_id = channelsDict[str(arg_list[i])]
            del_channel = client.get_channel(del_channel_id)
            await del_channel.delete()

    if message.content.find("*mute") != -1:
        await member.edit(mute=True)
        await member.edit(nick=None)

    if message.content.find("*unmute") != -1:
        await member.edit(mute=False)



client.run(os.environ["TOKEN"])
