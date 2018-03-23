import os
import gc
import sys
import time
import traceback
import json
import random

def open_case(case):
	if os.path.exists("cases/"+case+".json"):
		case = json.loads(open("cases/"+case+".json", "r").read() )
	else:
		return case + " is not a valid case"

	r = random.uniform(0, 1)

	g = {
			"mil-spec" : {
			"name" : "Mil-Spec",
			"color" : "6d97db",
		},
			"restricted" : {
			"name" : "Restricted",
			"color" : "bb5dea",
		},
			"classified" : {
			"name" : "Classified",
			"color" : "ff3fd2",
		},
			"covert" : {
			"name" : "Covert",
			"color" : "ea3515",
		},
			"special" : {
			"name" : "Special",
			"color" : "ea3515",
		},
	}

	statTrack = False

	if r < 0.7486:
		grade = "mil-spec"
	elif r < 0.8319:
		statTrack = True
		grade = "mil-spec"
	elif r < 0.9581:
		grade = "restricted"
	elif r < 0.9727:
		grade = "restricted"
		statTrack = True
	elif r < 0.9951:
		grade = "classified"
	elif r < 0.9965:
		grade = "classified"
		statTrack = True
	elif r < 0.9992:
		grade = "covert"
	elif r < 0.9992:
		grade = "covert"
		statTrack = True
	elif r < 0.9997:
		grade = "special"
	else:
		grade = "special"
		statTrack = True


	weapon = case[grade][random.randrange(0, len(case[grade]))]
	weapon["float"]["value"] = random.uniform(weapon["float"]["min"], weapon["float"]["max"])
	weapon["grade"] = g[grade]["name"]
	weapon["color"] = g[grade]["color"]
	weapon["case"] = case["name"]

	if weapon["float"]["value"] < 0.07:
		weapon["condition"] = "Factory New"
	elif weapon["float"]["value"] < 0.15:
		weapon["condition"] = "Minimal Wear"
	elif weapon["float"]["value"] < 0.38:
		weapon["condition"] = "Field-Tested"
	elif weapon["float"]["value"] < 0.45:
		weapon["condition"] = "Well-Worn"
	else:
		weapon["condition"] = "Battle-Scarred"

	weapon["StatTrack"] = statTrack

	return weapon
