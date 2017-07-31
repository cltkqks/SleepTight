import json

sleepData = {
    'day' : 20170731,
    'sleeptime' : 0100,
    'sleeppattern' : 0,
    'start_end' : 1,
    'patterntime' : 90
}

jsonString = json.dumps(sleepData)

print(jsonString)
print(type(jsonString))

with open('20170731.json', 'w') as make_file:
    json.dump(sleepData, make_file, ensure_ascii=False)
