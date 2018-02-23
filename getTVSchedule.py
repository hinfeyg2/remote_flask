import requests
import datetime
import json

myChannels = {
  "RTE One": 101,
  "RTE2": 102,
  "TV3": 103,
  "TG4": 104,
  "3e": 105,
  "be3": 106,
  "RTE One +1": 107,
  "BBC 1": 108,
  "BBC 2": 109,
  "TV3+1": 110,
  "Channel 4": 111,
  "E4": 112,
  "E4+1": 113,
  "Sky One": 114,
  "Sky Two": 115,
  "BBC FOUR": 117,
  "More4": 118,
  "G.O.L.D.": 120,
  "TLC": 121,
  "Dave": 122,
  "Universal": 123,
  "Sky Living": 124,
  "Sky Living+1": 125,
  "FOX": 126,
  "Comedy": 127,
  "Comedy +1": 128,
  "Syfy": 129,
  "ITV3": 131,
  "ITV4": 132,
  "Pick": 133,
  "Comedy Extra": 134,
  "RTE One HD": 135,
  "RTE2 HD": 136,
  "TG4 HD": 137,
  "BBC1 HD": 139,
  "BBC TWO HD": 140,
  "Sky Arts": 141,
  "Channel 4 HD": 142,
  "Sky 1 HD": 143,
  "Sky Living HD": 144,
  "Sky Arts HD": 145,
  "E!": 147,
  "be3 HD": 148,
  "3e HD": 149,
  "TV3 HD": 150,
  "Alibi": 151,
  "More4+1": 152,
  "G.O.L.D. +1": 153,
  "Discovery Quest": 154,
  "Discovery Shed": 155,
  "Discovery Turbo": 156,
  "Challenge": 157,
  "Real Lives": 158,
  "Quest Red": 159,
  "Watch": 160,
  "Channel 4 + 1": 161,
  "E4 HD": 162,
  "FOX +1": 166,
  "More4 HD": 168,
  "Universal HD": 173,
  "FOX HD": 176,
  "Comedy HD": 177,
  "SyFy HD": 179,
  "RTE News Now": 200,
  "BBC News 24": 201,
  "Sky News": 202,
  "Euronews": 203,
  "CNBC Europe": 204,
  "CNN": 205,
  "BBC World": 206,
  "Oireachtas TV": 207,
  "Discovery": 208,
  "Disc Channel +1": 209,
  "Home & Health": 210,
  "Discovery Science": 211,
  "Discovery History": 212,
  "Animal Planet": 213,
  "DMAX": 214,
  "National Geographic": 215,
  "Nat Geo Wild": 216,
  "History Channel": 217,
  "Lifetime": 218,
  "Discovery HD": 219,
  "History HD": 220,
  "National Geographic": 221,
  "Nat Geo Wild HD": 222,
  "Crime & Investigation": 225,
  "H2": 226,
  "Sky News HD": 232,
  "Bloomberg": 240,
  "Russia Today": 241,
  "Sky Comedy": 301,
  "Sky Action": 302,
  "Sky Family": 303,
  "Sky Horror": 304,
  "Sky Disney": 305,
  "Sky Select": 306,
  "Sky Greats": 307,
  "Sky Drama": 308,
  "Sky Crime and Thriller": 309,
  "Sky Hits": 318,
  "Sky Premiere": 320,
  "Sky Premiere +1": 321,
  "Film Four": 323,
  "FILM FOUR +1": 324,
  "TCM": 327,
  "TCM +1": 328,
  "True Movies 1": 329,
  "Sky Sports Mix": 400,
  "Sky Sports Main Event": 401,
  "Sky Sports Cricket": 402,
  "Sky Sports Action": 403,
  "Sky Sports Golf": 404,
  "Sky Sports Premiere": 405,
  "Sky Sports Arena": 406,
  "Sky Sports Football": 407,
  "Sky Sports News": 408
}

myNumbers = list(myChannels.values())

channels = requests.get('https://web-api-pepper.horizon.tv/oesp/v2/IE/eng/web/channels?byLocationId=6651943228&includeInvisible=true&personalised=false').json()
channelDict = {}

for i in channels['channels']:
	if i['channelNumber'] in myNumbers:
		channelDict[i['stationSchedules'][0]['station']['id']] = {"name": i['stationSchedules'][0]['station']['title'], "number": i['channelNumber'], "image": i['stationSchedules'][0]['station']['images'][2]['url'].split("?w=")[0].split("/")[-1], "schedule": []}


date = datetime.datetime.today().strftime('%Y%m%d')

for p in range(1, 5):

	listings = requests.get("https://web-api-pepper.horizon.tv/oesp/v2/IE/eng/web/programschedules/%s/%s" % (date, p)).json()

	for i in listings['entries']:
		if len(i['l']) > 1 and i['o'] in channelDict and channelDict[i['o']]['number'] in myNumbers:

			for j in i['l']:

				if 't' in j:

					channelDict[i['o']]["schedule"].append({"title": j['t'], "startTime": datetime.datetime.fromtimestamp(int(str(j['s'])[:10])).strftime('%Y-%m-%d %H:%M:%S'), "endTime": datetime.datetime.fromtimestamp(int(str(j['e'])[:10])).strftime('%Y-%m-%d %H:%M:%S')})


for i in channelDict:
	
	l = channelDict[i]['schedule']

	seen = set()
	new_l = []
	for d in l:
	    t = tuple(d.items())
	    if t not in seen:
	        seen.add(t)
	        new_l.append(d)

	channelDict[i]['schedule'] = new_l


with open('result.json', 'w') as fp:
    json.dump(channelDict, fp)

