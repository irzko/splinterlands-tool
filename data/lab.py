import json, os
os.system('cls')

with open('data/history.json') as f:
    history = json.load(f)
    f.close()

for i in history["99"]:
    h = i["enemy_team"]["team"]