import math
import json
import urllib.request
import discord
import os
import math

blank = {"items" : []}

def get_price(weapon, skin, wear):
	link = "http://steamcommunity.com/market/priceoverview/?appid=730&currency=2" + "&market_hash_name=" + weapon + " | " + skin + " (" + wear + ")"
	link = str.replace(link, " ", "%20")
	with urllib.request.urlopen(link) as url:
	    data = json.loads(url.read().decode())

	return data

def get_embed(userid, page):
    inv = get(userid)["items"]
    page = page - 1

    if page < 0 or page >= math.ceil( len(inv) / 10):
        page = 0
    inv_embed = discord.Embed(title = "Inventory", color = 0x00ff00)

    for item in inv[page * 10:page * 10 + 10]:
        inv_embed.add_field(name = item["weapon"] + " | " + item["skin"], value = item["condition"] + " | " + str(item["float"]), inline = False)
    inv_embed.add_field(name = "Page " + str(page + 1) + " of " + str(math.ceil(len(inv) / 10)), value = "Total items = " + str(len(inv)))
    return inv_embed

def get(userid):
    path = "inv/" + str(userid) + ".json"

    if os.path.exists(path):
        with open(path, "r") as inventory_file:
            inv = json.loads(inventory_file.read())
    else:
        with open(path, "w+") as inventory_file:
            inv = json.dump(blank, inventory_file)
            return blank

    return inv

def write(userid, weapon):
    path = "inv/" + str(userid) + ".json"
    inv = get(userid)
    weapon = dict(weapon)
    weapon.pop("case", None)
    weapon.pop("icon", None)
    weapon.pop("grade", None)
    weapon.pop("color", None)
    weapon["float"] = weapon["float"]["value"]
    inv["items"].insert(0, weapon)

    with open(path, "w+") as inventory_file:
        inv = json.dump(inv, inventory_file)
