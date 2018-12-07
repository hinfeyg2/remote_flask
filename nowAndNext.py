import json
import time

# def nowAndNext():

currentTime = time.time()
numIncludedResults = 2

data_file = "result.json"
with open(data_file, 'r') as infile:
    data = json.load(infile)

for channel in data:
    count = 0
    for i in list(data[channel]['schedule']):
        if i['endTimeStamp'] - currentTime < 0:
            data[channel]['schedule'].remove(i)
        else:
            count = count + 1
            if count > numIncludedResults:
                data[channel]['schedule'].remove(i)


data
with open('nowAndNext.json', 'w') as fp:
    json.dump(data, fp)

