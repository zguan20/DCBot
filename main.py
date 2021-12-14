import os
import discord
import random
import time
import enum

import main

client = discord.Client()

号数表 = ["一", "二", "三", "四", "五", "六", "七", "八", "九"]


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
        playersList[eliminator-1].survivalStatus = 1
        playersList[eliminator - 1].survivalStatus = 0



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

def getSurvivals():
    l = []
    for p in playersList:
        if p.survivalStatus == 2:
            l.append(p.number)
    return l

print(geneOrder())


class winner(enum.Enum):
    无 = 1
    狼人 = 2
    好人 = 3


class id(enum.Enum):
    wolf = 1
    civilian = 2
    prophet = 3
    witch = 4
    hunter = 5

class skills(enum.Enum):
    prophet_check = 1
    wolf_kill = 2
    witch_poison = 3
    witch_save = 4
    hunter_shoot = 7
    wolf_boom = 8
    none = 9

class stage(enum.Enum):
    prophet_check = 1
    wolf_kill = 2
    女巫阶段 = 3
    公布昨晚 = 4
    day = 5 #发言阶段
    公投阶段 = 6
    hunter_shoot = 7
    wolf_boom = 8
    none = 9

idToChannels = {"groupChannel" : 919306850493677578,
                id.wolf : 919306750929305630}


rooms = [919017619779096576, 919305506730954782, 919306040938487808,
         919306205212586065, 919306317376667650, 919306397118791690,
         919306467167858799, 919306605894455327, 919306683363229736]

textRooms = [919351644074946560, 919351790447755274, 919351880612741120,
             919351993980563477, 919352093469450250, 919363312007921724,
             919363378009497730, 919363475120222281, 919363753491980308,
             919369647109836830]

membersDict = {}



class Player:
    def __init__(self, member, number):
        self.number = number
        self.member = member
        self.identity = None
        self.survivalStatus = 2 #0真死 1还能救 2存活
        self.skills = []
        self.skillsFlag = False
        self.vote = -1
        self.out = False

playersDict = {
    "女巫" : Player(None, 2),
    "预言家" : Player(None, -1),
    "猎人": Player(None, 3),
    "狼人1": Player(None, 1),
    "狼人2": Player(None, -1),
    "狼人3": Player(None, -1)
}


daysCount = 1
stage = stage.none
requiredPlayerNum = 3
playersList = []
readyCount = 0
gameInProgress = False

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
    global stage
    global daysCount

    daysCount+=1

    stage = stage.prophet_check
    for i in range(0, len(playersList)):

        #move players to their rooms
        if playersList[i].identity == id.wolf:
            to_channel = client.get_channel(919306750929305630)
        else:
            to_channel = client.get_channel(rooms[i])
        if(playersList[i].survivalStatus == 2):
            await playersList[i].member.move_to(to_channel)  # move survival players to their corresponding channel
            await playersList[i].member.edit(mute=False)

async def day():
    global stage
    stage = stage.day
    for i in range(0, len(playersList)):
        to_channel = client.get_channel(919306850493677578)
        await playersList[i].member.move_to(to_channel)  # move all players to group channel
        await playersList[i].member.edit(mute=True)

#identityList = [id.wolf, id.wolf, id.wolf, id.civilian, id.civilian, id.civilian, id.prophet, id.witch, id.hunter]
identityList = [id.wolf, id.witch, id.hunter, id.wolf , id.wolf, id.civilian, id.civilian, id.civilian, id.prophet]

async def startGame():

    global rooms
    #random.shuffle(identityList)
    #random.shuffle(identityList)
    # random.shuffle(rooms)
    # random.shuffle(rooms)

    civilianCounter = 1
    wolfCounter = 1
    for i in range(0, len(playersList)):
        playersList[i].identity = identityList[i] #identityList[i] #assign id to player
        #playersList[1].survivalStatus = 1
        #playersList[i].skills = [skills.witch_save, skills.witch_poison]
        cur_member = playersList[i].member
        print(cur_member.name)
        # print(playersList[i].number)

        ind_n = playersList[i].number - 1
        role = discord.utils.get(cur_member.guild.roles, name=号数表[ind_n] + "号")
        await cur_member.add_roles(role)
        await playersList[i].member.edit(nick=str(playersList[i].number) + "号")

        to_channel = client.get_channel(rooms[i])

        if playersList[i].identity == id.wolf:
            to_channel = client.get_channel(919306750929305630)

        if playersList[i].identity == id.wolf:
            playersList[i].skills = [skills.wolf_kill]
            main.playersDict["狼人" + str(wolfCounter)] = playersList[i]
            wolfCounter += 1

        elif playersList[i].identity == id.prophet:
            playersList[i].skills = [skills.prophet_check]
            main.playersDict["预言家"] = playersList[i]

        elif playersList[i].identity == id.witch:
            playersList[i].skills = [skills.witch_save, skills.witch_poison]
            main.playersDict["女巫"] = playersList[i]

        elif playersList[i].identity == id.hunter:
            playersList[i].skills = [skills.hunter_shoot]
            main.playersDict["猎人"] = playersList[i]

        else:
            playersList[i].skills = [skills.none]
            main.playersDict["平民"+str(civilianCounter)] = playersList[i]
            civilianCounter += 1


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


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    theServer = client.get_guild(serverID)
    global sendToDict
    global gameInProgress
    global readyCount
    global playersList
    global membersDict
    global requiredPlayerNum
    global stage
    global dayflag
    global daysCount
    global stageLock
    global laststage
    global num_hero
    global num_civilian
    global num_wolf
    playersDict = main.playersDict
    dayflag = False
    authorID = message.author.id
    member = await theServer.fetch_member(authorID)

    announc_channal = client.get_channel(919369647109836830)

    if message.content.find("!day") != -1:
        stage = stage.day

    if readyCount <= requiredPlayerNum:

        if message.content.find("!ready") != -1:
            isReady = False
            for count, theMember in membersDict.items():
                if authorID == theMember.id:
                    isReady = True
                    break


            if(isReady is False):
                readyCount += 1
                membersDict[readyCount] = member

            await message.channel.send(
                str(member) + " is ready. Need " + str(requiredPlayerNum - readyCount) + " more players to start")



        if message.content.find("!boom") != -1 and stage is stage.day:
            print("自爆")
            dayflag = True
            await night()

        if message.content.find("!kill") != -1 and stage is stage.wolf_kill:

            msg = message.content
            arg_list = msg.split(" ")

            w1 = playersDict["狼人1"]
            w2 = playersDict["狼人2"]
            w3 = playersDict["狼人3"]
            t1 = client.get_channel(textRooms[w1.number - 1])
            t2 = client.get_channel(textRooms[w2.number - 1])
            t3 = client.get_channel(textRooms[w3.number - 1])

            if len(arg_list) < 2:
                await t1.send("请输入!kill playerNumber")
                return

            if(authorID == w1.member.id):
                w1.vote = playersList[int(arg_list[1]) - 1].number
                await t1.send("{}号狼人 voted {}号".format(w1.number, w1.vote))

            #if(authorID == w2.member.id):
                #w2.vote = playersList[int(arg_list[1]) - 1]

            #if (authorID == w3.member.id):
                #w3.vote = playersList[int(arg_list[1]) - 1]

            #await t1.send("{}号狼人 voted {}号".format(player.number, player.vote))
            #await t2.send("{}号狼人 voted {}号".format(player.number, player.vote))
            #await t3.send("{}号狼人 voted {}号".format(player.number, player.vote))


        if message.content.find("!shoot") != -1 and stage is stage.公布昨晚 and playersDict["猎人"].survivalStatus == 1 and authorID == playersDict["猎人"].member.id:

            msg = message.content
            arg_list = msg.split(" ")
            textChannel = client.get_channel(textRooms[playersDict["猎人"].number - 1])
            announc_channal = client.get_channel(919369647109836830)

            if len(arg_list) < 2:
                await textChannel.send("请输入!shoot playerNumber")
                return

            if skills.hunter_shoot in playersDict["猎人"].skills:
                target = playersList[int(arg_list[1]) - 1]
                if target.out is False:
                    target.out = True
                    target.survivalStatus = 0
                    await textChannel.send("你用射杀带走了玩家 " + str(target.number))
                    await announc_channal.send("玩家 " + str(playersDict["猎人"].number) + " 用射杀带走了玩家 " + str(target.number))
                    playersDict["猎人"].skills.remove(skills.hunter_shoot)

                else:
                    await textChannel.send("玩家" + str(target.number) + "已经是出局玩家，请重试")

                playersDict["猎人"].skillsFlag = True
            else:
                await textChannel.send("你无法发动技能！")
                return

        if message.content.find("!save") != -1 and stage is stage.女巫阶段 and playersDict["女巫"].out is False:
            msg = message.content
            arg_list = msg.split(" ")
            textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])

            if len(arg_list) < 2:
                textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                await textChannel.send("请输入!save playerNumber")
                return

            target = playersList[int(arg_list[1]) - 1]
            print(playersDict["女巫"].skills)
            if playersDict["女巫"].skillsFlag is False:

                if skills.witch_save in playersDict["女巫"].skills:


                    if target.number == playersDict["女巫"].number and daysCount > 1:

                        await textChannel.send("你无法对自己使用解药")
                        return

                    if target.out is False:
                        target.survivalStatus = 2
                        playersDict["女巫"].skills.remove(skills.witch_save)
                        textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                        await textChannel.send("你对玩家" + str(target.number) + "使用了解药")
                        playersDict["女巫"].skillsFlag = True
                        print(playersDict["女巫"].skills)
                    else:
                        await textChannel.send("玩家" + str(target.number) + "已经是出局玩家，请重试")
                        return

                else:
                    textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                    await textChannel.send("你的解药已经没了")
            else:
                textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                await textChannel.send("本回合你已经用过毒药")

        if message.content.find("!poison") != -1 and stage is stage.女巫阶段 and playersDict["女巫"].out is False:
            msg = message.content
            arg_list = msg.split(" ")

            if len(arg_list) < 2:
                textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                await textChannel.send("请输入!poison playerNumber")
                return

            target = playersList[int(arg_list[1]) - 1]
            print(playersDict["女巫"].skills)
            if playersDict["女巫"].skillsFlag is False:

                if skills.witch_poison in playersDict["女巫"].skills:

                    if target.out is False:
                        target.survivalStatus = 0
                        playersDict["女巫"].skills.remove(skills.witch_poison)
                        textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                        await textChannel.send("你对玩家" + str(target.number) + "使用了毒药")
                        print(playersDict["女巫"].skills)
                        playersDict["女巫"].skillsFlag = True

                        if target.identity == id.hunter:
                            target.skills = [skills.none]

                    else:
                        await textChannel.send("玩家" + str(target.number) + "已经是出局玩家，请重试")
                        return

                else:
                    textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                    await textChannel.send("你的毒药已经没了")
            else:
                textChannel = client.get_channel(textRooms[playersDict["女巫"].number - 1])
                await textChannel.send("本回合你已经用过解药")

        # if message.content.find("!no") != -1 and stage is stage.女巫阶段:
        #     for p in playersList:
        #         if p.survivalStatus == 1:
        #             p.survivalStatus = 0

        if message.content.find("!unready") != -1:

            for count, theMember in membersDict.items():
                if authorID == theMember.id:
                    membersDict.pop(count)
                    readyCount -= 1
                    await message.channel.send(
                        str(member) + " is unready. Need " + str(
                            requiredPlayerNum - readyCount) + " more players to start")
                    break




        if message.content.find("!start") != -1 and readyCount >= requiredPlayerNum:
            gameInProgress = True
            num_hero = 1
            num_civilian = 3
            num_wolf = 1

            for key in membersDict.keys():
                playersList.append(Player(membersDict[key], key))
            await message.channel.send("Game started")
            await startGame()
            announc_channal = client.get_channel(919369647109836830)
            await announc_channal.send("开始游戏: 存活玩家 {}".format(getSurvivals()))
            stage = stage.prophet_check
            stageLock = False

            while stageLock is not True:
                if stage is stage.prophet_check and stageLock is False:
                    await night()
                    stageLock = True
                    dayflag = False
                    playersDict["女巫"].skillsFlag = False
                    t = 5
                    msgsList = []
                    for p in playersList:
                        if p.identity is id.prophet:
                            textChannel = client.get_channel(textRooms[p.number - 1])
                            await textChannel.send(
                                "预言家，你要查验谁? 请按照格式\n!check playerNumber 来进行输入和查验。\n例如: !check 1 代表你要查验1号玩家的身份。 请确保关闭输入法。",
                                tts=False, delete_after=(t+10))
                            await textChannel.send("预言家查验阶段 存活玩家: {}".format(getSurvivals()), delete_after=(t+10))
                            msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))
                        else:
                            textChannel = client.get_channel(textRooms[p.number - 1])
                            await textChannel.send(
                                "预言家正在进行查验",
                                tts=False, delete_after=(t+10))
                            msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))

                    await announc_channal.send(
                        "预言家正在进行查验",
                        tts=False, delete_after=(t + 10))
                    msgsList.append(await announc_channal.send("剩余时间: " + str(t), delete_after=(t + 10)))

                    while t > 0:
                        # if (t % 10 == 0 and t > 10) or (t <= 5):
                        time.sleep(1)
                        t -= 1
                        # await theMsg.edit(content="剩余时间: " + str(t))
                        for eachMsg in msgsList:
                            await eachMsg.edit(content="剩余时间: " + str(t))
                            # if (t == 0):
                            #     await eachMsg.delete()
                    stage = stage.wolf_kill
                    stageLock = False

                if stage is stage.wolf_kill and stageLock is False:
                    stageLock = True
                    t = 10

                    msgsList = []
                    await announc_channal.send("狼人杀人阶段 存活玩家: {}".format(getSurvivals()), delete_after=(t + 10))
                    await announc_channal.send(
                        "狼人在杀人...",
                        tts=False, delete_after=(t + 10))
                    msgsList.append(await announc_channal.send("剩余时间: " + str(t), delete_after=(t + 10)))


                    for p in playersList:
                        if p.identity is id.wolf:
                            textChannel = client.get_channel(textRooms[p.number - 1])
                            await textChannel.send(
                                "狼人请杀人 输入指令!kill playerNumber",
                                tts=False, delete_after=(t+10))
                            await textChannel.send("狼人杀人阶段 存活玩家: {}".format(getSurvivals()), delete_after=(t+10))
                            msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))
                        else:
                            textChannel = client.get_channel(textRooms[p.number - 1])
                            await textChannel.send(
                                "狼人在杀人...",
                                tts=False, delete_after=(t+10))
                            msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))

                    while t > 0:
                        # if (t % 10 == 0 and t > 10) or (t <= 5):
                        time.sleep(1)
                        t -= 1
                        # await theMsg.edit(content="剩余时间: " + str(t))
                        for eachMsg in msgsList:
                            await eachMsg.edit(content="剩余时间: " + str(t))

                    w1 = playersDict["狼人1"]
                    # w2 = playersDict["狼人2"]
                    # w3 = playersDict["狼人3"]
                    t1 = client.get_channel(textRooms[w1.number - 1])
                    # t2 = client.get_channel(textRooms[w2.number - 1])
                    # t3 = client.get_channel(textRooms[w3.number - 1])

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

                    eliminator = 1
                    flatVoteList = []
                    for player in playersList:
                        if player.out is False and player.identity == id.wolf and player.vote != -1:
                            votes[player.vote].append(player.number)

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
                        await t1.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
                        # await t2.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
                        # await t3.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
                    else:
                        await t1.send(str(eliminator) + " 号玩家已被刺杀")
                        # await t2.send(str(eliminator) + " 号玩家已被刺杀")
                        # await t3.send(str(eliminator) + " 号玩家已被刺杀")
                        playersList[eliminator - 1].survivalStatus = 1

                    print(eliminator)

                    stage = stage.女巫阶段
                    #stage = stage.prophet_check
                    stageLock = False

                    if stage is stage.女巫阶段 and stageLock is False:
                        stageLock = True
                        t = 10
                        await announc_channal.send("女巫阶段 存活玩家: {}".format(getSurvivals()), delete_after=(t+10))

                        msgsList = []
                        dyingPlayer = -100
                        for p in playersList:
                            if p.survivalStatus == 1:
                                dyingPlayer = p.number

                        for p in playersList:
                            if p.identity is id.witch:
                                # playersDict["女巫"] = p
                                textChannel = client.get_channel(textRooms[p.number - 1])
                                await textChannel.send(
                                    "女巫请睁眼，昨晚玩家" + str(dyingPlayer) + "死了，你有一瓶解药，要救吗？如果要救，请输入!save playerNumber" +
                                    "\n你有一瓶毒药，要用吗？毒谁？ 如果要毒，请输入!poison playerNumber" +
                                    "\n你只能做出一个选择",
                                    tts=False, delete_after=(t+10))
                                await textChannel.send("存活玩家: {}".format(getSurvivals()))
                                msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))
                            else:
                                textChannel = client.get_channel(textRooms[p.number - 1])
                                await textChannel.send(
                                    "女巫睁眼阶段",
                                    tts=False, delete_after=(t+10))
                                msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t+10)))

                        while t > 0:
                            time.sleep(1)
                            t -= 1

                            for eachMsg in msgsList:
                                await eachMsg.edit(content="剩余时间: " + str(t))
                                # if (t == 0):
                                #     await eachMsg.delete()
                        laststage = stage.女巫阶段
                        stage = stage.公布昨晚
                        stageLock = False

                    if stage is stage.公布昨晚 and stageLock is False:
                        stageLock = True


                        # 确认死亡玩家
                        deadList = []
                        for p in playersList:
                            if p.survivalStatus == 1 or (p.survivalStatus == 0 and p.out is False):
                                if p.identity == id.wolf:
                                    num_wolf -= 1
                                if p.identity == id.hunter or p.identity == id.witch or p.identity == id.prophet:
                                    num_hero -= 1
                                if p.identity == id.civilian:
                                    num_civilian -= 1

                                print("人数：   -   -  -")
                                print(num_wolf)
                                print(num_hero)
                                print(num_civilian)

                                ind_n = p.number - 1
                                role = discord.utils.get(p.member.guild.roles, name="凉凉")
                                await p.member.add_roles(role)
                                await p.member.edit(nick="凉凉" + 号数表[ind_n] + "号")

                                deadList.append(p.number)

                        announc_channal = client.get_channel(919369647109836830)

                        # 检测是否有能发动技能的身份 此时survivalStatus依然是1
                        for d in deadList:
                            if playersList[d - 1].identity == id.hunter:
                                textChannel = client.get_channel(textRooms[d - 1])
                                await textChannel.send("玩家 " + str(d) + " 是否发动技能? 请选择射杀对象 !shoot playerNumber")
                                await textChannel.send("存活玩家: {}".format(getSurvivals()))

                        t = 5
                        editMsg = await announc_channal.send("等待玩家发动技能阶段... 剩余时间:" + str(t))
                        while t > 0:
                            time.sleep(1)
                            t -= 1
                            await editMsg.edit(content="等待玩家发动技能阶段... - 剩余时间:" + str(t))

                        # 发表遗言阶段
                        # if(daysCount == 1):

                        # 确认出局
                        for d in deadList:
                            playersList[d - 1].survivalStatus = 0
                            playersList[d - 1].out = True


                        winners = winner.无
                        if num_civilian == 0 or num_hero == 0 or (num_hero + num_civilian) == num_wolf:
                            # 狼人获胜
                            await announc_channal.send("游戏结束 狼人获胜!")
                            winners = winner.狼人
                        elif num_wolf == 0:
                            # 好人获胜
                            await announc_channal.send("游戏结束 好人阵营获胜!")
                            winners = winner.好人

                        if winners != winner.无:
                            for p in playersList:
                                ind_n = p.number - 1
                                role = discord.utils.get(p.member.guild.roles, name=号数表[ind_n] + "号")
                                await p.member.remove_roles(role)
                                role = discord.utils.get(p.member.guild.roles, name="凉凉")
                                await p.member.remove_roles(role)
                                await p.member.edit(nick=None)

                            for i in range(0, len(playersList)):
                                to_channel = client.get_channel(919306850493677578)
                                await playersList[i].member.move_to(to_channel)  # move all players to group channel
                                await playersList[i].member.edit(mute=False)

                            await announc_channal.send("你们可以开始复盘了!")

                            break

                        if laststage is stage.女巫阶段:
                            await announc_channal.send("公布昨晚的结果")
                            await announc_channal.send("第 " + str(daysCount) + " 天  存活玩家: {}".format(getSurvivals()))
                            if (len(deadList) > 0):
                                await announc_channal.send("昨晚这些玩家死亡 {}".format(deadList))
                            else:
                                await announc_channal.send("昨晚是平安夜")
                            stage = stage.day  # 正式发言阶段


                        if laststage is stage.公投阶段:
                            stage = stage.prophet_check
                        stageLock = False

                        deadList.clear()

                    if stage is stage.day and stageLock is False:
                        stageLock = True

                        announc_channal = client.get_channel(919369647109836830)
                        await announc_channal.send("存活玩家 {}".format(getSurvivals()))

                        for i in range(0, len(playersList)):
                            to_channel = client.get_channel(919306850493677578)
                            await playersList[i].member.move_to(to_channel)  # move to the corresponding channel
                            await playersList[i].member.edit(mute=True)


                        for p in playersList:
                            if p.out is False:
                                tt = 5
                                editMsg = await announc_channal.send(str(p.number) + "号玩家正式发言阶段 剩余时间:" + str(tt))
                                while tt > 0:
                                    # if (t % 10 == 0 and t > 10) or (t <= 5):
                                    await p.member.edit(mute=False)
                                    time.sleep(1)
                                    tt -= 1
                                    await editMsg.edit(content=str(p.number) + "号玩家正式发言阶段 剩余时间:" + str(tt))
                                    if dayflag is True:
                                        print("break")
                                        break
                                    print(tt)
                                    if tt == 0:
                                        print("tt ==== 1")
                                        await p.member.edit(mute=True)

                        stageLock = False
                        stage = stage.公投阶段



                    if stage is stage.公投阶段 and stageLock is False:
                        stageLock = True
                        await announc_channal.send("公投阶段")
                        msgsList = []
                        t = 20
                        for p in playersList:
                            textChannel = client.get_channel(textRooms[p.number - 1])
                            await textChannel.send(
                                "请投票 输入指令!vote playerNumber",
                                tts=False, delete_after=(t + 10))
                            await textChannel.send("存活玩家: {}".format(getSurvivals()), delete_after=(t + 10))
                            msgsList.append(await textChannel.send("剩余时间: " + str(t), delete_after=(t + 10)))
                        while t > 0:
                            # if (t % 10 == 0 and t > 10) or (t <= 5):
                            time.sleep(1)
                            t -= 1
                            # await theMsg.edit(content="剩余时间: " + str(t))
                            for eachMsg in msgsList:
                                await eachMsg.edit(content="剩余时间: " + str(t))

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
                            if player.out is False and player.vote != -1:
                                votes[player.vote].append(player.number)

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
                            await announc_channal.send("无人放逐")
                            # await t2.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
                            # await t3.send("这些玩家得到了同样票数: " + "{}".format(flatVoteList))
                        else:
                            await announc_channal.send(str(eliminator) + " 号玩家已被放逐")
                            # await t2.send(str(eliminator) + " 号玩家已被刺杀")
                            # await t3.send(str(eliminator) + " 号玩家已被刺杀")
                            playersList[eliminator - 1].survivalStatus = 1

                        laststage = stage.公投阶段
                        stage = stage.公布昨晚
                        stageLock = False



    if message.content.find("!check") != -1 and stage is stage.prophet_check:
        print(66666666)
        msg = message.content
        arg_list = msg.split(" ")
        if len(arg_list) > 1:
            targetNum = int(arg_list[1])
            for player in playersList:
                if player.member == message.author:
                    if player.survivalStatus == 2:  # and player.identity == id.prophet
                        await message.channel.send(
                            "Player " + str(targetNum) + "s identity is: " + str(playersList[targetNum - 1].identity))



    #if message.content.find("!boom") != -1 and stage is stage.day:
        #print("in boom 2.")
        #await night()

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

    if message.content.find("!vote") != -1 and stage is stage.公投阶段:
        msg = message.content
        arg_list = msg.split(" ")
        announc_channal = client.get_channel(919369647109836830)

        for player in playersList:
            target = playersList[int(arg_list[1]) - 1]
            if player.member == message.author:
                if player.survivalStatus == 2 and target.survivalStatus == 2:
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
            playersList[i].survivalStatus = 0
            await playersList[i].member.edit(mute=True)
            cur_member = playersList[i].member

            ind_n = playersList[i].number - 1
            role = discord.utils.get(cur_member.guild.roles, name=号数表[ind_n] + "号")
            await playersList[i].remove_roles(role)

            role = discord.utils.get(cur_member.guild.roles, name="凉凉")
            await member.add_roles(role)
            await playersList[i].member.edit(nick=cur_member.name)

    # if message.content.find("!reset name") != -1:
    #     for p in playersList:
    #         await playersList[i].member.edit(nick=cur_member.name)


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