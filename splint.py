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
        response = requests.get('https://api2.splinterlands.com/cards/get_details?')
        self.allCards = json.loads(response.text)
        try:
            self.ownerCard = File('data/playable.json')
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

    def showNames(self, list_card='owner'):
        if list_card == 'owner':
            typeOfListCard = self.ownerCardList
            length = len(typeOfListCard)
        elif list_card == 'all':
            typeOfListCard = self.allCards
            length = len(typeOfListCard)
        elif list_card == 'na':
            typeOfListCard = self.cardNotAvailable()
            length = len(typeOfListCard)
        listOfNames = self.sortNames(typeOfListCard)
        numOfRow = length // 4
        numOfRedunNames = length % 4
        columnName = [] 
        listIndex = []
        listOfRedunNames = []
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
            print(
                f'{i + 1:>3} {columnName[0][i]:<23}{i + index[0] + numOfRow:>3} {columnName[1][i]:<23}{i + index[1] + numOfRow * 2:>3} {columnName[2][i]:<23}{i + index[2] + numOfRow * 3:>3} {columnName[3][i]:<23}')

            
        if numOfRedunNames != 0:
            for i in range(len(listOfRedunNames)):
                print(f'{listIndex[i]:>3} {listOfRedunNames[i]:<23}', end='')
        print()


    def cardNotAvailable(self):
        cardNA = []
        sortedNameCardList = self.sortNames(self.ownerCardList)
        for card in self.allCards:
            if not (card['name'] in sortedNameCardList):
                cardNA.append(card)
        return cardNA


    def add(self):
        card_added = None
        n = None
        while (n != 'Q'):
            os.system('cls')
            listName = self.sortNames(self.cardNotAvailable())
            cardNA = self.cardNotAvailable()
            self.showNames('na')
            print('_' * 112)
            if card_added is not None:
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
                        self.ownerCard.wJSon(self.ownerCardList)
                        break
            else:
                print('Thông tin không hợp lệ!')
                time.sleep(1)

    def delete(self):
        n = None
        cardDeleted = None
        while (n != 'Q'):
            listName = self.sortNames(self.ownerCardList)
            os.system('cls')
            self.showNames('owner')
            print('_' * 112)
            if cardDeleted is not None:
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
                self.ownerCard.wJSon(self.ownerCardList)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)


    def details(self, number):
        os.system('cls')
        listName = self.sortNames(self.ownerCardList)
        card = {}
        for i in self.ownerCardList:
            if listName[number] == i['name']:
                card = i.copy()
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

    def show(self):
        n = ''
        while (n != 'Q'):
            os.system('cls')
            self.showNames('owner')
            print('_' * 112)
            print('\nNhập số của thẻ để xem chi tiết')
            print('[A] Thêm    |    [D] Xoá    |    [Q]Thoát')
            n = input('>> Chọn: ').upper()
            if n.isalpha() and n == 'A':
                self.add()
            elif n.isalpha() and n == 'D':
                self.delete()
            elif n.isdigit() and int(n) - 1 < len(self.ownerCardList) and int(n) - 1 >= 0:
                self.details(int(n) - 1)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)
        return 'Q'

class Account:
    def __init__(self, email, password):
        self.__email = email
        self.__password = password

    def toDict(self):
        return {'mail': self.__email, 'pwd': self.__password}

    def email(self):
        return self.__email

class AccountList:
    def __init__(self):
        try:
            self.account = File('data/account.json')
            self.accountList = self.account.rJSon()
        except:
            self.accountList = []

    def show(self):
        if len(self.accountList) > 0:
            number = 1
            for i in self.accountList:
                print(f'{number}. {i["mail"]}')
                number += 1

    def add(self):
        os.system('cls')
        email = input('Email: ')
        password = input('Mật khẩu: ')
        account = Account(email, password)
        self.accountList.append(account.toDict())
        self.account.wJSon(self.accountList)

    def delete(self):
        select = None
        while (select != 'B'):
            os.system('cls')
            print('DANH SÁCH TÀI KHOẢN\n')
            if len(self.accountList) > 0:
                j = 1
                for i in self.accountList:
                    print(f'{j}. {i["mail"]}')
                    j += 1
            else:
                print("Không có tài khoản nào!")
            print('\n[B] Trở lại')
            select = input('>> Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(self.accountList) and int(select) - 1 >= 0):
                self.accountList.pop(int(select) - 1)
                self.account.wJSon(self.accountList)
            elif select != 'B':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)
            else:
                select = 'B'

    def show(self):
        n = ''
        while (n != 'Q'):
            os.system('cls')
            print('DANH SÁCH TÀI KHOẢN\n')
            if len(self.accountList) > 0:
                j = 1
                for i in self.accountList:
                    print(f'{j}. {i["mail"]}')
                    j += 1
                print("\n[A] Thêm    |    [D] Xoá    |    [Q] Thoát")
                n = input('>> Chọn: ').upper()
                if n == 'A':
                    self.add()
                elif n == 'D':
                    self.delete()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)
            else:
                print("Không có tài khoản nào, vui lòng thêm tài khoản!")
                print("\n[A] Thêm    |    [Q] Thoát")
                n = input('>> Chọn: ').upper()
                if n == 'A':
                    self.add()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)


class History:
    def __init__(self):
        try:
            self.historyBattle = OpenFile('data/history.json')
            self.history = self.historyBattle.readJSonFile()
        except:
            self.history = {}

    def analys(self, mana):
        select = ''
        while (select != 'Q'):
            os.system('cls')
            self.topCard(mana)
            print("Chọn đội hình để xem chi tiết\n")
            j = 1
            for i in self.listOfTeams[mana]:
                print(f'[{j}] {", ".join(i)}')
                j += 1
            print('\n[Q] Thoát')
            select = input('>> Chọn đội hình: ').upper()
            if select.isdigit() and (int(select) - 1 >= 0 and int(select) - 1 < len(self.listOfTeams[mana])):
                select = int(select) - 1
                team = self.listOfTeams[mana][select]
                kda = self.kda(mana, team)
                os.system('cls')
                print(f'Team: {", ".join(team)}')
                print(f"\nTrong {kda[3]} trận:")
                print(f'    Thắng: {kda[0]}')
                print(f'    Thua: {kda[1]}')
                print(f'    Hoà: {kda[2]}')
                if len(self.history) > 0:
                    if kda[3] != 0:
                        print('\n\t\t\t\t\t\tLỊCH SỬ THUA\n')
                        for i in range(len(self.history[mana])):
                            if self.history[mana][i]['my_team']['team'] == team:
                                result = self.history[mana][i]['result']
                                if result[7:] == 'Lost':
                                    print('\n> [', end="")
                                    print(", ".join(self.history[mana][i]['enemy_team']['team']), end="")
                                    print(']')
                                    listNumCard = []
                                    listName = numOfCard()
                                    for k in self.history[mana][i]['enemy_team']['team']:
                                        listNumCard.append(str(listName.get(k)))
                                    num = ":".join(listNumCard)
                                    print(f'--> Số thứ tự [{num}]\n')
                                    print('-' * 120)
                else:
                    print('\n\t\t\t\t\t\tLỊCH SỬ THUA\n')
                    print('\t\t\t\t\t      Không có lịch sử')
                n = input('\n[B] Trở lại    |    [Q] Thoát\n>> Chọn: ').upper()
                while (n != 'B' and n != 'Q'):
                    os.system('cls')
                    print('Cú pháp không hợp lệ!')
                    n = input('\n[B] Trở lại    |    [Q] Thoát\n>> Chọn: ').upper()
                if n == 'Q': select = 'Q'
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)

    def kda(self, mana, team):
        if len(self.history) > 0:
            won = lost = drawn = match = 0
            if self.history.get(mana) != None:
                for i in range(len(self.history[mana])):
                    if self.history[mana][i]['my_team']['team'] == team:
                        if self.history[mana][i]['result'] == 'Battle Won': won += 1
                        if self.history[mana][i]['result'] == 'Battle Lost': lost += 1
                        if self.history[mana][i]['result'] == 'Drawn': drawn += 1
                match = won + lost + drawn
            return [won, lost, drawn, match]
        else:
            return [0, 0, 0, 0]

    def writeHistory(self, driver, times):
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rlt_soup = soup.find_all(class_="battle-log-entry")
        for n in range(times):
            btl_log = re.compile(r'\d+|\w+\s?\w*\s?\w*\s?\w*[^(\n)]').findall(rlt_soup[n].text)
            me = []
            enemy = []
            for i in range(3, len(btl_log)):
                if btl_log[i] != 'VS':
                    me.append(btl_log[i])
                else:
                    break
            en_name = ''
            en_rat = ''
            en_gui = ''
            for j in range(len(btl_log) - 3, -1, -1):
                if btl_log[j].isdigit():
                    en_name = btl_log[j + 1]
                    en_rat = btl_log[j]
                    en_gui = btl_log[j + 2]
                    for z in range(j + 3, len(btl_log) - 3):
                        enemy.append(btl_log[z])
                    break
            result = btl_log[len(me) + 4]
            mode = btl_log[-3]
            mana = btl_log[len(me) + 7]
            if mana == '0': mana = btl_log[len(me) + 9]
            if mana == 'DEC': mana = btl_log[len(me) + 10]
            my_team = {}
            my_team['name'] = btl_log[1]
            my_team['rating'] = btl_log[0]
            my_team['guid_name'] = btl_log[2]
            my_team['team'] = me
            enemy_team = {}
            enemy_team['name'] = en_name
            enemy_team['rating'] = en_rat
            enemy_team['guid_name'] = en_gui
            enemy_team['team'] = enemy
            result_ = result[:-3]
            if result[:-3] != "Battle Lost" and result[:-3] != "Battle Won": result_ = 'Drawn'
            match = {}
            match['mode'] = mode[:-4]
            match['result'] = result_
            match['my_team'] = my_team
            match['enemy_team'] = enemy_team
            if self.history.get(mana) == None:
                self.history[mana] = []
                self.history[mana].append(match)
            else:
                self.history[mana].append(match)
            self.historyBattle.writeJSonFile(self.history)