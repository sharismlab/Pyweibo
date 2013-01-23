import json

f = file('a.json')

s = json.load(f)
print s
f.close()