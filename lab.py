import json, os, requests
from splint import Card, History
os.system('cls')

response = requests.get('https://api2.splinterlands.com/battle/history2?player=initiate_975111')
history = json.loads(response.text)
match = {}
for i in range(5):
    mana_cap = history['battles'][i]['mana_cap']
    player_1 = history['battles'][i]['player_1']
    player_2 = history['battles'][i]['player_2']
    winner = history['battles'][i]['winner']
    result = None
    if winner == player_1:
        result = "Battle Won"
    elif winner == player_2:
        result = "Battle Lost"
    else:
        result = "Drawn"
    team1 = []
    team2 = []
    summoner = history['battles'][i]['details']['team1']['summoner']['card_detail_id']
    team1.append(Card.getNameById(summoner))
    monsters = history['battles'][i]['details']['team1']['monsters']
    for monster in monsters:
        team1.append(Card.getNameById(monster['card_detail_id']))
    summoner = history['battles'][i]['details']['team2']['summoner']['card_detail_id']
    team2.append(Card.getNameById(summoner))
    monsters = history['battles'][i]['details']['team2']['monsters']
    for monster in monsters:
        team2.append(Card.getNameById(monster['card_detail_id']))
    match = {'result': result, "team1": {"player": player_1, 'team': team1}, "team2": {"player": player_2, 'team': team2}}
    if History.history.get(mana_cap) == None:
                History.history[mana_cap] = []
                History.history[mana_cap].append(match)
    else:
        History.history[mana_cap].append(match)
    History.historyFile.wJSon(History.history)