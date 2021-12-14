import requests, json, random
from bs4 import BeautifulSoup


# with open('source.html', encoding='utf-8') as f:
# 	soup = BeautifulSoup(f, 'html.parser')

# card_name = soup.find_all(class_="card-name-name")
# c = []
# for i in card_name:
# 	c.append(i.text)

# response = requests.get('https://api2.splinterlands.com/cards/get_details?')
# full = json.loads(response.text)
# k = []
# for i in c:
# 	for j in full:
# 		if i == j["name"]:
# 			k.append(j)
# 			break
# with open('t.json', 'w') as f:
# 	json.dump(k, f, indent=4)


# response = requests.get('https://api2.splinterlands.com/battle/history2?player=initiate_726597')

# a = json.loads(response.text)


# bt = a['battles'][2]


# #v = bt.values()
# t = bt['details']['team2']['monsters'][0]['card_detail_id']

# print(t)
# '''
# for i in t:
# 	print(f'{i} : {t[i]}')
# '''

print(random.randrange(0,3))