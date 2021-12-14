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
    try:
        allCardsFile = File('data/allcards.json')
        allCards = allCardsFile.rJSon()
    except:
        response = requests.get('https://api2.splinterlands.com/cards/get_details?')
        allCards = json.loads(response.text)
        allCardsFile.wJSon(allCards)
    try:
        ownerCardFile = File('data/playable.json')
        ownerCards = ownerCardFile.rJSon()
    except:
        ownerCards = []

    def getNames(list_card):
        list_of_card_names = []
        for card in list_card:
            list_of_card_names.append(card['name'])
        return list_of_card_names


    def sortNames(list_card):
        return sorted(Card.getNames(list_card))

    def showNames(list_card='owner'):
        if list_card == 'owner':
            typeOfListCard = Card.ownerCards
            length = len(typeOfListCard)
        elif list_card == 'all':
            typeOfListCard = Card.allCards
            length = len(typeOfListCard)
        elif list_card == 'na':
            typeOfListCard = Card.cardNotAvailable()
            length = len(typeOfListCard)
        listOfNames = Card.sortNames(typeOfListCard)
        numOfRow = length // 4
        numOfRedundantNames = length % 4
        columnName = [] 
        listIndex = []
        listOfRedundantNames = []
        i = 1
        a = 0
        b = numOfRow
        while (i <= 3):
            columnName.append(listOfNames[a:b])
            if numOfRedundantNames >= i:
                listOfRedundantNames.append(listOfNames[b])
                b += 1
                listIndex.append(b)
            a = b
            b = b + numOfRow
            i += 1

        columnName.append(listOfNames[a:b])
        indexLastRow = ((1, 1, 1), (2, 2, 2), (2, 3, 3), (2, 3, 4))

        for i in range(numOfRow):
            index = indexLastRow[numOfRedundantNames]
            print(
                f'{i + 1:>3} {columnName[0][i]:<23}{i + index[0] + numOfRow:>3} {columnName[1][i]:<23}{i + index[1] + numOfRow * 2:>3} {columnName[2][i]:<23}{i + index[2] + numOfRow * 3:>3} {columnName[3][i]:<23}')

            
        if numOfRedundantNames != 0:
            for i in range(len(listOfRedundantNames)):
                print(f'{listIndex[i]:>3} {listOfRedundantNames[i]:<23}', end='')
        print()


    def cardNotAvailable():
        cardNA = []
        sortedNameCardList = Card.sortNames(Card.ownerCards)
        for card in Card.allCards:
            if not (card['name'] in sortedNameCardList):
                cardNA.append(card)
        return cardNA


    def add():
        card_added = None
        n = None
        while (n != 'Q'):
            os.system('cls')
            listName = Card.sortNames(Card.cardNotAvailable())
            cardNA = Card.cardNotAvailable()
            Card.showNames('na')
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
                        Card.ownerCards.append(card)
                        card_added = listName[n]
                        Card.ownerCardFile.wJSon(Card.ownerCards)
                        break
            else:
                print('Thông tin không hợp lệ!')
                time.sleep(1)

    def delete():
        n = None
        cardDeleted = None
        while (n != 'Q'):
            listName = Card.sortNames(Card.ownerCards)
            os.system('cls')
            Card.showNames('owner')
            print('_' * 112)
            if cardDeleted is not None:
                print(f'Đã xoá "{cardDeleted}"')
            else:
                print()
            print('Nhập số của thẻ mà bạn muốn xoá')
            print('[Q] Thoát\n')
            n = input('>> Chọn: ').upper()
            if n.isdigit() and int(n) - 1 < len(Card.ownerCards) and int(n) - 1 >= 0:
                n = int(n) - 1
                for card in range(len(Card.ownerCards)):
                    if Card.ownerCards[card]['name'] == listName[n]:
                        cardDeleted = listName[n]
                        del Card.ownerCards[card]
                        break
                Card.ownerCardFile.wJSon(Card.ownerCards)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)


    def details(number):
        os.system('cls')
        listName = Card.sortNames(Card.ownerCards)
        card = {}
        for i in Card.ownerCards:
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

    def getMana(card_name):
        for card in Card.allCards:
            if card_name == card['name']:
                try:
                    return card['stats']['mana'][0]
                except:
                    return card['stats']['mana']

    def show():
        n = ''
        while (n != 'Q'):
            os.system('cls')
            Card.showNames('owner')
            print('_' * 112)
            print('\nNhập số của thẻ để xem chi tiết')
            print('[A] Thêm    |    [D] Xoá    |    [Q]Thoát')
            n = input('>> Chọn: ').upper()
            if n.isalpha() and n == 'A':
                Card.add()
            elif n.isalpha() and n == 'D':
                Card.delete()
            elif n.isdigit() and int(n) - 1 < len(Card.ownerCards) and int(n) - 1 >= 0:
                Card.details(int(n) - 1)
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

class AccountManager:
    try:
        accountFile = File('data/account.json')
        account = accountFile.rJSon()
    except:
        account = []

    def show():
        if len(AccountManager.account) > 0:
            number = 1
            for i in AccountManager.account:
                print(f'{number}. {i["mail"]}')
                number += 1

    def add():
        os.system('cls')
        email = input('Email: ')
        password = input('Mật khẩu: ')
        account = Account(email, password)
        AccountManager.account.append(account.toDict())
        AccountManager.accountFile.wJSon(AccountManager.account)

    def delete():
        select = None
        while (select != 'B'):
            os.system('cls')
            print('DANH SÁCH TÀI KHOẢN\n')
            if len(AccountManager.account) > 0:
                j = 1
                for i in AccountManager.account:
                    print(f'{j}. {i["mail"]}')
                    j += 1
            else:
                break
            print('\n[B] Trở lại')
            select = input('>> Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(AccountManager.account) and int(select) - 1 >= 0):
                AccountManager.account.pop(int(select) - 1)
                AccountManager.accountFile.wJSon(AccountManager.account)
            elif select != 'B':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)
            else:
                select = 'B'

    def show():
        n = ''
        while (n != 'Q'):
            os.system('cls')
            print('DANH SÁCH TÀI KHOẢN\n')
            if len(AccountManager.account) > 0:
                j = 1
                for i in AccountManager.account:
                    print(f'{j}. {i["mail"]}')
                    j += 1
                print("\n[A] Thêm    |    [D] Xoá    |    [Q] Thoát")
                n = input('>> Chọn: ').upper()
                if n == 'A':
                    AccountManager.add()
                elif n == 'D':
                    AccountManager.delete()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)
            else:
                print("Không có tài khoản nào, vui lòng thêm tài khoản!")
                print("\n[A] Thêm    |    [Q] Thoát")
                n = input('>> Chọn: ').upper()
                if n == 'A':
                    AccountManager.add()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)


class History:
    try:
        historyFile = File('data/history.json')
        history = historyFile.rJSon()
    except:
        history = {}

    def analys(mana):
        select = ''
        while (select != 'Q'):
            os.system('cls')
            Team.topCard(mana)
            print("Chọn đội hình để xem chi tiết\n")
            j = 1
            for i in Team.teams[mana]:
                print(f'[{j}] {", ".join(i)}')
                j += 1
            print('\n[Q] Thoát')
            select = input('>> Chọn đội hình: ').upper()
            if select.isdigit() and (int(select) - 1 >= 0 and int(select) - 1 < len(Team.teams[mana])):
                select = int(select) - 1
                team = Team.teams[mana][select]
                kda = History.kda(mana, team)
                os.system('cls')
                print(f'Team: {", ".join(team)}')
                print(f"\nTrong {kda[3]} trận:")
                print(f'    Thắng: {kda[0]}')
                print(f'    Thua: {kda[1]}')
                print(f'    Hoà: {kda[2]}')
                if len(History.history) > 0:
                    if kda[3] != 0:
                        print('\n\t\t\t\t\t\tLỊCH SỬ THUA\n')
                        for i in range(len(History.history[mana])):
                            if History.history[mana][i]['my_team']['team'] == team:
                                result = History.history[mana][i]['result']
                                if result[7:] == 'Lost':
                                    print('\n> [', end="")
                                    print(", ".join(History.history[mana][i]['enemy_team']['team']), end="")
                                    print(']')
                                    listNumCard = []
                                    listName = History.numOfCard()
                                    for k in History.history[mana][i]['enemy_team']['team']:
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

    def kda(mana, team):
        if len(History.history) > 0:
            won = 0 
            lost = 0
            drawn = 0
            match = 0
            if History.history.get(mana) != None:
                for i in range(len(History.history[mana])):
                    if History.history[mana][i]['my_team']['team'] == team:
                        if History.history[mana][i]['result'] == 'Battle Won': won += 1
                        if History.history[mana][i]['result'] == 'Battle Lost': lost += 1
                        if History.history[mana][i]['result'] == 'Drawn': drawn += 1
                match = won + lost + drawn
            return [won, lost, drawn, match]
        else:
            return [0, 0, 0, 0]

    def writeHistory(driver, times):
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
            if History.history.get(mana) == None:
                History.history[mana] = []
                History.history[mana].append(match)
            else:
                History.history[mana].append(match)
            History.historyFile.wJSon(History.history)

class Team:
    try:
        teamFile = File('data/team.json')
        teams = teamFile.rJSon()
    except:
        teams = {}
    manaList = ('12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '99')

    def inputMana():
        mana = input('>> Mana: ')
        while (not mana.isdigit() or not (mana in Team.manaList)):
            os.system('cls')
            print('Số mana không hợp lệ, thử lại!')
            print(f'Những mana hợp lệ: {", ".join(Team.manaList)}\n')
            mana = input('>> Mana: ')
        return mana

    def currentMana(team_adding):
        currentMana = 0
        for i in team_adding:
            currentMana += Card.getMana(i)
        return currentMana

    def teamSorted(list_team):
        team_sorted = {}
        for key in sorted(list_team.keys()):
            team_sorted[key] = list_team.get(key)
        return team_sorted

    def add():
        os.system('cls')
        mana = Team.inputMana()
        select = ''
        teamAdding = []
        listName = Card.sortNames(Card.ownerCards)
        while (select != 'Q'):
            os.system('cls')
            Card.showNames()
            print("\n")
            print(f'Mana: [{Team.currentMana(teamAdding)}/{mana}]')
            print('\n'.join(teamAdding))
            print(
                "\n[S] Lưu    |    [C] Xoá bỏ tất cả    |    [M] Sửa mana    |    [D] Xoá thẻ bài vừa chọn    |    [Q] Thoát\n")
            select = input('>> Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(Card.ownerCards) and int(select) - 1 >= 0):
                select = int(select) - 1
                teamAdding.append(listName[select])
            elif (select == 'S'):
                if (len(teamAdding) == 0):
                    print('Đội hình trống! Thử lại.')
                    select = ''
                    time.sleep(1)
                else:
                    if (Team.teams.get(mana) != None):
                        Team.teams[mana].append(teamAdding)
                    else:
                        Team.teams[mana] = []
                        Team.teams[mana].append(teamAdding)
                    Team.teams = Team.teamSorted(Team.teams)
                    Team.teamFile.wJSon(Team.teams)
                    print('Đội hình đã được lưu!')
                    time.sleep(1)
                    teamAdding = []
            elif (select == 'C'):
                teamAdding.clear()
            elif (select == 'M'):
                os.system('cls')
                mana = Team.inputMana()
            elif (select == 'D'):
                if len(teamAdding) > 0: teamAdding.pop(-1)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)

    def delete():
        os.system('cls')
        mana = lt = None
        while True:
            os.system('cls')
            mana = input('>> Nhập mana: ')
            lt = Team.teams.get(mana)
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
            Team.teams[mana].pop(int(td) - 1)
            if len(Team.teams[mana]) == 0: Team.teams.pop(mana)
            Team.teamFile.wJSon(Team.teams)
            os.system('cls')
            print('Đã xoá thành công!')
            time.sleep(1)

    def stringList(li):
        return f'[{", ".join(li)}]'
    
    def randomTeam(team):
        if len(team) == 1:
            return team[0]
        else:
            a = random.randrange(0, len(team))
            return team[a]

    def teamSelector(mana):
        mana = str(mana)
        team = Team.teams.get(mana)
        teamSelected = ''
        if team is not None:
            teamSelected = Team.randomTeam(team)
        else:
            try:
                teamDefault = File('data/team_default.json')
                team = teamDefault.rJSon()
            except:
                response = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/team_default.json')
                team = json.loads(response.text)
                teamDefault.wJSon(Team.team_def)
            teamSelected = team[mana][0]
        return Team.stringList(teamSelected)

    def checkTeam():
        if len(Team.teams) <= 20:
            teamNA = []
            for mana in Team.manaList:
                if Team.teams.get(mana) == None:
                    teamNA.append(mana)
            print('-' * 120)
            print('CHÚ Ý!')
            print('''Bạn chưa thêm đủ đội hình, vì thế những đội hình nào chưa có chúng tôi sẽ chọn đội hình mặc định để chiến đấu, và
kết quả có thể sẽ không như mong muốn!''')
            print('\nNhững đội hình có mana sau chưa được thêm:')
            print(", ".join(teamNA))
            print('-' * 120)

    def numOfCard():
        listCard = Card.sortListOfName(Card.allCardList)
        numCard = {}
        for i in range(1, len(listCard) + 1):
            numCard[listCard[i - 1]] = str(i)
        return numCard

    def topCard(mana):
        if len(History.history) > 0:
            print(f"THẺ BÀI ĐƯỢC ĐỐI THỦ CHỌN NHIỀU NHẤT VỚI {mana} MANA\n")
            team = {}
            for i in History.history[mana]:
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

    def show():
        select = ''
        while (select != 'Q'):
            os.system('cls')
            won = lost = drawn = match = 0
            if len(Team.teams) > 0:
                for mana in Team.teams:
                    print('_' * 120)
                    print(f'\n MANA {mana}:')
                    k = 1
                    for i in Team.teams[mana]:
                        kda = History.kda(Team.teamFile, i)
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
            Team.checkTeam()
            print(f'\n>> Tổng cộng: {match} trận đấu  |   Tỉ lệ thắng {round(sumOfWinRate, 2)}%\n')
            print('\nNhập số mana để xem chi tiết, hoặc:')
            print('[A] Thêm    |    [D] Xoá    |    [Q] Thoát')
            select = input('\n>> Chọn: ').upper()
            if select == 'A':
                Team.add()
            elif select == 'D':
                Team.delete()
            elif select.isdigit() and (Team.teams.get(select) != None):
                History.analys(select)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)


class Launcher:
    logo = '''
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
    keyFile = File('data/key')
    versionFile = File('data/version')
    updateFile = File('update.py')

    def menu():
        Launcher.update()
        select = None
        while (select != 'Q'):
            os.system('cls')
            print(Launcher.logo)
            print(f"\t\t\t\t\t\t     Bản dựng {'.'.join(str(x) for x in Launcher.version())}")
            print('\n1: Vào game\n2: Đội hình\n3: Tài khoản\n4: Thẻ bài\n5: Phản hồi\n\n[Q] Thoát')
            select = input('\n>> Chọn: ').upper()
            
            if select == '1':
                pass
            elif select == '2':
                Team.show()
            elif select == '3':
                AccountManager.show()
            elif select == '4':
                Card.show()
            elif select == '5':
                Launcher.feedback()
            elif select != 'Q':
                print('Cú pháp không hợp lệ! Thử lại.')
                time.sleep(1)
        

    def shutDown(mess):
        for i in range(3,0,-1):
            os.system('cls')
            print(mess)
            print(f'Ứng dụng sẽ đóng trong {i}')
            time.sleep(1)



    def checkVer(old_ver, new_ver):
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


    def version():
        try:
            version = Launcher.versionFile.rJSon()
        except:
            response = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/data/version')
            version = json.loads(response.text.strip())
            Launcher.versionFile.wJSon(version)
        return version	


    def update():
        ver = Launcher.version()
        get_version = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/data/version')
        new_ver = json.loads(get_version.text.strip())
        if Launcher.checkVer(ver, new_ver):
            get_update = requests.get('https://raw.githubusercontent.com/tmkha/splinterlands/master/update.py')
            Launcher.updateFile.wText(get_update.text)
            from update import update_lib
            update_lib()
            Launcher.versionFile.wJSon(new_ver)
            try:
                os.remove('update.py')
            except:
                pass

    def feedback():
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