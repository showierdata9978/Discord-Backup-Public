from discord import Webhook, RequestsWebhookAdapter # Importing discord.Webhook and discord.RequestsWebhookAdapter
import discord
from MeowerBot import Client
import os
import threading
import sys as sus

TOKEN = "Token Here"

channelbridge = 990279484341125130
channelbridge2 = 962646188220370974

print("init")

client = discord.Client()

ulist = "No Ulist Update."

import json
#fp = open("ids.json", "r")
#ids = json.load(fp)

backup_up = False
enable_statuses = False
msgfromeower = True
sendmsgtomeower = True
impersonationtext = True

c = Client("username","password",False) 

print("client init")

webhook = Webhook.from_url('weebhook', adapter=RequestsWebhookAdapter())
print("webhook init")

os.system("pip install meowerbot --upgrade")

# todo (based on what to do first):
# fix security (arrows api)
# mod only options system
# better pass

print("start bot")

def on_raw_msg(msg:dict):
    if backup_up and msgfromeower:
        if not "@everyone" in msg["p"] and not "@here" in msg["p"] and not "<@" in msg["p"]:
            #sendmsg("cant sned messages because bloctans is stupid and also security issue\nim waiting for arrow to make a system for me")
            sendmsg(msg["p"],msg["u"])
        else:
            print(msg)
            sendmsg("This message had a bad @ in it,\nView the raw JSON of this msg at "+"https://api.meower.org/posts?id="+msg["_id"], msg["u"])

webhookless = False

def sendmsg(msg,user="",pfp=""):
    channel = client.get_channel(962646188220370974)
    if webhookless:
        client.loop.create_task(channel.send(msg))
    else:
        webhook.send(content=msg,username=user,avatar_url=pfp)

def sendmsg_bot(msg):
    channel = client.get_channel(962646188220370974)
    client.loop.create_task(channel.send(msg))

import subprocess

async def handlecmds(msg):
    global backup_up
    global msgfromeower
    global enable_statuses
    global sendmsgtomeower
    global impersonationtext
    if msg.content == "!ulist":
        sendmsg_bot("The current ulist is: "+ulist)
    elif msg.content.startswith("!options"):
        args = msg.content.split(" ")
        role_names = [role.name for role in msg.author.roles]
        if "The Council of Meowers" in role_names or msg.author.id == 709226842149748767:
            if len(args) == 1:
                sendmsg_bot("Usage: !options <enablebridgebackup:Boolean> <getmsgfromeower:boolean> <statuses:boolean> <impersonationtext:boolean> <sendmsgtomeower:boolean>\n Defaults to: false true false true true")
            else:
                tosend = ""

                if args[1] == "true":
                    backup_up = True
                    tosend = tosend + "set <enablebridgebackup:Boolean> to true\n"
                else:
                    backup_up = False
                    tosend = tosend + "set <enablebridgebackup:Boolean> to false\n"

                if args[2] == "true":
                    msgfromeower = True
                    tosend = tosend + "set <msgfrommeower:Boolean> to true\n"
                else:
                    msgfromeower = False
                    tosend = tosend + "set <msgfrommeower:Boolean> to false\n"

                if args[3] == "true":
                    enable_statuses = True
                    tosend = tosend + "set <statuses:Boolean> to true\n"
                else:
                    enable_statuses = False
                    tosend = tosend + "set <statuses:Boolean> to false\n"

                if args[5] == "true":
                    sendmsgtomeower = True
                    tosend = tosend + "set <sendmsgtomeower:Boolean> to true\n"
                else:
                    sendmsgtomeower = False
                    tosend = tosend + "set <sendmsgtomeower:Boolean> to false\n"

                if args[4] == "true":
                    impersonationtext = True
                    tosend = tosend + "set <impersonationtext:Boolean> to true\n"
                else:
                    impersonationtext = False
                    tosend = tosend + "set <impersonationtext:Boolean> to false\n"

                sendmsg_bot(tosend)
        else:
            sendmsg_bot("Admin Only.")
    elif msg.content == "!testbridgemsg":
        sendmsg_bot("hello")
        print(msg)
        role_names = [role.name for role in msg.author.roles]
        if "Team Meower" in role_names:
            print("Council member")
    elif msg.content == "!restart":
        role_names = [role.name for role in msg.author.roles]
        if "The Council of Meowers" in role_names or msg.author.id == 709226842149748767:
            subprocess.Popen("main.py")
            sus.exit() 
        else:
            sendmsg_bot("Needs Admin.")
    elif msg.content == "!quit":
        role_names = [role.name for role in msg.author.roles]
        if "The Council of Meowers" in role_names or msg.author.id == 709226842149748767:
            quit()
        else:
            sendmsg_bot("Needs Admin.")
    elif msg.content.startswith("!!"):
        print("no send")
    elif msg.content == "!bbhelp":
        sendmsg_bot("commands:\n!ulist\n!testbridgemsg\n\nAdmins:\n!options <enablebridgebackup:Boolean> <getmsgfromeower:boolean> <statuses:boolean> <impersonationtext:boolean> <sendmsgtomeower:boolean>\n!quit\n!restart")
    else:
        sendmsg_bot("Invalid")

@client.event
async def on_ready():
    sendmsg_bot("will now init, !bbhelp for commands plz")

@client.event
async def on_message(msg):
    global channelbridge
    if not msg.webhook_id and msg.author.bot == False and msg.author.id != 982817154485321780 and msg.channel.id == channelbridge2 and not msg.content.startswith("!"):
        #name = ""
        #for i in ids:
        #    if i == str(msg.author.id):
        #        name = ids[i]
        #        if name == "":
        #            name = "User who has not set up discordbackup"
        #c.send_msg(name + ": " + msg.content)
        if backup_up:
            if sendmsgtomeower:
                if impersonationtext:
                    c.send_msg(msg.author.name + ": " + msg.content + " | Note: this message might not be from who it really is")
                else:
                    c.send_msg(msg.author.name + ": " + msg.content)
    elif msg.content.startswith("!"):
        await handlecmds(msg)

def on_error(data):
	print("error of " + data + ", ignoring")
	pass

print("init func")

c.callback(on_raw_msg)
c.callback(on_error)

print("cb")

from json import loads

def handlestatuses(oldulist):
    userlogin = ""
    userout = ""
    if len(ulist) > len(oldulist):
        for user in ulist.split(";"):
            if user in oldulist.split(";"):
                continue
            else:
                userlogin = user
                if userlogin == "Discord":
                    quit()
        if enable_statuses:
            c.send_msg(userlogin + " logged in!")
    elif len(ulist) < len(oldulist):
        for user2 in oldulist.split(";"):
            if user2 in ulist.split(";"):
                continue
            else:
                userout = user2
        if enable_statuses:
            c.send_msg(userout + " logged off!")

def packethandlelol(packet:dict):
    global ulist
    packetc = loads(packet)
    if packetc["cmd"] == "ulist":
        oldulist = ulist
        ulist = packetc["val"]
        handlestatuses(oldulist)
    c._bot_packet_handle(packet)

c._wss.callback("on_packet",packethandlelol)

t1 = threading.Thread(target=c.start)
t1.daemon = True
t1.name = 'Bot'
t1.start()

print("start bot")

client.run(TOKEN)
