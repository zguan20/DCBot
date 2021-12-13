import os
import discord
import random
import time
import enum

import main

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
    prophet_check = 1
    wolf_vote = 2
    witch_poison = 3
    witch_save = 4
    hunter_shoot = 7
    wolf_boom = 8
    none = 9


class stage(enum.Enum):
    prophet_check = 1
    wolf_vote = 2
    女巫阶段 = 3
    day = 5
    night = 6
    hunter_shoot = 7
    wolf_boom = 8
    voting = 9
    none = -1


idToChannels = {"groupChannel": 919306850493677578,
                id.wolf: 919306750929305630}

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
        self.skills = []
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
    "Text Channels": 9190013887118254384,
    "Voice Channels": 919017619779096576,
    "general": 918987327131492384,
    "General": 918987327131492386,
    "repos": 918987327131492385,
    "1号玩家": 919017619779096576
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
    global stage

    stage = stage.prophet_check
    civilianCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = identityList[i]  # assign id to player

        # move players to their rooms
        if identityList[i] == id.wolf:
            to_channel = client.get_channel(919306750929305630)
        else:
            to_channel = client.get_channel(rooms[i])
        if (playersList[i].survivalStatus == 2):
            await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
            await playersList[i].member.edit(mute=False)


async def day():
    global stage
    stage = stage.day
    for i in range(0, len(playersList)):
        to_channel = client.get_channel(919306850493677578)
        if (playersList[i].survivalStatus is True):
            await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
            await playersList[i].member.edit(mute=True)


async def notify():
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

theWitch = Player(None, -1)
async def startGame():

    global rooms
    random.shuffle(identityList)
    random.shuffle(identityList)
    # random.shuffle(rooms)
    # random.shuffle(rooms)
    global idToChannels

    civilianCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = id.witch#identityList[i] #assign id to player
        playersList[i].survivalStatus = 1
        playersList[i].skills = [skills.witch_save, skills.witch_poison]
        cur_member = playersList[i].member
        print(cur_member.name)
        # print(playersList[i].number)

        main.theWitch = playersList[i]

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

        # if identityList[i] == id.wolf:
        #     to_channel = client.get_channel(919306750929305630)

        # if identityList[i] == id.wolf:
        #     playersList[i].skills = [skills.wolf_kill]
        #
        # elif identityList[i] == id.prophet:
        #     playersList[i].skills = [skills.prophet_check]
        #
        # elif identityList[i] == id.witch:
        #     playersList[i].skills = [skills.witch_save, skills.witch_poison]
        #
        # elif identityList[i] == id.hunter:
        #     playersList[i].skills = [skills.hunter_shoot]

        await playersList[i].member.move_to(to_channel)  # move to the corresponding channel


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    theServer = client.get_guild(serverID)
    # get guild (server) -> [<Guild id=918987327131492382 name='狼人杀' shard_id=None chunked=False member_count=6>]
    server = client.guilds;
    users = client.users;

    print(server)
    print(users)
    print(theServer.roles)

    print("---")
    for i in client.get_all_channels():
        print(i)
        print(i.id)

    # print("countdown:")
    # input time in seconds
    # t = input("Enter the time in seconds: ")

    # function call
    # countdown(int(t))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    theServer = client.get_guild(serverID)
    global sendToDict
    global gameInProgress
    global readyCount
    global playersList
    global playersDict
    global requiredPlayerNum
    global stage
    global dayflag
    global votingflag
    global wolf_kill_flag
    global witchFlag
    theWitch = main.theWitch
    dayflag = False
    authorID = message.author.id
    member = await theServer.fetch_member(authorID)

    async def countvote():
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
            if (len(votersList) == len(votes[eliminator])):
                if (eliminator not in flatVoteList):
                    flatVoteList.append(eliminator)
                if (candidate not in flatVoteList):
                    flatVoteList.append(candidate)

            elif (len(votersList) > len(votes[eliminator])):
                eliminator = candidate
                flatVoteList.clear()

        if (len(flatVoteList) > 1):
            await announc_channal.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
        else:
            await announc_channal.send(str(eliminator) + " is out")

            # i = eliminator - 1
            # playersList[i].survivalStatus = False
            # await playersList[i].member.edit(mute=True)
            # cur_member = playersList[i].member
            #
            # if playersList[i].number == 1:
            #     role = discord.utils.get(cur_member.guild.roles, name="一号")
            #
            # if playersList[i].number == 2:
            #     role = discord.utils.get(cur_member.guild.roles, name="二号")
            #
            # if playersList[i].number == 3:
            #     role = discord.utils.get(cur_member.guild.roles, name="三号")
            #
            # if playersList[i].number == 4:
            #     role = discord.utils.get(cur_member.guild.roles, name="四号")
            #
            # if playersList[i].number == 5:
            #     role = discord.utils.get(cur_member.guild.roles, name="五号")
            #
            # if playersList[i].number == 6:
            #     role = discord.utils.get(cur_member.guild.roles, name="六号")
            #
            # if playersList[i].number == 7:
            #     role = discord.utils.get(cur_member.guild.roles, name="七号")
            #
            # if playersList[i].number == 8:
            #     role = discord.utils.get(cur_member.guild.roles, name="八号")
            #
            # if playersList[i].number == 9:
            #     role = discord.utils.get(cur_member.guild.roles, name="九号")
            #
            # await playersList[i].remove_roles(role)
            #
            # role = discord.utils.get(cur_member.guild.roles, name="凉凉")
            # await member.add_roles(role)

    async def countkill():
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

        for player in playersList:
            if player.survivalStatus is True and player.identity is id.wolf:
                votes[player.vote].append(player.number)
        for key in votes.keys():
            if len(votes[key]) != 0:
                await announc_channal.send("{} : {}".format(key, votes[key]))

    if message.content.find("!day") != -1:
        # await day()
        # stage = stage.day
        # for i in range(0, requiredPlayerNum):
        #     await playersList[i].member.edit(mute=False)
        #     t = 20
        #     while t > 0:
        #         print(t)
        #         if(message.content.find("!boom")):
        #             print("in boom 1")
        #         time.sleep(1)
        #         t -= 1
        #     await playersList[i].member.edit(mute=True)
        #
        # await night()

        # elif message.content.find("!night") != -1:
        # await night()
        # stage = stage.night
        stage = stage.day

    if readyCount <= requiredPlayerNum:

        if message.content.find("!ready") != -1:
            if (authorID not in playersDict):
                readyCount += 1
                playersDict[readyCount] = member

            # await message.channel.send("Hi " + str(member) + " " + str(authorID)) # If the user says !hello we will send back hi
            await message.channel.send(
                str(member) + " is ready. Need " + str(requiredPlayerNum - readyCount) + " more players to start")

        if message.content.find("!boom") != -1 and stage is stage.day:
            print("自爆")
            dayflag = True
            await night()

        if message.content.find("!save") != -1 and stage is stage.女巫阶段:
            witchFlag = True
            msg = message.content
            arg_list = msg.split(" ")

            if len(arg_list) < 2:
                textChannel = client.get_channel(textRooms[theWitch.number - 1])
                await textChannel.send("请输入!save playerNumber")
                return

            target = playersList[int(arg_list[1]) - 1]
            print(theWitch.skills)
            if theWitch.skillsFlag is False:

                if skills.witch_save in theWitch.skills:

                    if target.survivalStatus == 1 and target.number is theWitch.number and daysCount > 1:
                        textChannel = client.get_channel(textRooms[theWitch.number - 1])
                        await textChannel.send("你无法对自己使用解药")
                        return

                    if target.survivalStatus == 1:
                        target.survivalStatus = 2
                        theWitch.skills.remove(skills.witch_save)
                        textChannel = client.get_channel(textRooms[theWitch.number - 1])
                        await textChannel.send("你对玩家" + str(target.number) + "使用了解药")
                        theWitch.skillsFlag = True
                        print(theWitch.skills)
                    else:
                        return

                else:
                    textChannel = client.get_channel(textRooms[theWitch.number - 1])
                    await textChannel.send("你的解药已经没了")
            else:
                textChannel = client.get_channel(textRooms[theWitch.number - 1])
                await textChannel.send("本回合你已经用过毒药")

        if message.content.find("!poison") != -1 and stage is stage.女巫阶段:
            witchFlag = True
            msg = message.content
            arg_list = msg.split(" ")

            if len(arg_list) < 2:
                textChannel = client.get_channel(textRooms[theWitch.number - 1])
                await textChannel.send("请输入!poison playerNumber")
                return

            target = playersList[int(arg_list[1]) - 1]
            print(theWitch.skills)
            if theWitch.skillsFlag is False:

                if skills.witch_poison in theWitch.skills:

                    if target.survivalStatus == 1 or target.survivalStatus == 2:
                        target.survivalStatus = 0
                        theWitch.skills.remove(skills.witch_poison)
                        textChannel = client.get_channel(textRooms[theWitch.number - 1])
                        await textChannel.send("你对玩家" + str(target.number) + "使用了毒药")
                        print(theWitch.skills)
                        theWitch.skillsFlag = True
                    else:
                        return

                else:
                    textChannel = client.get_channel(textRooms[theWitch.number - 1])
                    await textChannel.send("你的毒药已经没了")
            else:
                textChannel = client.get_channel(textRooms[theWitch.number - 1])
                await textChannel.send("本回合你已经用过解药")

        if message.content.find("!boom") != -1 and stage is stage.day:
            print("自爆")
            dayflag = True
            await night()

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

        if stage is stage.prophet_check:
            dayflag = False
            t = 5
            msgsList = []
            for p in playersList:
                if p.identity is id.prophet:
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "预言家，你要查验谁? 请按照格式\n!check playerNumber 来进行输入和查验。\n例如: !check 1 代表你要查验1号玩家的身份。 请确保关闭输入法。",
                        tts=True, delete_after=32)
                    msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=32))
                else:
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "预言家正在进行查验",
                        tts=True, delete_after=32)
                    msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=32))

            while t > 0:
                # if (t % 10 == 0 and t > 10) or (t <= 5):
                time.sleep(1)
                t -= 1
                # await theMsg.edit(content="剩余时间: " + str(t))
                for eachMsg in msgsList:
                    await eachMsg.edit(content="剩余时间: " + str(t))
                    if (t == 0):
                        await eachMsg.delete()
                witchFlag = False
                stage = stage.女巫阶段




        if stage is stage.女巫阶段 and witchFlag is False:
            t = 30
            witchFlag = True

            msgsList = []
            dyingPlayer = -1
            for p in playersList:
                if p.survivalStatus == 1:
                    dyingPlayer = p.number
                if p.identity is id.witch:
                    theWitch = p
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "女巫请睁眼，昨晚玩家 "+ str(dyingPlayer) +" 死了，你有一瓶解药，要救吗？如果要救，请输入!save playerNumber" +
                        "\n你有一瓶毒药，要用吗？毒谁？ 如果要毒，请输入!poison playerNumber" +
                        "\n你只能做出一个选择",
                        tts=False, delete_after=32)
                    msgsList.append( await textChannel.send("剩余时间: " + str(t), delete_after=40) )
                else:
                    textChannel = client.get_channel(textRooms[p.number - 1])
                    await textChannel.send(
                        "女巫睁眼阶段",
                        tts=False, delete_after=32)
                    msgsList.append( await textChannel.send("剩余时间: " + str(t), delete_after=40) )

            while t > 0:
                time.sleep(1)
                t -= 1

                for eachMsg in msgsList:
                    await eachMsg.edit(content="剩余时间: " + str(t))
                    if(t == 0):
                        await eachMsg.delete()

            stage = stage.day


        if stage is stage.day:
            tt = 10

            for i in range(0, len(playersList)):
                to_channel = client.get_channel(919306850493677578)
                if playersList[i].survivalStatus == 2:
                    await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
                    await playersList[i].member.edit(mute=True)
            for j in range(0, requiredPlayerNum):
                announc_channal = client.get_channel(919369647109836830)
                msg = await announc_channal.send("剩余时间: " + str(tt))
                while tt > 0:
                    # if (t % 10 == 0 and t > 10) or (t <= 5):
                    await playersList[j].member.edit(mute=False)
                    time.sleep(1)
                    tt -= 1
                    if dayflag is True:
                        print("break")
                        break
                    await msg.edit(content="剩余时间: " + str(tt))
                    if tt == 1:
                        await playersList[j].member.edit(mute=True)
                stage = stage.voting
                await announc_channal.send("请开始投票")
                votingflag = False

        if stage is stage.voting and votingflag is False:
            votingflag = True
            tt = 10
            announc_channal = client.get_channel(919369647109836830)
            msg = await announc_channal.send("投票剩余时间: " + str(tt))
            while tt > 0:
                time.sleep(1)
                tt -= 1
                await msg.edit(content="投票剩余时间: " + str(tt))
            await countvote()
            stage = stage.wolf_vote
            # votingflag = False
            wolf_kill_flag = False

        if stage is stage.wolf_vote and wolf_kill_flag is False:
            wolf_kill_flag = True
            tt = 10
            announc_channal = client.get_channel(919369647109836830)
            msg = await announc_channal.send("刺杀剩余时间: " + str(tt))
            while tt > 0:
                time.sleep(1)
                tt -= 1
                await msg.edit(content="刺杀剩余时间: " + str(tt))
            await countkill()
            stage = stage.wolf_vote
            wolf_kill_flag = False

    if message.author.id in playersDict:
        if message.content.find("!day") != -1:
            await day()

        elif message.content.find("!night") != -1:
            await night()

        # if message.content.find("!reset_game") != -1:

    if message.content.find("!check") != -1 and stage is stage.prophet_check:
        print(66666666)
        msg = message.content
        arg_list = msg.split(" ")
        if len(arg_list) > 1:
            targetNum = int(arg_list[1])
            for player in playersList:
                if player.member == message.author:
                    if player.survivalStatus is True:  # and player.identity == id.prophet
                        await message.channel.send(
                            "Player " + str(targetNum) + "s identity is: " + str(playersList[targetNum - 1].identity))

    # if message.content.find("!boom") != -1 and stage is stage.day:
    # print("in boom 2.")
    # await night()

    if message.content.find("!hello") != -1:
        await message.channel.send("hi")

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

    if message.content.find("!vote") != -1 and stage is stage.voting:
        print("voting!!")
        msg = message.content
        arg_list = msg.split(" ")
        announc_channal = client.get_channel(919369647109836830)

        for player in playersList:
            target = playersList[int(arg_list[1]) - 1]
            if player.member == message.author:
                if player.survivalStatus is True and target.survivalStatus is True:
                    player.vote = target.number
                    await announc_channal.send("{}号 voted {}号".format(player.number, player.vote))

    if message.content.find("!kill") != -1 and (stage is stage.prophet_check or stage is stage.wolf_vote):
        msg = message.content
        arg_list = msg.split(" ")
        announc_channal = client.get_channel(919369647109836830)

        for player in playersList:
            target = playersList[int(arg_list[1]) - 1]
            if player.member == message.author:
                if player.survivalStatus is True and target.survivalStatus is True and player.identity is id.wolf:
                    player.vote = target.number
                    await announc_channal.send("{}号 wanna kill {}号".format(player.number, player.vote))

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
