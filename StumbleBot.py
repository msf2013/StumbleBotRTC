# -*- coding: utf-8 -*-
import json
import requests
import random
from websocket import create_connection
import time
import threading
from threading import Thread

#import config

import socket


#===========================================
#================  URLS  ===================
#===========================================

tokenUrl = "https://stumblechat.com/api/room/token/thevoid"
profileurl = 'https://stumblechat.com/api/profile/thevoid'


#===========================================
#========  STUMBLECHAT SETTINGS  ===========
#===========================================

botsname = 'botsname'
username = 'username'
password = 'password'
room = 'roomname'
webserver = "wss://wss32.stumblechat.com/"
prefix = ['@', '!']
botadmins = ['1057372']
botonline = False
kob = False
roomcount = 0
VIP = False
VIPCAM = False

checkvip = False
checkcamvip = False
#===========================================
#=============  User Rights ================
#===========================================

Level0 = [] #Guest
Level1 = [] #Everyone
Level2 = [] #Operator
Level3 = [] #CoOwner
Level4 = [] #Admin



#===========================================
#=============  Databases  =================
#===========================================

chatlogs = '/Logs/' + room + '/Logs.db'
youtubelogs = '/Logs/' + room + '/Youtubelogs.db'
youtubeload = []

#loadlists
knownuserslist = '/Database/KnownUsers.db'
knownusers = []
cambanslist = '/Database/CamBans.db'
cambans = []
banlistlist = '/Database/Banlist.db'
banlist = []
operatorslist = '/Database/Operators.db'
operators = []
youtubelistlist = '/Database/Youtube.db'
youtubelist = []
scorelist = '/Database/Scores.db'
scores = []
loadadminslist = '/Database/Adminlist.db'
loadadmins = []
bannickslist = '/Database/BannedNicks.db'
bannicks = []
banwordslist = '/Database/BanWords.db'
banwords = []



#===========================================
#============ YOUTUBE SETTINGS =============
#===========================================

logyoutube = False
publicyoutube = False

#===========================================
#============ IRC Settings =================
#===========================================

ircserver = ""
ircport = ""
ircaccount = ""
ircbotname = ""
ircsocket = socket.socket()
ircusers = []
ircoperators = []

#===========================================
#============= Twitch Settings =============
#===========================================


#import socket

twitchserver = 'irc.chat.twitch.tv'
twitchport = 6667
twitchnickname = 'twitchbotname'
twitchtoken = 'oauth:yourauth'
twitchsocket = socket.socket()
twitchusers = []
twitchoperators = []

#===========================================
#============= YouNow Settings =============
#===========================================

bitcoinbot = False
triviaresults = ""
triviaWrong = []
debugging = True
logging = True
usertoken = ""
annoucement = False
tokesstarted = False
tokes = 0
triviastarted = False
greet = True
#room data
pingcount = 0

userlist = []

connected = False
ws = create_connection(webserver)
twitchsocket = socket.socket()

startTime = time.time()

def LoadKnownUsers():
    txt_file = open(knownuserslist, "r")
    users = txt_file.readlines().split('\n')
    knownusers = users
    return
def HandleUptime():
    uptime = time.time() - startTime
    seconds = uptime.split('.')
    SendPublicMessage(str(seconds[0]))
def ConnectToTwitch(twitchchannel):
    
    print('Connecting to %s on Twitch!' % twitchchannel)
    twitchsocket.connect((twitchserver, twitchport))
    twitchsocket.send(f"PASS {twitchtoken}\n".encode('utf-8'))
    twitchsocket.send(f"NICK {twitchnickname}\n".encode('utf-8'))
    twitchsocket.send(f"JOIN {twitchchannel}\n".encode('utf-8'))

    while True:
        resp = twitchsocket.recv(2048).decode('utf-8')
        SendPublicMessage('Connected to %s!' % twitchchannel)
        print(resp)
        if resp/startswith('PING :tmi.twitch.tv'):
            twitchsocket.send(b'PONG :tmi.twitch.tv')
        if resp.startswith('@quit'):
            break
    twitchsocket.close()
def HandleMessage(message):

    print("Message: %s" % message)

    j = json.loads(message)
    pass
def SendPublicMessage(message):
    
    ws.send(json.dumps({"cc": "msg","text": message}))

def SendPrivateMessage(handle, message):
    ws.send(json.dumps({"cc": "pvtmsg","handle": handle, "text": message}))

def SendPublicEmoji(message):
    emoji = message + ' ~~🔥~~'
    ws.send(json.dumps({"cc": "msg","text": emoji}))

def HandleRoll():
    choices = ['1', '2', '3', '4', '5', '6']
    rollu = random.choice(choices)
    rollb = random.choice(choices)
    if rollu < rollb:
        SendPublicMessage('You rolled: %s\nBot rolled:%s\nYou Lose!' % (rollu, rollb))
    elif rollu == rollb:
        SendPublicMessage('You rolled: %s\nBot rolled:%s\nRoll was a draw!' % (rollu, rollb))
    else:     
        SendPublicMessage('🔥 You rolled: %s\nBot rolled:%s\nYou win! 🔥' % (rollu, rollb))
def HandleFlip():
    choices = ['Heads', 'Tails']
    flip = random.choice(choices)
    SendPublicMessage('You flipped: %s!' % flip)
def HandleJoke():

    url = "https://v2.jokeapi.dev/joke/Pun?type=single"
    req = requests.get(url).text
    data = json.loads(req)
    #print(data)
    question = data['joke']
    
    SendPublicMessage("Joke: %s" % question)
def HandleTrivia():
    url = "https://beta-trivia.bongo.best/?search=cat&type=multiple&difficulty=easy&limit=1"
    req = requests.get(url).text
    data = json.loads(req)
    question = data[0]['question']
    answer = data[0]['correct_answer']
    print("Question: " + question)
    SendPublicMessage(question)
    print("Answer: " + answer)
    time.sleep(20)
    
    SendPublicMessage("Answer: " + answer)
def HandleTokeTimer():
    running = tokesstarted
    if not running:

        SendPublicMessage("Tokes in 60 seconds!")
        time.sleep(60)
        
        SendPublicMessage("🔥 Tokes started! 🔥")
def HandleBitcoinLoop():

    if bitcoinbot != True:

        while(1):

            url = "https://api.cryptowat.ch/markets/kraken/btcusd/price"
            req = requests.get(url).text
            data = json.loads(req)
            results = data['result']['price']
            SendPublicMessage("🔥 [HOURLY BITCOIN]\n CryptoWatch says: %s 🔥" % results)
            time.sleep(60*60)
def HandleBitcoins():

    url = "https://api.cryptowat.ch/markets/kraken/btcusd/price"
    req = requests.get(url).text
    data = json.loads(req)
    results = data['result']['price']
    SendPublicMessage("CryptoWatch says: %s" % results)
    #write date|time|price
def HandleLiteoins():

    url = "https://api.cryptowat.ch/markets/kraken/ltcusd/price"
    out = requests.get(url).text
    resp_dict = json.loads(out)
    results = resp_dict['result']['price']
    SendPublicMessage("CrytpoWatch says: %s" % results)
def HandleChuckNorris(): # YEA RIGHT! ~roundhouse

    url = "https://api.chucknorris.io/jokes/random"
    out = requests.get(url).text
    resp_dict = json.loads(out)
    results = resp_dict['value']
    SendPublicMessage("%s." % results)  
def HandleMom(): #MAYBE!

    url = "https://api.yomomma.info/"

    out = requests.get(url).text

    resp_dict = json.loads(out)
    results = resp_dict['joke']
    SendPublicMessage(results)
def HandleOneLiner():

    url = "http://getpickuplines.herokuapp.com/lines/random"

    out = requests.get(url).text

    resp_dict = json.loads(out)
    results = resp_dict['line']
    SendPublicMessage(results)
def HandleFortune():

    
    answers = [ 
    'Pass Go, Collect [̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅] [̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅] !',
    'When in anger, sing the alphabet.','About time i got out of that cookie.', 'Avoid taking unnecessary gambles. Lucky numbers 2,12,10,15,6,5.', 'Ask your mom.',
    'I cannot help you, I am just a cookie.', 'Ignore previous fortune cookies.', 'Ignore future fortune cookies.', 'The fortune you seek is in another cookie.',
    'Some fortune cookies contain no fortune.', 'Always think something can go wrong, then you will always be right.', 'Found the mistake in the code..', 'Ask again later',
    'If Hakuna Matata dont work, then no worries', 'Maybe whoever has this will feel better? ~Matt~', 'Tell x0r hes pretty, might save his life some day.']
    SendPublicMessage(random.choice(answers))
def YoutubeAdd(videoid):   
    data = {
            "cc": "youtube",
            "type": "add",
            "id": videoid,
            "time": 1}
    ws.send(json.dumps(data))
    SendPublicMessage('%s added!' % videoid)
def CheckMessage(username, msg):
    
    #if not knownuser, kick/ban user
    if badwords in msg:
        pass

        if kob == False: # False to kick, True to ban
            ws.send(json.dumps({"cc": "kick","user": username}))
        else:
            ws.send(json.dumps({"cc": "ban","user": username}))
def HandleMood():

    moods = ['Happier than Gallagher at a Farmer\'s market.',
    'Happier than a Bodybuilder Directing Traffic.',
    'Happier than Christopher Columbus with Speedboats',
    'Happier than Eddie Money running a travel agency.',
    'Happier than a Witch at a Broom Factory',
    'Happier than a Slinky on an Escalator.',
    'Happier than an Antelope with Nightvision Goggles.',
    'Happier than Dikembe Mutombo Blocking a Shot.',
    'Happier than Paul Revere with a Cell phone.',
    'Happier than Dracula Volunteering at a Blood Drive.',
    'Happier than the Pillsbury Doughboy on his way to a Baking Convention.',
    'Happier than a Camel on Wednesday/Hump Day.']

    SendPublicMessage(random.choice(moods))
def HandleAnimal():
    
    facts = ['the peacock mantis shrimp can throw a punch at 50 mph, accelerating quicker than a 22 caliber bullet.',
             'studies have shown that wild chimps in guinea drink fermented palm sap, which contains about 3 percent alcohol by volume.',
             'the chevrotain is an animal that looks like a tiny deer with fangs. ',
             'capuchin monkeys pee on their hands to wash their feet.',
             'only the males are called peacocks. females are called peahens.',
             'dragonflies and damselflies form a heart with their tails when they mate.',
             'baby elephants suck their trunks for comfort.',
             'tigers have striped skin as well. each pattern is as unique as a fingerprint.',
             'there was once a type of crocodile that could gallop.',
             'sea otters hold hands while they\'re sleeping so they don\'t drift apart.',
             'prairie dogs say hello by kissing.',
             'animal behaviorists have concluded that cats dont meow as a way to communicate with each other. its a method they use for getting attention from humans.',
             'despite their appearance, elephant shrews are more closely related to elephants than shrews.',
             'flamingos are naturally white—their diet of brine shrimp and algae turns them pink.',
             'alberta, canada is the largest rat-free populated area in the world.',
             'red-eyed tree frog eggs can hatch early if they sense danger.',
             'whitetail deer can sprint at speeds up to 30 miles per hour.',
             'blue jays mimic hawks calls to scare away other birds',
             'in the uk, the british monarch legally owns all unmarked mute swans in open water.',
             'all clownfish are born male—some turn female to enable mating.',
             'moray eels have a second set of jaws that extends from their throats.',
             'male ring-tailed lemurs will \"stink fight\" by wafting scent at each other.']
    SendPublicMessage(random.choice(facts))
def Handle8Ball():
    
    
    answers = [
                '[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]',
                'It is certain',
                'It is decidedly so',
                'Without a doubt',
                'Yes definitely',
                'You may rely on it',
                'As I see it, yes',
                'Most likely',
                'Outlooks good',
                'Yes',
                'Signs point to yes',
                'Signs point to no',
                'Don\'t count on it', 
                'My reply is no',
                'My sources say no',
                'Outlook not so good',
                'Very doubtful',
                'Why do you need to ask?',
                'Negative', 'Indeed',
                'Sorry Boo', 
                'Doubt JSD cares.',
                'Don\'t go Full retarded',
                'Is Ed \"Too Tall\" Jones too tall?',
                'Does Charlie Daniels play a mean fiddle?',
                'Does Elmer Fudd have trouble with the letter R?',
                'Did The Waltons take way too long to say good night?',
                'Does a ten-pound bag of flour make a really big biscuit?',
                'Did the caveman invent fire?',
                'Was Abe Lincoln honest?',
                'Is having a snowball fight with pitching great Randy Johnson a bad idea?',
                'Is a bird in the hand worth two in the bush?',
                'Can fútbol announcer Andrés Cantor make any sport exciting?',
                'Does a former drill sergeant make a terrible therapist?',
                'Do woodchucks chuck wood?',
                'Did the little piggy really cry \"wee wee wee\"" all the way home?',
                'Does it take two to tango?',
                'What, do you live under a rock?',
                'Does the buck stop here?',
                'Do dogs chase cats?',
                'Would Foghorn Leghorn make a really bad book narrator?',
                'Is the pen mightier than the sword?',
                'Do people use smartphones to do dumb things?',
                'Would helium make opera sound less stuffy?',
                'Do mimes make even less sense when you can\'t see them?']


    SendPublicMessage(random.choice(answers))
def CheckCamBan(handle):
    create = open('cambans.db', 'a+')

    with open('cambans.db', 'r') as banlist:
        
        for users in banlist.read():
            if handle in users:
                SendPublicMessage('%s is in cambans.db' % handle)
                print("User in cam bans: %s!" % user)
                pass
                #SendCloseCam()
def Handle_Joined(data):

    #print('OnHandle: %s' % data)
    room_avatar = data['room']['avatar']
    room_biography = data['room']['biography']
    room_location = data['room']['location']
    room_name = data['room']['name']

    self_avatar = data['self']['avatar']
    self_chatcolor = data['self']['chatcolor']
    self_namecolor = data['self']['namecolor']
    self_handle = data['self']['handle']
    self_mod = data['self']['mod']
    print('Joined %s as %s' % (room, botsname))

def Handle_Ping():
    ws.send(json.dumps({"cc":"pong"}))
    if debugging: print("Pong!")
def Handle_YoutubePlay(data):

    handletype = data['type']
    if 'play' in handletype:

        title = data['title']
        videoid = data['id']
        queueid = data['queueid']
        vidtime = data['time']
        print('Playing %s!' %title)  
        
    else:

        if 'stop' in handletype:
            print('Youtube Stopped!')
def Handle_OnSys(data):

    text = data['text']
    print('[SYS MESSAGE] %s'  % text) 
def HandlePublicMessage(data):

    if data:
        handle = data['handle']
        text = data['text']
        cmd_arg = text.split(' ')

        if debugging: print('%i: %s' % (handle,text))

        if '@test' in text:
            SendPublicMessage("Pass!")
        #=================================
        #====== PUBLIC COMMANDS ==========
        #=================================
        
        if text.startswith('@bitcoinbot'):
            if not bitcoinbot:

                marketcheck = threading.Thread(target=HandleBitcoinLoop)
                marketcheck.start()
                bitcoinbot = True
                SendPublicMessage('Bitcoin started, updates hourly!')

        if text.startswith('@check'):
            HandleCheck()

        if text.startswith('@handle'):
            SendPublicMessage(str(handle))

        if text.startswith('@roll'):
            HandleRoll()
     
        if text.startswith('@btc'):
            HandleBitcoins()
     
        if text.startswith('@ltc'):
            HandleLitecoins()
     
        if text.startswith('@flip'):           
            HandleFlip()
            
        if text.startswith('@mood'):
            HandleMood()

        if text.startswith('@line'):
            HandleOneLiner()

        if text.startswith('@fact'):
            HandleAnimal()

        if text.startswith('@joke'):
            HandleJoke()

        if text.startswith('@cookie'):
            HandleFortune()

        if text.startswith('@mom'):
            HandleMom() #Giggity

        if text.startswith('@cn'):
            HandleChuckNorris()

        if text.startswith('@8ball'):
            question = text.split(' ')
            if len(text) == 6:
                SendPublicMessage('Must have a question!')
            else:
                Handle8Ball()

        if text.startswith('@trivia'):
            trivia = threading.Thread(target=HandleTrivia)
            trivia.start()
            triviastarted = True
        if text.startswith('@tokes'):
            toke = threading.Thread(target=HandleTokeTimer)
            toke.start()
            tokesstarted = True
            
        if text.startswith('@uptime'):
            HandleUptime()

        if text.startswith('@yt'):
            url = decode['text']
            msg = url.split(' ')
            vid = msg[1]
            
            YoutubeAdd(vid)

def HandlePrivateMessage(data):
    if data:
        handle = data['handle']
        text = data['text']
        cmd_arg = text.split(' ')

        print('[Private Message] %i: %s' % (handle, text))
        SendPrivateMessage(handle, text)

def HandleUserJoin(data):
    name = data['nick']
    mod = data['mod']
    handle = data['handle']

    if mod == 0 and mod == 0: #GUEST

        if greet: SendPublicMessage('Welcome to the room %s: %s (Level %s). 💓' % (name, handle, mod))
        print('[User Join] %s(Level %s) has joined the room!' % (name, mod))
        if name not in Level0:
            Level0.append(name)
            userlist.append(handle)
            if debugging:print("[User Join] %s added to Guests!" % name)


    if mod == 1 and mod == 1: #EVERYONE
        if greet: SendPublicMessage('Welcome to the room %s: %s (Level %s). 💓' % (name, handle, mod))
        print('[Operator Join] %s(Level %s) has joined the room!' % (name, mod))
        if name not in Level1:
            Level1.append(name)
            userlist.append(handle)
            if debugging:print("[User Join] %s added to everyone!" % name)

    if mod == 2 and mod == 2: #OPERATOR
        if greet: SendPublicMessage('Welcome to the room %s: %s (Level %s). 💓' % (name, handle, mod))
        print('[Moderator Join] %s(Level %s) has joined the room!' % (name, mod))
        if name not in Level2:
            Level2.append(name)
            userlist.append(handle)
            if debugging:print("[User Join] %s added to Operators!" % name)

    if mod == 3 and mod == 3: #COWNER
        if greet: SendPublicMessage('Welcome to the room %s: %s (Level %s). 💓' % (name, handle, mod))
        print('[CoOwner Join] %s(Level %s) has joined the room!' % (name, mod))
        if name not in Level3:
            Level3.append(name)
            userlist.append(handle)
            if debugging:print("[User Join] %s added to CoOwners!" % name)

    if mod == 4 and mod == 4: #ADMIN
        if greet: SendPublicMessage('Welcome to the room %s: %s (Level %s). 💓' % (name, handle, mod))
        print('[Admin Join] %s(Level %s) has joined the room!' % (name, mod))
        if name not in Level4:
            Level4.append(name)
            userlist.append(handle)
            if debugging:print("[User Join] %s added to Admins!" % name)
def HandleCheck():
    roomcount = len(Level0)
    SendPublicMessage(str(roomcount))

def HandleUserlist(data):

    producers = data['users']

    for producer in producers:
        user_handle = producer['handle']
        user_avatar = producer['avatar']
        user_chatcolor = producer['chatcolor']
        user_namecolor = producer['namecolor']
        user_username = producer['username']
        user_nick = producer['nick']
        user_mod = producer['mod']

        userdata = "%s|%s|%s|%s|%s|%s|%s|" % (user_handle,user_avatar,user_chatcolor,user_namecolor,user_username,user_nick,user_mod)
        if user_handle not in userlist:
            userlist.append(user_handle)
            print(userlist)
        if user_nick not in Level0 and user_mod == 0:
            if user_nick not in Level0:Level0.append(user_nick)
            if debugging:print("[User Join] %s added to everyone!" % user_nick)
        if user_nick not in Level1 and user_mod == 1:
            if user_nick not in Level1:Level1.append(user_nick)
            if debugging:print("[Operator Join] %s added to Operators!" % user_nick)
        if user_nick not in Level2 and user_mod == 2:
            if user_nick not in Level2:Level2.append(user_nick)
            if debugging:print("[Moderator Join] %s added to Moderators!" % user_nick)
        if user_nick not in Level3 and user_mod == 3:
            if user_nick not in Level3:Level3.append(user_nick)
            if debugging:print("[CoOwner Join] %s added to CoOwners!" % user_nick)
        if user_nick not in Level4 and user_mod == 4:
            if user_nick not in Level4:Level4.append(user_nick)
            if debugging:print("[Admin Join] %s added to Admins!" % user_nick)

        #CheckUserExist(user_username, userdata)
        #GetScore(user_username)
def HandleProducers(data):
    
    producers = data['producers']
    for producer in producers:
        handle = producer['handle']
        if VIPCAM: CheckCamBan(handle)
        if debugging:print(f'{handle} is broadcasting!'.format(handle))
def HandleQuit(data):
    handle = data['handle']
    print('%s has left the room!' % handle)

    if handle in userlist:
        userlist.remove(handle)

    if handle in Level0:
        Level0.remove(handle)
    if handle in Level1:
        Level1.remove(handle)
    if handle in Level2:
        Level2.remove(handle)
    if handle in Level3:
        Level3.remove(handle)
    if handle in Level4:
        Level4.remove(handle)
def HandleCallBack(data):

    
    decode = json.loads(str(data))
    
    event = decode["cc"]
    if debugging:print("event = %s" % event)
    print(data)


    if event.startswith('ping'):
        Handle_Ping()     

    if event.startswith('sysmsg'):
        Handle_OnSys(decode)

    if 'joined' in event:
        Handle_Joined(decode) 
        #done

    if 'join' in event and len(event) < 5:
        HandleUserJoin(decode)

    if event.startswith('userlist'):
        HandleUserlist(decode)

    if event.startswith('youtube'):
        Handle_YoutubePlay(decode)

    if event.startswith('producers'):
        HandleProducers(decode)

    if event.startswith('quit'):
        HandleQuit(decode)

    if event.startswith('msg'):
        HandlePublicMessage(decode)
    if event.startswith('pvtmsg'):
        HandlePrivateMessage(decode)

def Connect():


    payload = {'username': username,'password': password}
    
    with requests.Session() as session:
        p = session.post('https://stumblechat.com/login', data=payload)
        print("Logged in...")
        g = session.get(tokenUrl)
        #print(g.text)
    
        usertoken = g.text
        msg = json.loads(usertoken)
        token = msg['result']
        endpoint = msg['endpoint']
        if debugging: print("Getting Token...")  
        

        ws.send(json.dumps({"cc":"join", "token": token, "room": room, "nick": botsname}))
        print("%s is online! Connected to %s" % (botsname, endpoint))

        if annoucement:
            SendPublicMessage("%s is online!" % botsname)

        
        events = []    
        while(1):
            
            isonline = True

            data = ws.recv()
            fix = type(data)
            if debugging: print(data)

            if data:
                
                HandleCallBack(data)
                
                with open("logs.js", 'a', errors='ignore') as writelog:
                    writelog.write(data + '\n')

Connect()
