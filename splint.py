from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
import json, os, time, requests, multiprocessing, random

class File:
    def __init__(self, path):
        self.path = path

    def wText(self, content):
        with open(self.path, 'w') as file:
            file.write(content)
            file.close()

    def wJSon(self, content):
        with open(self.path, 'w') as file:
            json.dump(content, file, indent=4)
            file.close()

    def rText(self):
        with open(self.path) as file:
            content = file.read()
            file.close()
        return content

    def rJSon(self):
        with open(self.path) as file:
            content = json.load(file)
            file.close()
        return content

class Card:
    def __init__(self):
        try:
            self.allCard = File('data/card_details.json')
            self.allCardList = self.allCard.rJSon()
            print(len(self.allCardList))
        except:
            print('Đang tải thẻ bài...')
            response = requests.get('https://api2.splinterlands.com/cards/get_details?')
            self.allCardList = json.loads(response.text)
            self.allCard.wJSon(self.allCardList)
            os.system('cls')

        try:
            self.ownerCard = File('data/card_owned.json')
            self.ownerCardList = self.ownerCard.rJSon()
        except:
            self.ownerCardList = []

    def getNames(self, list_card):
        list_of_card_names = []
        for card in list_card:
            list_of_card_names.append(card['name'])
        return list_of_card_names

    def sortNames(self, list_card):
        return sorted(self.getNames(list_card))

    def show(self, list_card='owner'):
        if list_card == 'owner':
            typeOfListCard = self.ownerCardList
            length = len(typeOfListCard)
        elif list_card == 'all':
            typeOfListCard = self.allCardList
            length = len(typeOfListCard)
        elif list_card == 'na':
            typeOfListCard = self.cardNotAvailable()
            length = len(typeOfListCard)
        listOfNames = self.sortNames(typeOfListCard)
        numOfRow = length // 4
        numOfRedunNames = length % 4
        columnName = listIndex = listOfRedunNames = []
        i = 1
        a = 0
        b = numOfRow
        while (i <= 3):
            columnName.append(listOfNames[a:b])
            if numOfRedunNames >= i:
                listOfRedunNames.append(listOfNames[b])
                b += 1
                listIndex.append(b)
            a = b
            b = b + numOfRow
            i += 1
        columnName.append(listOfNames[a:b])
        indexLastRow = ((1, 1, 1), (2, 2, 2), (2, 3, 3), (2, 3, 4))
        for i in range(numOfRow):
            index = indexLastRow[numOfRedunNames]
            print(f'{i + 1:>3} {columnName[0][i]:<23}{i + index[0] + numOfRow:>3} {columnName[1][i]:<23}{i + index[1] + numOfRow * 2:>3} {columnName[2][i]:<23}{i + index[2] + numOfRow * 3:>3} {columnName[3][i]:<23}')
        if numOfRedunNames != 0:
            for i in range(len(listOfRedunNames)):
                print(f'{listIndex[i]:>3} {listOfRedunNames[i]:<23}', end='')
        print()

    def cardNotAvailable(self):
        cardNA = []
        sortedNameCardList = self.sortNames(self.ownerCardList)
        for card in self.allCardList:
            if not (card['name'] in sortedNameCardList):
                cardNA.append(card)
        return cardNA

    '''
    def add(self):
        card_added = n = ''
        if not os.path.isfile():
            print('Đang tải thẻ bài...')
            response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/card_details.json')
            self.allCard.wText(response.text)
        while (n != 'Q'):
            os.system('cls')
            listName = self.sortListOfName(self.CardNotAvailable())
            cardNA = self.CardNotAvailable()
            self.showListOfNames('na')
            print('_' * 112)
            if card_added != '':
                print(f'Đã thêm "{card_added}"')
            else:
                print()
            print('Nhập số của thẻ mà bạn muốn thêm')
            print('[Q] Thoát\n')
            n = input('>> Chọn: ').upper()
            if n == 'Q':
                break
            elif (n.isdigit() and int(n) - 1 < len(listName) and int(n) - 1 >= 0):
                n = int(n) - 1
                for card in cardNA:
                    if card['name'] == listName[n]:
                        self.ownerCardList.append(card)
                        card_added = listName[n]
                        self.ownerCard.writeJSonFile(self.ownerCardList)
                        break
            else:
                print('Thông tin không hợp lệ!')
                time.sleep(1)

    def delete(self):
        n = cardDeleted = ''
        while (n != 'Q'):
            listName = self.sortListOfName(self.ownerCardList)
            os.system('cls')
            self.showListOfNames('owner')
            print('_' * 112)
            if cardDeleted != '':
                print(f'Đã xoá "{cardDeleted}"')
            else:
                print()
            print('Nhập số của thẻ mà bạn muốn xoá')
            print('[Q] Thoát\n')
            n = input('>> Chọn: ').upper()
            if n.isdigit() and int(n) - 1 < len(self.ownerCardList) and int(n) - 1 >= 0:
                n = int(n) - 1
                for card in range(len(self.ownerCardList)):
                    if self.ownerCardList[card]['name'] == listName[n]:
                        cardDeleted = listName[n]
                        del self.ownerCardList[card]
                        break
                self.ownerCard.writeJSonFile(self.ownerCardList)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)
    '''

    def details(self, number):
        os.system('cls')
        listName = self.sortListOfName(self.ownerCardList)
        card = {}
        for card in self.ownerCardList:
            if listName == card['name']:
                break
        print(f'{"ID:":<10}{card["id"]}')
        print(f'{"Name:":<10}{card["name"]}')
        print(f'{"Color:":<10}{card["type"]}')
        print(f'{"Sub type:":<10}{card["sub_type"]}')
        print(f'{"Rarity:":<10}{card["rarity"]}')
        print('_' * 25)
        print('STATS')
        print(f'{"Mana:":<10}{card["stats"]["mana"]}')
        print(f'{"Attack:":<10}{card["stats"]["attack"]}')
        print(f'{"Ranged:":<10}{card["stats"]["ranged"]}')
        print(f'{"Magic:":<10}{card["stats"]["magic"]}')
        print(f'{"Armor:":<10}{card["stats"]["armor"]}')
        print(f'{"Health:":<10}{card["stats"]["health"]}')
        print(f'{"Speed:":<10}{card["stats"]["speed"]}')
        print()
        os.system('pause')

    def getMana(self, card_name):
        for card in self.allCardList:
            if card_name == card['name']:
                try:
                    return card['stats']['mana'][0]
                except:
                    return card['stats']['mana']

    '''
    def show(self):
        n = ''
        while (n != 'Q'):
            os.system('cls')
            self.showListOfNames('owner')
            print('_' * 112)
            print('\nNhập số của thẻ để xem chi tiết')
            print('[A] Thêm    |    [D] Xoá    |    [Q]Thoát')
            n = input('>> Chọn: ').upper()
            if n.isalpha() and n == 'A':
                self.add()
            elif n.isalpha() and n == 'D':
                self.delete()
            elif n.isdigit() and int(n) - 1 < len(card) and int(n) - 1 >= 0:
                self.details(int(n) - 1)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)
        return 'Q'
    '''

p=Card()
p.show("all")