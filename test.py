import requests, json
from bs4 import BeautifulSoup


with open('source.html', encoding='utf-8') as f:
	soup = BeautifulSoup(f, 'html.parser')



a = soup.find_all(class_="card-name-name")
c=[]
for i in a:
	c.append(i.text)

response = requests.get('https://api2.splinterlands.com/cards/get_details?')
full = json.loads(response.text)


k = []

for i in c:
	for j in full:
		if i == j["name"]:
			k.append(j)
			break

with open('t.json', 'w') as f:
	json.dump(k, f, indent=4)


