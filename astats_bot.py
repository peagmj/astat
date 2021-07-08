#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
# import required modules
#
import sys, os, getopt
import time 
import requests
import json

from secrets import TOKEN,ChatIDs,AStatGroups,api_key
import datetime
from time import strftime,gmtime
from requests.adapters import HTTPAdapter
from collections import OrderedDict
from operator import getitem
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf-8')

url = 'http://www.agent-stats.com/'
TURL = "https://api.telegram.org/bot{}/".format(TOKEN)

Testmodus= False
Logging = True
language = "DE"
group= ""

emoji = {"thumbUp": u"👍",
		"trophy": u"🏆",
		"first_place_medal": u"🥇",
		"second_place_medal": u"🥈",
		"third_place_medal": u"🥉",
		"gem": u"💎",
		"bomb": u"💣",
		"military_medal": u"🎖",
		"enl": u"🟢",
		"res": u"🔵"
	}

ranking_emoji = {
	1: emoji["first_place_medal"],
	2: emoji["second_place_medal"],
	3: emoji["third_place_medal"],
	4: "4. ",
	5: "5. ",
	6: "6. ",
	7: "7. ",
	8: "8. ",
	9: "9. ",
	10: "10.",
	11: "11.",
	12: "12.",
	13: "13.",
	14: "14.",
	15: "15.",
	16: "16.",
	17: "17.",
	18: "18.",
	19: "19.",
	20: "20.",
	21: "21.",
	22: "22.",
	23: "23.",
	24: "24.",
	25: "25.",
	26: "26.",
	27: "27.",
	28: "28.",
	29: "29.",
	30: "30.",
	31: "31.",
	32: "32.",
	33: "33.",
	34: "34.",
	35: "35.",
	36: "36.",
	37: "37.",
	38: "38.",
	39: "39.",
	40: "40.",
	41: "41.",
	42: "42.",
	43: "43.",
	44: "44.",
	45: "45.",
	46: "46.",
	47: "47.",
	48: "48.",
	49: "49.",
	50: "50."
	}

Badges = {
	"explorer" : {
			"Name":"Unique Portals Visited",
			"File":"Explorer",
			"Bronze": 100,
			"Silber": 1000,
			"Gold"  : 2000,	
			"Platin": 10000,	
			"Black" : 30000
			},
	"seer": {
			"Name":"Seer Points",
			"File":"Neutral",
			"Bronze": 10,	
			"Silber": 50,	
			"Gold"  : 200,	
			"Platin": 500,	
			"Black" : 5000
			},
	"recon": {
			"Name":"OPR Agreements",
			"File":"Recon",
			"Bronze": 100,	
			"Silber": 750,	
			"Gold"  : 2500,	
			"Platin": 5000,
			"Black" : 10000
			},
	"scout": {
			"Name":"Portal Scans Uploaded",
			"File":"Scout",
			"Bronze": 50,	
			"Silber": 250,	
			"Gold"  : 1000,	
			"Platin": 3000,
			"Black" : 6000
			},
	"scout_controller" : {
			"Name":"Uniques Scout Controlled",
			"File":"Scout_Controller",
			"Bronze": 100,	
			"Silber": 500,	
			"Gold"  : 1000,	
			"Platin": 5000,
			"Black" : 12000
			},
	"builder": {
			"Name":"Resonators Deployed",
			"File":"Builder",
			"Bronze": 2000,	
			"Silber": 10000,	
			"Gold"  : 30000,
			"Platin": 100000,	
			"Black" : 200000
			},
	"connector": {
			"Name":"Links Created",
			"File":"Connector",
			"Bronze": 50,	
			"Silber": 1000,	
			"Gold"  : 5000,	
			"Platin": 25000,	
			"Black" : 100000
			},
	"mind-controller": {
			"Name":"Control Fields Created",
			"File":"Mind_Controller",
			"Bronze": 100,	
			"Silber": 500,	
			"Gold"  : 2000,	
			"Platin": 10000,	
			"Black" : 40000
			},
	"illuminator" : {
			"Name":"Mind Units Captured",
			"File":"Illuminator",
			"Bronze": 5000,	
			"Silber": 50000,	
			"Gold"  : 250000,	
			"Platin": 1000000,	
			"Black" : 4000000
			},
	"recharger": {
			"Name":"XM Recharged",
			"File":"Recharger",
			"Bronze": 100000,
			"Silber": 1000000,	
			"Gold"  : 3000000,	
			"Platin": 10000000,	
			"Black" : 25000000
			},
	"liberator": {
			"Name":"Portals Captured",
			"File":"Liberator",
			"Bronze": 100,	
			"Silber": 1000,	
			"Gold"  : 5000	,
			"Platin": 15000	,
			"Black" : 40000
			},
	"pioneer": {
			"Name":"Unique Portals Captured",
			"File":"Pioneer",
			"Bronze": 20,	
			"Silber": 200,	
			"Gold"  : 1000,	
			"Platin": 5000	,
			"Black" : 20000
			},
	"engineer": {
			"Name":"Mods Deployed",
			"File":"Engineer",
			"Bronze": 150,	
			"Silber": 1500,	
			"Gold"  : 5000	,
			"Platin": 20000	,
			"Black" : 50000
			},
	"hacker": {
			"Name":"Hacks",
			"File":"Hacker",
			"Bronze": 2000	,
			"Silber": 10000	,
			"Gold"  : 30000	,
			"Platin": 100000,	
			"Black" : 200000
			},
	"maverick": {
			"Name":"Drone Hacks",
			"File":"Neutral",
			"Bronze": 250	,
			"Silber": 1000	,
			"Gold"  : 2000	,
			"Platin": 5000	,
			"Black" : 10000
			},
	"translator": {
			"Name":"Glyph Hack Points",
			"File":"Translator",
			"Bronze": 200	,
			"Silber": 2000	,
			"Gold"  : 6000	,
			"Platin": 20000	,
			"Black" : 50000
			},
	"sojourner": {
			"Name":"Longest Sojourner Streak",
			"File":"Sojourner",
			"Bronze": 15	,
			"Silber": 30	,
			"Gold"  : 60	,
			"Platin": 180	,
			"Black" : 360
			},
	"epoch": {
			"Name":"Completed Hackstreaks",
			"File":"Epoch",
			"Bronze": 2	,
			"Silber": 4	,
			"Gold"  : 8	,
			"Platin": 30,	
			"Black" : 60
			},
	"purifier": {
			"Name":"Resonators Destroyed",
			"File":"Purifier",
			"Bronze": 2000,	
			"Silber": 10000,	
			"Gold"  : 30000	,
			"Platin": 100000,	
			"Black" : 300000
			},
	"trekker": {
			"Name":"Distance Walked",
			"File":"Trekker",
			"Bronze": 10	,
			"Silber": 100	,
			"Gold"  : 300	,
			"Platin": 1000	,
			"Black" : 2500
			},
	"specops": {
			"Name":"Unique Missions Completed",
			"File":"SpecOps",
			"Bronze": 5	,
			"Silber": 25,	
			"Gold"  : 100,	
			"Platin": 200,	
			"Black" : 500
			},
	"missionday" : { 
			"Name":"Mission Day(s) Attended",
			"File":"Mission_Day",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 6	,
			"Platin": 10,	
			"Black" : 20
			},
	"nl-1331-meetups": {
			"Name":"NL-1331 Meetup(s) Attended",
			"File":"NL-1331_Meetups",
			"Bronze": 1	,
			"Silber": 5	,
			"Gold"  : 10,	
			"Platin": 25,	
			"Black" : 50
			},
	"recruiter": {
			"Name":"Agents Recruited",
			"File":"Recruiter",
			"Bronze": 2	,
			"Silber": 10,	
			"Gold"  : 25,	
			"Platin": 50,	
			"Black" : 100
			},
	"recursions": {
			"Name":"Recursions",
			"File":"Simulacrum",
			"Bronze": 1,
			"Silber": 2,
			"Gold"  : 3,
			"Platin": 4,
			"Black" : 5
			},
	"prime_challenge": {
			"Name":"Prime Challenges",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 2	,
			"Gold"  : 3	,
			"Platin": 4	,
			"Black" : 5
			},
	"stealth_ops": {
			"Name":"Stealth Ops Missions",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 6	,
			"Platin": 10,	
			"Black" : 20
			},
	"opr_live": {
			"Name":"OPR Live Events",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 6	,
			"Platin": 10,	
			"Black" : 20
			},
	"ocf": {
			"Name":"Clear Fields Events",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 6	,
			"Platin": 10,	
			"Black" : 20
			},
	"intel_ops": {
			"Name":"Intel Ops Missions",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 6	,
			"Platin": 10,	
			"Black" : 20
			},
	"ifs": {
			"Name":"First Saturday Events",
			"File":"First_Saturday",
			"Bronze": 1	,
			"Silber": 6	,
			"Gold"  : 12,	
			"Platin": 24,	
			"Black" : 36
			},
	"drone_explorer": {
			"Name":"Unique Portals Drone Visited",
			"File":"Neutral",
			"Bronze": 100,	
			"Silber": 1000,	
			"Gold"  : 2000	,
			"Platin": 10000	,
			"Black" : 30000
			},
	"drone_distance": {
			"Name":"Furthest Drone Distance",
			"File":"Neutral",
			"Bronze": 10	,
			"Silber": 50	,
			"Gold"  : 100	,
			"Platin": 250	,
			"Black" : 500
			},
	"discoverer": {
			"Name":"Portals Discovered",
			"File":"Neutral",
			"Bronze": 10	,
			"Silber": 50	,
			"Gold"  : 200	,
			"Platin": 500	,
			"Black" : 5000
			},
	"collector": {
			"Name":"XM Collected",
			"File":"Neutral",
			"Bronze": 100000,	
			"Silber": 1000000,	
			"Gold"  : 10000000,	
			"Platin": 100000000,	
			"Black" : 200000000
			},
	"crafter": {
			"Name":"Kinetic Capsules Completed",
			"File":"Neutral",
			"Bronze": 50	,
			"Silber": 100	,
			"Gold"  : 200	,
			"Platin": 350	,
			"Black" : 700
			},
	"binder": {
			"Name":"Longest Link Ever Created",
			"File":"Neutral",
			"Bronze": 10	,
			"Silber": 200	,
			"Gold"  : 800	,
			"Platin": 1300	,
			"Black" : 1800
			},
	"country-master": {
			"Name":"Largest Control Field",
			"File":"Neutral",
			"Bronze": 5000	,
			"Silber": 30000	,
			"Gold"  : 100000,	
			"Platin": 1000000,	
			"Black" : 5000000
			},
	"neutralizer": {
			"Name":"Portals Neutralized",
			"File":"Neutral",
			"Bronze": 100	,
			"Silber": 1000	,
			"Gold"  : 5000	,
			"Platin": 15000	,
			"Black" : 40000
			},
	"disruptor": {
			"Name":"Enemy Links Destroyed",
			"File":"Neutral",
			"Bronze": 50	,
			"Silber": 1000	,
			"Gold"  : 5000	,
			"Platin": 25000	,
			"Black" : 100000
			},
	"salvator": {
			"Name":"Enemy Fields Destroyed",
			"File":"Neutral",
			"Bronze": 100	,
			"Silber": 500	,
			"Gold"  : 2000	,
			"Platin": 10000	,
			"Black" : 40000
			},
	"bb_combatant": {
			"Name":"Battle Beacon Combatant",
			"File":"Neutral",
			"Bronze": 10	,
			"Silber": 50	,
			"Gold"  : 200	,
			"Platin": 1000	,
			"Black" : 4000
			},
	"guardian": {
			"Name":"Max Time Portal Held",
			"File":"Guardian",
			"Bronze": 3	,
			"Silber": 10,	
			"Gold"  : 20,	
			"Platin": 90,	
			"Black" : 150
			},
	"smuggler": {
			"Name":"Max Time Link Maintained",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 5	,
			"Gold"  : 10,	
			"Platin": 45,	
			"Black" : 75
			},
	"link-master": {
			"Name":"Max Link Length x Days",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 10,	
			"Gold"  : 50,	
			"Platin": 200,	
			"Black" : 1000
			},
	"controller": {
			"Name":"Max Time Field Held",
			"File":"Neutral",
			"Bronze": 1	,
			"Silber": 3	,
			"Gold"  : 8	,
			"Platin": 30,	
			"Black" : 50
			},
	"field-master": {
			"Name":"Largest Field MUs x Days",
			"File":"Neutral",
			"Bronze": 5000,	
			"Silber": 40000,	
			"Gold"  : 150000,	
			"Platin": 400000,	
			"Black" : 1000000
			},
	"drone_recalls": {
			"Name":"Forced Drone Recalls",
			"File":"Neutral",
			"Bronze": 50	,
			"Silber": 100	,
			"Gold"  : 250	,
			"Platin": 500	,
			"Black" : 1000
			},
	"drone_sender": {
			"Name":"Drones Returned",
			"File":"Neutral",
			"Bronze": 100	,
			"Silber": 200	,
			"Gold"  : 500	,
			"Platin": 800	,
			"Black" : 1200
			},
	"lifetime_ap": {
			"Name":"Lifetime AP",
			"File":"Neutral",
			"Bronze": 55555555	,
			"Silber": 66666666	,
			"Gold"  : 77777777	,
			"Platin": 88888888	,
			"Black" : 99999999
			}
		}

BadgeLvlList = {"Bronze":{
					"Rank":1,
					"File": "bronze"},
				"Silber":{
					"Rank":2,
					"File": "silver"},
				"Gold":{
					"Rank":3,
					"File": "gold"},
				"Platin":{
					"Rank":4,
					"File": "platinum"},
				"Black":{
					"Rank":5,
					"File": "black"}
			}
		
stattypes = [#"ap",
			"lifetime_ap", 
              "explorer", 
#              "discoverer", 
#              "seer", 
              "collector", 
#              "recon", 
              "hacker", 
              "builder", 
              "connector", 
              "mind-controller", 
              "illuminator", 
#              "binder", 
#              "country-master", 
              "recharger", 
              "liberator", 
              "pioneer", 
              "purifier", 
              "neutralizer", 
              "disruptor", 
              "salvator", 
              "trekker", 
#             "guardian", 
#              "smuggler", 
#              "link-master", 
#              "controller", 
#              "field-master", 
              "specops", 
              "engineer", 
#              "sojourner", 
#              "recruiter", 
              "translator", 
#              "missionday", 
#              "nl-1331-meetups", 
#              "recursions", 
#              "prime_challenge", 
#              "stealth_ops", 
#              "opr_live", 
#              "ocf", 
#              "intel_ops", 
#              "ifs", 
              "scout", 
              "drone_explorer", 
#              "drone_distance", 
              "maverick", 
#              "drone_recalls", 
#              "drone_sender", 
              "scout_controller" 
#              "bb_combatant", 
#              "crafter", 
#              "epoch", 
#              "level", 
#              "faction", 
#              "last_submit"
	]

toutput = {
	"T1": {
		"EN":"{0}The <b>Top-{1}</b> in {2} ({3}) {4}: \n",
		"DE":"{0}Die <b>Top-{1}</b> bei {2} ({3}) {4}: \n"
		},
	"T2": {
		"DE":"{0} Klasse Leistung Agent {1}, Glueckwunsch zum LevelUp. \nNeues Level: {2}",
		"EN":"{0} Top performance agent {1}, congratulation to level up. \nNew level: {2}"
		},	
	"T3": {
		"DE":"{0}Daumen hoch an Agent <b>{1}</b> zur {2} Badge ({3}). \nNeue Stufe: {4} {5}\n Herzlichen Glueckwunsch!",
		"EN":"{0}Thumb up to agent <b>{1}</b> for {2} badge ({3}). \nNew rank: {4} {5}\n Good work!"
		},
	"T4": {
		"DE":"{0}Daumen hoch an Agent {1} zur <b>{2}</b>-fachen Black Badge {3} ({4}). \n Herzlichen Glueckwunsch!",
		"EN":"{0}Thumb up to agent {1} for <b>{2}</b>-time black badge {3} ({4}). \n Good Work!"
		}

	}
	
timespans = {
	"week": {"DE":"in der letzten Woche",
			"EN":"in the last week"
			},
	"custom": {"DE":"im vorgegebenen Zeitraum",
			"EN":"in the custom interval"
			},
	"all": {"DE":"im gesamten Zeitraum",
			"EN":"in all time"
			}
	}	
	
def print_json(your_json):
	parsed = json.loads(your_json)
	print(json.dumps(parsed, indent=4, sort_keys=False))

def get_new_dict_stats(group,Timespan=""):
	global Testmodus
	global Logging
	s = requests.Session()
	s.mount('https://', HTTPAdapter(max_retries=3))
	s.headers.update({'AS-Key': api_key})
	r = s.get('https://api.agent-stats.com/groups', stream=True)
	r.raise_for_status()
	groups = r.json()
	#print(groups)
	if Timespan == "week":
		r = s.get("https://api.agent-stats.com/groups/{}/week".format(AStatGroups[group]["ID"])) 
	elif Timespan == "custom":
		r = s.get("https://api.agent-stats.com/groups/{}/custom".format(AStatGroups[group]["ID"])) 
	else:
		r = s.get("https://api.agent-stats.com/groups/{}".format(AStatGroups[group]["ID"])) 
	r.raise_for_status()
	dict_stats = r.json() # convert to Dictionary
	if Testmodus:
		filename = "stats_"+group +"_"+datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".json"
		with open(filename, "w") as outfile:
			json.dump(dict_stats, outfile, ensure_ascii=False, indent=4)
		print ("Datei: "+ filename + " geschrieben")
	return dict_stats

def get_ordered_dict_stats(group,Ticket,Timespan="week"):
	return OrderedDict(sorted(get_new_dict_stats(group,Timespan).items(),key = lambda tup: (tup[1][Ticket], tup[1][Ticket]), reverse = True))
	
def get_daily_stattype():
	global Logging
	DayOfMonth= strftime("%d", gmtime())
	if Logging : print ("Tag des Monats: "+ DayOfMonth)
	x = int(DayOfMonth) % len(stattypes)
	if Logging : print ("Nummer des gewählten Statistiktyps: "+ str(x))
	if Logging : print ("gewählter Statistiktyp: "+ stattypes[x-1])
	return stattypes[x-1]

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def checkgroup(group):
	if len(group) >0:
		return group
	else:
		if len(AStatGroups)== 0:
			print ("No group in AStatGroups defined.")
			print_CLI_Help()
			sys.exit()
		elif len(AStatGroups)== 1:
			for AStatGroup in AStatGroups:
				return AStatGroup
		else:
			print ("No group from AStatGroups selected.")
			print_CLI_Help()
			sys.exit()
		
def get_chat_id():
	global Testmodus
	global Logging
	answer = requests.get(TURL+"getUpdates")
	content = answer.content
	data = json.loads(content)
	if data["ok"]== True:
		#if Logging: print_json(content)
		num_updates = len(data["result"])
		last_update = num_updates - 1
		#chat_id = data["result"][last_update]["message"]["chat"]["id"]
		#return chat_id
		if Testmodus :
			return ChatIDs["Bot"]
		else:
			return ChatIDs[group]
	else:
		print ("Fehler")
		print(data)
		return 1
	
def send_TGMessage(TGmessage,chat_id):
	global Logging	
	#text = urllib.parse.quote_plus(text)
	url = TURL + "sendMessage?chat_id={}&text={}&parse_mode=html".format(chat_id,TGmessage)
	#if Logging : print (url)
	response=get_url(url)
	if json.loads(response)["ok"]:
		return response
	else:
		print_json(response)
		exit(2)

def send_TGImage( image_path, image_caption=""):
	chat_id =get_chat_id()
	data = {"chat_id": chat_id, "caption": image_caption}
	if Logging: print(data)
	url = TURL+"sendPhoto"
	if Logging: print(url)
	with open(image_path, "rb") as image_file:
		ret = requests.post(url, data=data, files={"photo": image_file})
		if Logging: print(ret.json)
	return ret.json()

def send_TGBadge(Badge, BadgeLvl,Caption=""):
	print(Badge)
	print(BadgeLvl)
	filename = os.sep.join(["badges_webp", Badges[Badge]["File"]+"-"+BadgeLvlList[BadgeLvl]["File"]+".webp"])
	try:
		if Logging: print(filename)
		with open(filename) as image_file:
			print("Sending ..."+ filename)
			send_TGImage(filename,Caption) 
	except OSError as error:
		print ("Could not open/read file:", filename)
		print (error)
		filename = os.sep.join(["badges_webp", "Neutral-" +BadgeLvlList[BadgeLvl]["File"]+".png"])
		if Logging: print(filename)
		with open(filename) as image_file:
			print("Sending ..."+ filename)
			send_TGImage(filename,Caption) 			

def send_TGRecursionBadge(Badge, Caption=""):
	filename = os.sep.join(["badges_webp", Badges[Badge]["File"] + "-"+"recursion"+".png"])
	try:
		if Logging: print(filename)
		with open(filename) as image_file:
			print("Sending ..."+ filename)
			send_TGImage(filename,Caption) 
	except OSError as error:
		print ("Could not open/read file:", filename)
		print (error)
			
def send_Daily_stats(group,given_stattype,MaxAgentsShown,Timespan):
	global Logging
	if given_stattype == "":
		daily_stattype = get_daily_stattype()
	else:
		daily_stattype = given_stattype
	#daily_stattype = "lifetime_ap"
	if Logging : print(daily_stattype)
	ordered_dict_stats= get_ordered_dict_stats(group,daily_stattype,Timespan)
	#if Logging : print(json.dumps(ordered_dict_stats, indent = 4, sort_keys=False))
	
	agentlist= list(ordered_dict_stats.keys())
	x=0
	daily_message=toutput["T1"][language].format(emoji["trophy"],str(MaxAgentsShown),daily_stattype ,Badges[daily_stattype]["Name"],timespans[Timespan][language])
	for agent in agentlist:  
		x=x+1
		daily_message= daily_message + "" + ranking_emoji[x]+emoji[str(ordered_dict_stats[agent]["faction"])] + " <b>" + agent.ljust(20," ") + "</b>\t"+ locale.format_string('%d',ordered_dict_stats[agent][daily_stattype],1) +" \n"
		if x == MaxAgentsShown: 
			break
	if Logging : print(daily_message)
	send_TGMessage(daily_message,get_chat_id())

def send_WWC_stats(given_stattype):
	global Logging
	global MaxAgentsShown 
	MaxAgentsShown = 20
	if given_stattype == "":
		daily_stattype = get_daily_stattype()
	else:
		daily_stattype = given_stattype
	#daily_stattype = "lifetime_ap"
	if Logging : print(daily_stattype)
	ordered_dict_stats= get_ordered_dict_stats(daily_stattype,"custom")
	#if Logging : print(json.dumps(ordered_dict_stats, indent = 4, sort_keys=False))
	agentlist= list(ordered_dict_stats.keys())
	x=0
	daily_message=emoji["trophy"]+"The <b>Top-"+str(MaxAgentsShown)+"</b>  "+daily_stattype + " ("+Badges[daily_stattype]["Name"]+") in the custom interval: \n"
	for agent in agentlist:  
		if Logging : print("agentname: "+agent)
		x=x+1
		daily_message= daily_message + "" + ranking_emoji[x]+emoji[str(ordered_dict_stats[agent]["faction"])] + " <b>" + agent.ljust(18," ") + "</b>\t"+ locale.format_string('%d',ordered_dict_stats[agent][daily_stattype],1) +" \n"
		if x == MaxAgentsShown: 
			break
	#if Logging : print(daily_message)
	send_TGMessage(daily_message,get_chat_id())
	
def check_LevelUp():
	global Logging
	filename = "last_levelstats_"+group+".json"
	new_stats = get_new_dict_stats(group,"all")
	try:
		with open(filename) as json_file:
			last_reference_stats = json.load(json_file)
	except OSError:
		print ("Could not open/read file:", filename)
		last_reference_stats=new_stats
	
	if Logging : print("Running...")
	last_agentlist = list(last_reference_stats.keys()) 
	for agent in last_agentlist:  	
		LevelUpMessage = ""
		if new_stats[agent]["level"] > last_reference_stats[agent]["level"]:
			if Logging : print (agent)
			LevelUpMessage = toutput["T2"][language].format(emoji["thumbUp"],str(agent),str(new_stats[agent]["level"]))
			if Logging : print(LevelUpMessage)
			send_TGMessage(LevelUpMessage,get_chat_id())
			levelup_file = os.sep.join(["badges_webp", "levelup{}.jpg".format(str(new_stats[agent]["level"]))])
			send_TGImage(levelup_file)
	with open(filename, "w") as outfile:
		json.dump(new_stats, outfile, ensure_ascii=False, indent=4)

def check_Badges():
	global Logging
	filename = "last_badgestats_"+group+".json"
	
	new_stats = get_new_dict_stats(group,"all")
	try:
		with open(filename) as json_file:
			last_reference_stats = json.load(json_file)
	except OSError:
		print ("Could not open/read file:", filename)
		with open(filename, "w") as outfile:
			json.dump(new_stats, outfile, ensure_ascii=False, indent=4)
		exit(0)

	if Logging : print("Running...")
	last_agentlist = list(last_reference_stats.keys()) 
	for agent in last_agentlist: 
		for Badge in Badges:
			LevelUpMessage = ""
			#print (Badge)
			for BadgeLvl in BadgeLvlList:
				if int(new_stats[agent][Badge]) >= int(Badges[Badge][BadgeLvl]) and int(last_reference_stats[agent][Badge]) < int(Badges[Badge][BadgeLvl]):
					if Logging : print ("Agent: "+agent + " BadgeLvl= " + BadgeLvl)
					LevelUpMessage = toutput["T3"][language].format(emoji["thumbUp"],str(agent),str(Badge), Badges[Badge]["Name"], str(BadgeLvl),emoji["thumbUp"])
					if Logging : print(LevelUpMessage)
					send_TGMessage(LevelUpMessage,get_chat_id())
					send_TGBadge(Badge,BadgeLvl, Badges[Badge]["Name"]+": "+str(Badges[Badge][BadgeLvl]))
			if int(int(last_reference_stats[agent][Badge])/int(Badges[Badge]["Black"])) >0 and int(int(new_stats[agent][Badge])/int(Badges[Badge]["Black"])) != int(int(last_reference_stats[agent][Badge])/int(Badges[Badge]["Black"])):
				if Logging : print (agent)
				LevelUpMessage = toutput["T4"][language].format(emoji["thumbUp"], str(agent), str(int(int(new_stats[agent][Badge])/int(Badges[Badge]["Black"]))),  str(Badge), Badges[Badge]["Name"])
				if Logging : print(LevelUpMessage)
				send_TGMessage(LevelUpMessage,get_chat_id())
				send_TGRecursionBadge(Badge, "")
	with open(filename, "w") as outfile:
		json.dump(new_stats, outfile, ensure_ascii=False, indent=4)

def check_wttr():
	global Logging	
	message =""
	Towns = ["Potsdam",
			"Berlin"]
	for Town in Towns:
		url = 'https://wttr.in/'+ Town +'?format=%l:+%t+%c+%C'
		wttr_json = get_url(url)
		message= message+ wttr_json + "\n"
	if Logging : print(message)
	send_TGMessage(message,get_chat_id())

def print_CLI_Help():
	print ('astats_bot.py -c <Function> -g <groupname> -s <stattype>')
	print ("    options:    -c --check  : Funktionstyp")
	print ("                -g --group  : Name of group as mentioned in secrets.py")
	print ("                -s --stattype: define a stattype you want to see,default= changing each day ")
	print ("                -m --MaxAgentsShown: Count of Agents in the List (default=5), ")
	print ("                -i --interval: Zeitraum [custom, week],default = week ")
	print ("                -l --language: language for output [DE, EN],default = DE ")
	print ("                -v --verbose: keine Statusanzeigen ")
	print ("                -t --Test   : Nur Testkommunikation mit dem Bot ")
	print ("     function : LevelUp ")
	print ("                DailyStats ")
	print ("                Badges ")
	print ("                wttr ")
	
def main():
	Check=""
	short_options = "hc:g:smilvt"
	long_options = ["help", "check=", "group=","stattype=", "MaxAgentsShown=","interval=","language=", "verbose", "Test"]
	global Logging
	global Testmodus
	global group
	global language
	MaxAgentsShown = 5
	Timespan = "week"
	given_stattype=""
	group = ""
	full_cmd_arguments = sys.argv
	argument_list = full_cmd_arguments[1:]
	try:
		arguments, values = getopt.getopt(argument_list,short_options,long_options)
	except getopt.GetoptError:
		print_CLI_Help()
		sys.exit(2)
	for current_argument, current_value in arguments:
		if Logging: print (current_argument+" : "+ current_value)
		if current_argument in ("-h", "--help"):
			print_CLI_Help()
			sys.exit()
		elif current_argument in ("-c","--check"):
			Check = current_value
		elif current_argument in ("-g", "--group"):
			group = current_value
		elif current_argument in ("-s", "--stattype"):
			given_stattype = current_value
		elif current_argument in ("-m", "--MaxAgentsShown"):
			if int(current_value)>0:
				MaxAgentsShown = int(current_value)
				if MaxAgentsShown>50:
					print ("MaxAgentsShown maximum is 50.")
					sys.exit(2)
			else:
				print("Parameter --MaxAgentsShown invalid")
				print_CLI_Help()
				sys.exit(2)
		elif current_argument in ("-i", "--interval"):
			if current_value in ["custom","week"]:
				Timespan = current_value
			else:
				print("Parameter --interval {} invalid".format(current_value))
				print_CLI_Help()
				sys.exit(2)
		elif current_argument in ("-l", "--language"):
			if current_value in ["DE","EN"]:
				language = current_value
			else:
				print("Parameter --language {} invalid".format(current_value))
				print_CLI_Help()
				sys.exit(2)
		elif current_argument in ("-v", "--verbose"):
			Logging = False
		elif current_argument in ("-t", "--Test"):
			Testmodus = True
		else:
			print_CLI_Help()
	group = checkgroup(group)
	
	if Check =="DailyStats":
		send_Daily_stats(group,given_stattype,MaxAgentsShown,Timespan)
	elif Check =="WWCStats":
		send_WWC_stats(given_stattype)
	elif Check == "LevelUp":
			check_LevelUp()
	elif Check == "Badges":
			check_Badges()
	elif Check == "wttr":
			check_wttr()
	else: 
		print ("'" + Check + "' not found")
	
	
if __name__ == '__main__':
  main()
  
  
  
  
  


