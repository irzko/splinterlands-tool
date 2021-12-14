from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from bs4 import BeautifulSoup
import json, os, time, requests, multiprocessing, random, re

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
            self.cardFile = File('data/playable.json')
            self.ownerCards = self.cardFile.rJSon()
        except:
            self.ownerCards = []

    def getNames(self, list_card):
        list_of_card_names = []
        for card in list_card:
            list_of_card_names.append(card['name'])
        return list_of_card_names


    def sortNames(self, list_card):
        return sorted(self.getNames(list_card))

    def showNames(self, list_card='owner'):
        if list_card == 'owner':
            typeOfListCard = self.ownerCards
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
        sortedNameCardList = self.sortNames(self.ownerCards)
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
                        self.ownerCards.append(card)
                        card_added = listName[n]
                        self.cardFile.wJSon(self.ownerCards)
                        break
            else:
                print('Thông tin không hợp lệ!')
                time.sleep(1)

    def delete(self):
        n = None
        cardDeleted = None
        while (n != 'Q'):
            listName = self.sortNames(self.ownerCards)
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
            if n.isdigit() and int(n) - 1 < len(self.ownerCards) and int(n) - 1 >= 0:
                n = int(n) - 1
                for card in range(len(self.ownerCards)):
                    if self.ownerCards[card]['name'] == listName[n]:
                        cardDeleted = listName[n]
                        del self.ownerCards[card]
                        break
                self.cardFile.wJSon(self.ownerCards)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)


    def details(self, number):
        os.system('cls')
        listName = self.sortNames(self.ownerCards)
        card = {}
        for i in self.ownerCards:
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
            elif n.isdigit() and int(n) - 1 < len(self.ownerCards) and int(n) - 1 >= 0:
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
            self.accountFile = File('data/account.json')
            self.account = self.accountFile.rJSon()
        except:
            self.account = []

    def show(self):
        if len(self.account) > 0:
            number = 1
            for i in self.account:
                print(f'{number}. {i["mail"]}')
                number += 1

    def add(self):
        os.system('cls')
        email = input('Email: ')
        password = input('Mật khẩu: ')
        account = Account(email, password)
        self.account.append(account.toDict())
        self.accountFile.wJSon(self.account)

    def delete(self):
        select = None
        while (select != 'B'):
            os.system('cls')
            print('DANH SÁCH TÀI KHOẢN\n')
            if len(self.account) > 0:
                j = 1
                for i in self.account:
                    print(f'{j}. {i["mail"]}')
                    j += 1
            else:
                print("Không có tài khoản nào!")
            print('\n[B] Trở lại')
            select = input('>> Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(self.account) and int(select) - 1 >= 0):
                self.account.pop(int(select) - 1)
                self.accountFile.wJSon(self.account)
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
            if len(self.account) > 0:
                j = 1
                for i in self.account:
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
            self.historyFile = File('data/history.json')
            self.history = self.historyFile.rJSon()
        except:
            self.history = {}

    def analys(self, mana):
        select = ''
        while (select != 'Q'):
            os.system('cls')
            self.topCard(mana)
            print("Chọn đội hình để xem chi tiết\n")
            j = 1
            for i in self.teams[mana]:
                print(f'[{j}] {", ".join(i)}')
                j += 1
            print('\n[Q] Thoát')
            select = input('>> Chọn đội hình: ').upper()
            if select.isdigit() and (int(select) - 1 >= 0 and int(select) - 1 < len(self.teams[mana])):
                select = int(select) - 1
                team = self.teams[mana][select]
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
            won = 0 
            lost = 0
            drawn = 0
            match = 0
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
            self.historyFile.wJSon(self.history)

class Team:
    def __init__(self):
        try:
            self.teamFile = File('data/team.json')
            self.teams = self.teamFile.rJSon()
        except:
            self.teams = {}
        self.history = History()
        self.card = Card()
        self.manaList = (
        '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
        '30', '99')

    def inputMana(self):
        mana = input('>> Mana: ')
        while (not mana.isdigit() or not (mana in self.manaList)):
            os.system('cls')
            print('Số mana không hợp lệ, thử lại!')
            print(f'Những mana hợp lệ: {", ".join(self.manaList)}\n')
            mana = input('>> Mana: ')
        return mana

    def currentMana(self, team_adding):
        currentMana = 0
        for i in team_adding:
            currentMana += self.card.getMana(i)
        return currentMana

    def teamSorted(self, list_team):
        team_sorted = {}
        for key in sorted(list_team.keys()):
            team_sorted[key] = list_team.get(key)
        return team_sorted

    def add(self):
        os.system('cls')
        mana = self.inputMana()
        select = ''
        teamAdding = []
        listName = self.card.sortNames(self.card.ownerCards)
        while (select != 'Q'):
            os.system('cls')
            self.card.showNames()
            print("\n")
            print(f'Mana: [{self.currentMana(teamAdding)}/{mana}]')
            print('\n'.join(teamAdding))
            print(
                "\n[S] Lưu    |    [C] Xoá bỏ tất cả    |    [M] Sửa mana    |    [D] Xoá thẻ bài vừa chọn    |    [Q] Thoát\n")
            select = input('>> Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(self.card.ownerCards) and int(select) - 1 >= 0):
                select = int(select) - 1
                teamAdding.append(listName[select])
            elif (select == 'S'):
                if (len(teamAdding) == 0):
                    print('Đội hình trống! Thử lại.')
                    select = ''
                    time.sleep(1)
                else:
                    if (self.teams.get(mana) != None):
                        self.teams[mana].append(teamAdding)
                    else:
                        self.teams[mana] = []
                        self.teams[mana].append(teamAdding)
                    self.teams = self.teamSorted(self.teams)
                    self.teamFile.wJSon(self.teams)
                    print('Đội hình đã được lưu!')
                    time.sleep(1)
                    teamAdding = []
            elif (select == 'C'):
                teamAdding.clear()
            elif (select == 'M'):
                os.system('cls')
                mana = self.inputMana()
            elif (select == 'D'):
                if len(teamAdding) > 0: teamAdding.pop(-1)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)

    def delete(self):
        os.system('cls')
        mana = lt = None
        while True:
            os.system('cls')
            mana = input('>> Nhập mana: ')
            lt = self.teams.get(mana)
            if lt == None:
                print('Không tìm thấy đội hình! Thử lại.')
                time.sleep(1)
            else:
                break
        os.system('cls')
        td = ''
        while True:
            os.system('cls')
            print(f'Mana: {mana}')
            print('Chọn một đội hình để xoá\n')
            for i in range(len(lt)):
                print(f'{i + 1}. {lt[i]}')
            td = input('>> Chọn: ')
            if (td <= '0' or td > str(len(lt))) and td.isalpha():
                print("Cú pháp không hợp lệ! Thử lại.")
                time.sleep(1)
            else:
                break
        os.system('cls')
        st = lt[int(td) - 1]
        acpt = ''
        while True:
            os.system('cls')
            acpt = input(f'Đội hình đã được chọn:\n{st}\n\nBạn có muốn xoá đội hình này? [Y/N]\n>> Chọn: ').upper()
            if acpt != 'Y' and acpt != 'N':
                print("Cú pháp không hợp lệ! Thử lại.")
            else:
                break
        if acpt == 'Y':
            self.teams[mana].pop(int(td) - 1)
            if len(self.teams[mana]) == 0: self.teams.pop(mana)
            self.teamFile.wJSon(self.teams)
            os.system('cls')
            print('Đã xoá thành công!')
            time.sleep(1)

    def stringList(self, _list):
        strlst = '["'
        strlst += '", "'.join(_list)
        strlst += '"]'
        return strlst

    def randomTeam(self, team):
        if len(team) == 1:
            return team[0]
        else:
            a = random.randrange(0, len(team))
            return team[a]

    def teamSelector(self, mana):
        mana = str(mana)
        team = self.teams.get(mana)
        teamSelected = ''
        if team is not None:
            teamSelected = self.randomTeam(team)
        else:
            try:
                teamDefault = File('data/team_default.json')
                team = teamDefault.rJSon()
            except:
                response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/team_default.json')
                team = json.loads(response.text)
                teamDefault.wJSon(team_def)
            teamSelected = team[mana][0]
        return self.stringList(teamSelected)

    def checkTeam(self):
        if len(self.teams) <= 20:
            teamNA = []
            for mana in self.manaList:
                if self.teams.get(mana) == None:
                    teamNA.append(mana)
            print('-' * 120)
            print('CHÚ Ý!')
            print('''Bạn chưa thêm đủ đội hình, vì thế những đội hình nào chưa có chúng tôi sẽ chọn đội hình mặc định để chiến đấu, và
kết quả có thể sẽ không như mong muốn!''')
            print('\nNhững đội hình có mana sau chưa được thêm:')
            print(", ".join(teamNA))
            print('-' * 120)

    def numOfCard(self):
        listCard = self.card.sortListOfName(self.card.allCardList)
        numCard = {}
        for i in range(1, len(listCard) + 1):
            numCard[listCame[i - 1]] = str(i)
        return numCard

    def topCard(self, mana):
        if len(self.history) > 0:
            print(f"THẺ BÀI ĐƯỢC ĐỐI THỦ CHỌN NHIỀU NHẤT VỚI {mana} MANA\n")
            team = {}
            for i in self.history[mana]:
                enemyTeam = i['enemy_team']['team']
                for j in enemyTeam:
                    if team.get(j) == None:
                        team[j] = 1
                    else:
                        team[j] += 1
            items_sorted = sorted(team.items(), reverse=True, key=lambda x: x[1])
            print(f'{"Tên thẻ bài":>12}{"Số lần chọn":>16}\n')
            j = 1
            for i in items_sorted:
                print(f'{j:>2} {i[0]:<20} {i[1]:>2}')
                j += 1
            print(f"{'_' * 100}\n")

    def show(self):
        select = ''
        while (select != 'Q'):
            os.system('cls')
            won = lost = drawn = match = 0
            if len(self.teams) > 0:
                for mana in self.teams:
                    print('_' * 120)
                    print(f'\n MANA {mana}:')
                    k = 1
                    for i in self.teams[mana]:
                        kda = self.history.kda(self.teamFile, i)
                        winRate = 0.0
                        if kda[3] != 0: winRate = int(kda[0]) / int(kda[3]) * 100
                        team = ", ".join(i)
                        print(f'{k}. {team}')
                        won += int(kda[0])
                        lost += int(kda[1])
                        drawn += int(kda[2])
                        match += int(kda[3])
                        print(
                            f'   --> Thắng: {kda[0]} / Thua: {kda[1]} / Hoà: {kda[2]} / {kda[3]} trận | Tỉ lệ thắng {round(winRate, 2)}%')
                        k += 1
                        print()
            print('_' * 120)
            sumOfWinRate = 0.0
            if match != 0: sumOfWinRate = won / match * 100
            print()
            self.checkTeam()
            print(f'\n>> Tổng cộng: {match} trận đấu  |   Tỉ lệ thắng {round(sumOfWinRate, 2)}%\n')
            print('\nNhập số mana để xem chi tiết, hoặc:')
            print('[A] Thêm    |    [D] Xoá    |    [Q] Thoát')
            select = input('\n>> Chọn: ').upper()
            if select == 'A':
                self.add()
            elif select == 'D':
                self.delete()
            elif select.isdigit() and (self.teams.get(select) != None):
                self.history.analys(select)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)

class Battle:
    def __init__(self):
        self.account = AccountList()
        self.history = History()
        self.team = Team()

    def initDriver(self):
        options = webdriver.ChromeOptions()
        #chrome_options.add_argument("user-data-dir="+filePath)
        driver = webdriver.Chrome('chromedriver', options = options)
        return driver

    def status(self, stt, mail):
        named_tuple = time.localtime()
        time_string = time.strftime("%H:%M:%S", named_tuple)
        print(f'[{time_string}] [{mail}] {stt}')

    def start(self, match, acc):
        self.status('Đang khởi động trình duyệt...', acc['mail'])
        driver = self.initDriver()
        wait = WebDriverWait(driver, 60)
        driver.get('https://splinterlands.com/?p=battle_history')
        driver.find_element(By.ID, 'log_in_button').click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body")))
        time.sleep(1)
        driver.find_element(By.ID, 'email').send_keys(acc['mail'])
        driver.find_element(By.ID, 'password').send_keys(acc['pwd'])
        driver.find_element(By.CSS_SELECTOR, 'form.form-horizontal:nth-child(2) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)').click()
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[2]/div[2]/div')))
            driver.execute_script("document.getElementsByClassName('close')[0].click();")
        except:
            pass
        driver.get('https://splinterlands.com/?p=battle_history')
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div[1]")))
            driver.execute_script("document.getElementsByClassName('modal-close-new')[0].click();")
        except:
            pass
        team = []
        mana = 0
        driver.execute_script(
            "var roww = document.getElementsByClassName('row')[1].innerHTML;var reg = /HOW TO PLAY|PRACTICE|CHALLENGE|RANKED/;var resultt = roww.match(reg);while(resultt != 'RANKED'){document.getElementsByClassName('slider_btn')[1].click();roww = document.getElementsByClassName('row')[1].innerHTML;resultt = roww.match(reg);};")

        def checkPoint_0():
            time.sleep(1)
            driver.execute_script("document.getElementsByClassName('big_category_btn red')[0].click();")
            self.status('Đang tìm đối thủ...', acc['mail'])

        def checkPoint_1():
            nonlocal team
            nonlocal mana
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
            time.sleep(1)
            mana = driver.find_element_by_css_selector(
                'div.col-md-3:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
            team = self.team.teamSelector(mana)
            self.status('Đang khởi tạo đội hình...', acc['mail'])
            driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")

        def checkPoint_2():
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
            self.status('Đang chọn thẻ bài...', acc['mail'])
            time.sleep(7)
            driver.execute_script(
                "var team = " + team + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")

        def checkPoint_3():
            self.status('Đang chờ đối thủ...', acc['mail'])
            WebDriverWait(driver, 150).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
            driver.execute_script("document.getElementsByClassName('btn-battle')[0].click()")
            self.status('Đang bắt đầu trận...', acc['mail'])
            time.sleep(3.5)
            self.status('Đang bỏ qua...', acc['mail'])
            driver.execute_script("document.getElementsByClassName('btn-battle')[1].click()")

        def checkPoint_4():
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
            driver.execute_script("document.getElementsByClassName('btn btn--done')[0].click();")
            self.status('Kết thúc trận đấu', acc['mail'])

        def checkPage():
            try:
                WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="play_now"]/div/div/div/div/button')))
                return -1
            except:
                pass
            try:
                WebDriverWait(driver, 1.5).until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
                return 0
            except:
                pass
            try:
                WebDriverWait(driver, 1.5).until(EC.visibility_of_element_located(
                    (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
                return 1
            except:
                pass
            try:
                WebDriverWait(driver, 1.5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
                return 2
            except:
                pass
            try:
                WebDriverWait(driver, 1.5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
                return 3
            except:
                pass
            try:
                WebDriverWait(driver, 1.5).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
                return 4
            except:
                pass
            return -2

        def isCheckPoint_0():
            try:
                checkPoint_0()
                isCheckPoint_1()
                return 0
            except:
                return -1

        def isCheckPoint_1():
            try:
                checkPoint_1()
                isCheckPoint_2()
                return 0
            except:
                return -1

        def isCheckPoint_2():
            try:
                checkPoint_2()
                isCheckPoint_3()
                return 0
            except:
                return -1

        def isCheckPoint_3():
            try:
                checkPoint_3()
                isCheckPoint_4()
                return 0
            except:
                return -1

        def isCheckPoint_4():
            try:
                checkPoint_4()
                return 0
            except:
                return -1

        def sl_group(x):
            c = -1
            if x == -1:
                driver.get('https://splinterlands.com/?p=battle_history')
                isCheckPoint_0()
            elif x == 0:
                c = isCheckPoint_0()
            elif x == 1:
                c = isCheckPoint_1()
            elif x == 2:
                c = isCheckPoint_2()
            elif x == 3:
                c = isCheckPoint_3()
            elif x == 3:
                c = isCheckPoint_4()
            return c

        check_point = clone_i = 0
        for i in range(int(match)):
            clone_i = i + 1
            self.status(f'Bắt đầu trận thứ [{i + 1}/{match}]', acc['mail'])
            wait.until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
            vf = i + 1
            if vf % 5 == 0:
                time.sleep(3)
                try:
                    self.status('Đang lưu lịch sử trận đấu...', acc['mail'])
                    self.history.writeHistory(driver, 20)
                    self.status('Xong', acc['mail'])
                except Exception as e:
                    self.status('Lỗi lưu lịch sử:' + e, acc['mail'])
                finally:
                    check_point = vf
            try:
                isCheckPoint_0()
            except:
                q = -2
                while (q != 0):
                    driver.refresh()
                    vt = checkPage()
                    if vt != -2: q = sl_group(vt)
        time.sleep(3)
        times_when_smaller_20 = clone_i - check_point
        if times_when_smaller_20 > 0:
            try:
                self.status('Đang lưu lịch sử trận đấu...', acc['mail'])
                self.history.writeHistory(driver, times_when_smaller_20)
                self.status('Xong', acc['mail'])
            except:
                self.status('Lỗi lưu lịch sử', acc['mail'])
            finally:
                driver.quit()
        return 'Q'

    def multiBattle(self):
        accounts_list = []
        if len(self.account.account) > 0:
            select = ''
            while (select != 'Q'):
                os.system('cls')
                self.team.checkTeam()
                print("CHỌN TÀI KHOẢN")
                print(f'\nĐã chọn {len(accounts_list)} tài khoản')
                if len(accounts_list) > 0:
                    t = 1
                    for account in accounts_list:
                        print(f"{t}. {account['mail']}")
                        t += 1
                print('\n\n')
                print('_' * 30)
                if len(self.account.account) >= 0:
                    j = 1
                    for k in self.account.account:
                        print(f'[{j}] {k["mail"]}')
                        j += 1
                    print('\n[S] Bắt đầu    |    [C] Xoá lựa chọn trước đó    |    [Q] Thoát')
                    select = input('>> Chọn: ').upper()
                    if select.isdigit() and int(select) - 1 < len(self.account.account) and int(select) - 1 >= 0:
                        select = int(select)
                        select -= j
                        accounts_list.append(self.account.account[select])
                        self.account.account.pop(select)
                    elif select == 'S' and len(accounts_list) > 0:
                        os.system('cls')
                        match = input('Số trận đấu: ')
                        while (not (match.isdigit() and int(match) > 0)):
                            os.system('cls')
                            print('Vui lòng nhập một số!')
                            match = input('Số trận đấu: ')
                        os.system('cls')
                        if len(accounts_list) == 1:
                            self.start(match, accounts_list[0])
                        else:
                            try:
                                pross = {}
                                for i in range(len(accounts_list)):
                                    keys = 'p' + str(i + 1)
                                    pross[keys] = multiprocessing.Process(target=self.start, args=(match, acc[i]))
                                for b in pross:
                                    pross[b].start()
                                response = requests.get(
                                    'https://raw.githubusercontent.com/tmkha/Splint/main/splint.py')
                                if response:
                                    splib = OpenFile().writeTextFile(response.text)
                                for k in pross:
                                    pross[k].join()
                            finally:
                                os.remove('splib.py')
                        return 'Q'
                    elif select == 'S' and len(acc) == 0:
                        print('Vui lòng chọn ít nhất một tài khoản!')
                        time.sleep(1)
                    elif select == 'C' and len(accounts_list) > 0:
                        all_acc.append(accounts_list[-1])
                        acc.pop(-1)
                    elif select != 'Q':
                        print('Cú pháp không hợp lệ!')
                        time.sleep(1)
        else:
            m = ''
            while (m != 'Q'):
                os.system('cls')
                print("CHỌN TÀI KHOẢN")
                print("\nKhông có tài khoản nào, vui lòng thêm tài khoản!")
                print('\n[Q] Thoát')
                m = input('>> Chọn: ').upper()
                if m != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)
        return 'Q'

class Launcher:

    def __init__(self):
        self.logo = '''
        \t\t\t\t\t  ██████  ██▓███   ██▓     ██▓ ▄▄▄▄   
        \t\t\t\t\t▒██    ▒ ▓██░  ██▒▓██▒    ▓██▒▓█████▄ 
        \t\t\t\t\t░ ▓██▄   ▓██░ ██▓▒▒██░    ▒██▒▒██▒ ▄██
        \t\t\t\t\t  ▒   ██▒▒██▄█▓▒ ▒▒██░    ░██░▒██░█▀  
        \t\t\t\t\t▒██████▒▒▒██▒ ░  ░░██████▒░██░░▓█  ▀█▓
        \t\t\t\t\t▒ ▒▓▒ ▒ ░▒▓▒░ ░  ░░ ▒░▓  ░░▓  ░▒▓███▀▒
        \t\t\t\t\t░ ░▒  ░ ░░▒ ░     ░ ░ ▒  ░ ▒ ░▒░▒   ░ 
        \t\t\t\t\t░  ░  ░  ░░         ░ ░    ▒ ░ ░    ░ 
        \t\t\t\t\t      ░               ░  ░ ░   ░      
        \t\t\t\t\t                By tmkha            ░ 
        '''
        self.keyFile = File('data/key')
        self.versionFile = File('data/version')
        self.updateFile = File('update.py')

    def menu(self):
        os.system('cls')
        print(self.logo)
        print(f"\t\t\t\t\t\t     Bản dựng {self.version()}")
        print('\n1: Vào game\n2: Đội hình\n3: Tài khoản\n4: Thẻ bài\n5: Phản hồi\n\n[Q] Thoát')
        select = input('\n>> Chọn: ').upper()
        list_op = ['1', '2', '3', '4', '5', 'Q']
        while (not btn(select, list_op)):
            os.system('cls')
            print(self.logo)
            print(f"\t\t\t\t\t\t     Bản dựng {self.version()}")
            print('\n1: Vào game\n2: Đội hình\n3: Tài khoản\n4: Thẻ bài\n5: Phản hồi\n\n[Q] Thoát')
            print("Cú pháp không hợp lệ! Thử lại.")
            select = input('\n>> Chọn: ').upper()
        return select

    def shutDown(self, mess):
        for i in range(3,0,-1):
            os.system('cls')
            print(mess)
            print(f'Ứng dụng sẽ đóng trong {i}')
            time.sleep(1)

    def btn(self, x,li):
        if (x.isalpha()): x = x.upper()
        check = False
        for i in li:
            if x == i:
                check = True
                break   
        return check

    def check_key(self, key):
        response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/key')
        lskey = response.text.split()
        if dec_2(key) in lskey: return True
        else: return False

    def start(self):
        try:
            with open('data/key', mode="r", encoding="utf-8") as f:
                key = f.read()
                f.close()
        except:
            key = ''
        while(not self.check_key(key)):
            os.system('cls')
            if key == '':
                key = dec_1(input('Nhập mã khoá: '))
                if self.check_key(key):
                    self.keyFile.wText(key)
                else:
                    key = ''
                    print('Mã khoá này không có sẵn!')
                    time.sleep(1)
            else:
                if self.check_key(key):
                    d_src()
                else:
                    print('Rất tiếc, mã khoá đã hết hạn!')
                    key = dec_1(input('Nhập mã khoá mới: '))
                    if self.check_key(key):
                        self.keyFile.wText(key)
                    else:
                        print('Mã khoá này không có sẵn!')
                        time.sleep(1)

    def checkVer(self, old_ver, new_ver):
        for i in range(3):
            if int(old_ver[i]) < int(new_ver[i]):
                return True
                break
            elif int(old_ver[i]) == int(new_ver[i]):
                continue
            else:
                return False
                break
        return False

    def version(self):
        try:
            with open('data/version', mode='r') as f:
                version = f.read()
                f.close
        except:
            response = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/data/version')
            version = response.text.strip()
            self.versionFile.wText(version)
        return version	


    def update(self):
        ver = list(self.version())
        get_version = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/data/version')
        new_ver = list(get_version.text.strip())
        if self.checkVer(ver, new_ver):
            get_update = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/update.py')
            self.updateFile.wText(get_update.text)
            from update import update_lib
            update_lib()
            self.versionFile.rText(new_ver)
            try:
                os.remove('update.py')
            except:
                pass

    def feedback(self):
        print('Mô tả nội dung phản hồi')
        print('[Q] Thoát\n')
        content = input('>> ')
        if content.upper() == 'Q': return 'Q'
        else:
            payload = {'notenumber': 'bp574p9j', 'name': 'Quess', 'content': content}
            os.system('cls')
            print('Đang gửi phản hồi...')
            requests.post('https://anotepad.com/note/addcomment', data=payload)
            os.system('cls')
            print('Đã gửi phản hồi của bạn!')
            time.sleep(2)
            return 'Q'
        

    def main(self):
        #os.remove('splint.py')
        self.update()
        self.start()
        select = self.menu()
        while (select != 'Q'):
            os.system('cls')
            if (select == '1'):
                n = multiBattle()
                if (n == 'Q'): select = self.menu()
            elif (select == '2'):
                n = viewTeam()
                if (n == 'Q'): select = self.menu()
                elif (n== 'R'): select == '3'
            elif (select == '3'):
                n = account_manage()
                if (n == 'Q'): select = self.menu()
            elif (select == '4'):
                n = Card().showCard()
                if (n == 'Q'): select = self.menu()
            elif (select == '5'):
                n = feedback()
                if (n == 'Q'): select = self.menu()
        os.system('cls')

