from __future__ import print_function
import discord
from discord.ext import commands
from overwatch_api import *
from overwatch_api.core import AsyncOWAPI
from overwatch_api.constants import *
from pprint import pprint

import rocket_snake as rs

import asyncio, aiohttp
import os
import gc
import sys
import time
import traceback
import subprocess
import random
import json
import threading
import inventory
from open_case import open_case
# import urllib.request

description = "This is a bot programmed and managed by Tyler or aka Nexus Novaz"
bot_prefix = "-"

client = commands.Bot(description = description, command_prefix = bot_prefix)

# def get_price(currencyNum, weapon, skin, wear):
# 	link = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=" + str(currencyNum) + "&market_hash_name=" + weapon + " | " + skin + " (" + wear + ")"
# 	link = str.replace(link, " ", "%20")
# 	with urllib.request.urlopen(link) as url:
# 	    data = json.loads(url.read().decode())
#
# 	return data

#user is ctx
#r is either string of the role name or a list or roles (will return true if the user has any of the roles)
#e.g either "Staff" or ["Staff", "Moderator"]

def has_role(ctx, r):
	roles = []
	if not isinstance(r, list):
		roles.append(r)
	else:
		roles = r

	if ctx.message.author == ctx.message.server.owner:
		return True
	else:
		allowed = False
		for i in range(0, len(ctx.message.author.roles)):
			for j in range(0, len(roles)):
				if ctx.message.author.roles[i].name == roles[j]:
					allowed = True
					break
		return allowed

def is_server_owner(ctx):
	if ctx.message.author == ctx.message.server.owner:
		return True
	else:
		return False

def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

@client.event
async def on_ready():
	print("""
	Logged In.
	Name: {}
	ID: {}
	Discord Version: {}
	I'm Online!""".format(client.user.name, client.user.id, discord.__version__))
	await client.change_presence(game = discord.Game(name = open("game.txt", "r").read()))

@client.command(pass_context = True)
async def myinv(ctx, page = 1):
	# await client.say(inventory.get_price("AK-47", "Frontside Misty", "Minimal Wear"))
	await client.say(embed = inventory.get_embed(ctx.message.author.id, page) )

@client.command(pass_context = True)
async def quit(ctx):
	if not has_role(ctx, "I.T"):
		await client.say("You don't have permissions for this command")
	else:
		await client.say("Going offline!")
		await client.delete_message(ctx.message)
		await client.close()

@client.command(pass_context = True)
async def clear(ctx, number = None):
	if not has_role(ctx, "Staff"):
		await client.say("You don't have the permissions for this command")
	else:
		mgs = []
		if number == None or not is_int(number):
			await client.say("Correct usage: ```{}clear <integer>```".format(bot_prefix))
		else:
			number = int(number)
			if number < 2:
				await client.delete_message(ctx.message)
			elif number > 99:
				number = 99

			async for x in client.logs_from(ctx.message.channel, limit = number):
				mgs.append(x)

			if len(mgs) > 1:
				await client.delete_messages(mgs)
			else:
				await client.delete_message(ctx.message)

@client.command(pass_context = True)
async def playing(ctx):
	if not has_role(ctx, "Staff"):
		await client.say("You don't have permission to use this command")
	else:
		msg = ctx.message.content.split(" ")[1:]
		game = ""
		for x in range(0, len(msg)):
			game += msg[x] + " "
		open("game.txt", "w").write(game)
		await client.change_presence(game = discord.Game(name = open("game.txt", "r").read() ))
		await client.say("NexusBot is now playing: " + open("game.txt", "r").read() )
		await client.delete_message(ctx.message)

@client.command(pass_context = True)
async def choose(ctx):
	if not has_role(ctx, "Verified"):
		await client.say("You don't have the permission to use this command")
	else:
		options = ctx.message.content.split(" ")[1:]
		await client.say(options[random.randrange(0, len(options)-1)])

@client.command(pass_context = True)
async def rand(ctx, num1 = None, num2 = None):
	if num1 == None or num2 == None:
		await client.say("Correct usage: ```" + bot_prefix + "random <min integer> <max integer>```")
	elif not is_int(num1) or not is_int(num2):
		await client.say("Correct usage: ```" + bot_prefix + "random <min integer> <max integer>```")
	else:
		num1 = int(num1)
		num2 = int(num2)
		if num1 - num2 <= 0:
			await client.say("Enter values with a difference or more than 0")
		else:
			rand = random.randrange(num1, num2)
			await client.say(rand)

@client.command(pass_context = True)
async def openCase(ctx, case):
	if case.lower() == "list":
		cases = os.listdir("cases")
		case_str = ""
		for casename in cases:
			if casename != "blank.json":
				case_str += casename[:-5] + "\n"
		await client.say(case_str)
	else:
		weapon = open_case(case.lower())
		if isinstance(weapon, str):
			await client.say(weapon)
		else:
			inventory.write(ctx.message.author.id, weapon)
			if weapon["StatTrack"] == True:
				drop = discord.Embed(title = "@" + ctx.message.author.name + " unboxed:", description=weapon["weapon"] + " | " + weapon["skin"] + "\n" + "StatTrack", color = int(weapon["color"], 16))
			else:
				drop = discord.Embed(title = "@" + ctx.message.author.name + " unboxed:", description=weapon["weapon"] + " | " + weapon["skin"], color = int(weapon["color"], 16))

			drop.set_image(url = weapon["icon"])
			drop.add_field(name = "**Condition**", value = weapon["condition"], inline = True)
			drop.add_field(name = "**Float**", value = weapon["float"]["value"], inline = True)
			drop.add_field(name = "**Case:**", value = weapon["case"], inline = True)
			# drop.add_field(name = "**Price**", value = get_price(2, weapon["weapon"], weapon["skin"], weapon["condition"])["lowest_price"] + " | " + get_price(3, weapon["weapon"], weapon["skin"], weapon["condition"])["lowest_price"])
			await client.say(embed = drop)
			await client.delete_message(ctx.message)
			
@client.command(pass_context = True)
async def rlstats(ctx, player):
	client = rs.RLS_Client("7GLWZDHT8G884IJJJ5OYVJTVM90WGQ2R")
	client.get_player(str(player))
	
