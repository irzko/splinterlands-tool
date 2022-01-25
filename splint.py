from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import json, os, time, requests, random
import multiprocessing


empty_line = "  │                                                                                                                  │"
end = "  └──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘"
break_line = "  ├──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤"

def header(tittle):
    t = " {0} ".format(tittle)
    p = t.center(114, '═')
    header = "\n  ╒" + p.format(tittle) + "╕"
    print(header)
    print(empty_line)
def make_empty_line(line):
    for i in range(0, line):
        print(empty_line)
class File:
    def __init__(self, path):
        self.path = path

    def wText(self, content):
        with open(self.path, 'w', encoding='utf-8') as file:
            file.write(content)
            file.close()

    def wJSon(self, content):
        with open(self.path, 'w', encoding='utf-8') as file:
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

    def getNameById(id):
        for card in Card.allCards:
            if card['id'] == id:
                return card['name']

    def sortNames(list_card):
        return sorted(Card.getNames(list_card))

    def showNames(typeOfListCard, li = True, start=0):
        if li:
            listOfNames = Card.sortNames(typeOfListCard)
        else:
            listOfNames = typeOfListCard
        length = len(typeOfListCard)
        numOfRow = (length // 4)
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

        for row in range(numOfRow):
            index = indexLastRow[numOfRedundantNames]
            i = row + start
            print('  │'.ljust(7) +
                f'{i + 1:>3} {columnName[0][row]:<23}{i + index[0] + numOfRow:>3} {columnName[1][row]:<23}{i + index[1] + numOfRow * 2:>3} {columnName[2][row]:<23}{i + index[2] + numOfRow * 3:>3} {columnName[3][row]:<23}' + '│'.rjust(3))
        
        t = 0
        if len(listOfRedundantNames) == 1:
            t = 84
        elif len(listOfRedundantNames) == 2:
            t = 57
        elif len(listOfRedundantNames) == 3:
            t = 30
        if numOfRedundantNames != 0:
            print('  │'.ljust(7), end='')
            for row in range(len(listOfRedundantNames)):
                i = listIndex[row] + start
                print(f'{i:>3} {listOfRedundantNames[row]:<23}', end='')
            print('│'.rjust(t))


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
            header("Danh sách thẻ")
            listName = Card.sortNames(Card.cardNotAvailable())
            cardNA = Card.cardNotAvailable()
            Card.showNames(Card.cardNotAvailable())
            make_empty_line(1)
            print('  │' + 'Nhập số của thẻ mà bạn muốn thêm'.center(114) + '│')
            print('  │' + '[Q]Thoát'.center(114) + '│')
            print(end)
            if card_added is not None:
                print(f'Đã thêm "{card_added}"')
            n = input('  > Chọn: ').upper()
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
                print('Thông tin không hợp lệ!'.center(116))
                time.sleep(1)

            


    def delete():
        n = None
        cardDeleted = None
        while (n != 'Q'):
            os.system('cls')
            listName = Card.sortNames(Card.ownerCards)
            header("Danh sách thẻ")
            Card.showNames(Card.ownerCards)
            make_empty_line(1)
            print('  │' + 'Nhập số của thẻ mà bạn muốn xoá'.center(114) + '│')
            print('  │' + '[Q]Thoát'.center(114) + '│')
            print(end)
            if cardDeleted is not None:
                print(f'Đã xoá "{cardDeleted}"')
            n = input('  > Chọn: ').upper()
            if n.isdigit() and int(n) - 1 < len(Card.ownerCards) and int(n) - 1 >= 0:
                n = int(n) - 1
                for card in range(len(Card.ownerCards)):
                    if Card.ownerCards[card]['name'] == listName[n]:
                        cardDeleted = listName[n]
                        del Card.ownerCards[card]
                        break
                Card.ownerCardFile.wJSon(Card.ownerCards)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!'.center(116))
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
        print(f'{"Color:":<10}{card["color"]}')
        print(f'{"Type:":<10}{card["type"]}')
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

    def getColor(card_name):
        for card in Card.allCards:
            if card_name == card['name']:
                return card['color']

    def getSummoner(color=None):
        cd = []
        if color == None:
            for card in Card.ownerCards:
                if card['type'] == 'Summoner':
                    cd.append(card)
        else:
            for card in Card.ownerCards:
                if card['type'] == 'Summoner' and card['color'] == color:
                    cd.append(card)
        return cd

    def getMonsters(color=None):
        cd = []
        if color == None:
            for card in Card.ownerCards:
                if card['type'] == 'Monster':
                    cd.append(card)
        else:
            for card in Card.ownerCards:
                if card['type'] == 'Monster' and card['color'] == color:
                    cd.append(card)
        return cd


    def show():
        n = ''
        while (n != 'Q'):
            os.system('cls')
            header("Thẻ bài đang sở hữu")
            Card.showNames(Card.ownerCards)
            print(empty_line)
            print('  │' + 'Nhập số của thẻ để xem chi tiết'.center(114) + '│')
            print('  │' + '[A] Thêm    |    [D] Xoá    |    [Q]Thoát'.center(114) + '│')
            print(end)
            n = input('  > Chọn: ').upper()
            if n.isalpha() and n == 'A':
                Card.add()
            elif n.isalpha() and n == 'D':
                Card.delete()
            elif n.isdigit() and int(n) - 1 < len(Card.ownerCards) and int(n) - 1 >= 0:
                Card.details(int(n) - 1)
            elif n != 'Q':
                print('Cú pháp không hợp lệ!'.center(116))
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
    def __init__(self):
        try:
            self.accountFile = File('data/account.json')
            self.account = self.accountFile.rJSon()
        except:
            self.account = []


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
            header("Danh sách tài khoản")
            make_empty_line(5)
            if len(self.account) > 0:
                j = 1
                for i in self.account:
                    print('  │'.ljust(5) + f"{j}. {i['mail']}".ljust(112) + '│')
                    j += 1
            else:
                break
            make_empty_line(5)
            print('  │' + "Chọn tài khoản muốn xoá".center(114) + '│')
            print('  │' + "[B] Trở lại".center(114) + '│')
            print(end)
            select = input('  > Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(self.account) and int(select) - 1 >= 0):
                self.account.pop(int(select) - 1)
                self.accountFile.wJSon(self.account)
            elif select != 'B':
                print('Cú pháp không hợp lệ!'.center(116))
                time.sleep(1)
            else:
                select = 'B'

    def show(self):
        n = ''
        while (n != 'Q'):
            os.system('cls')
            header("Danh sách tài khoản")
            make_empty_line(4)
            if len(self.account) > 0:
                j = 1
                for i in self.account:
                    print('  │'.ljust(5) + f"{j}. {i['mail']}".ljust(112) + '│')
                    j += 1
                make_empty_line(5)
                print('  │' + "[A] Thêm    |    [D] Xoá    |    [Q] Thoát".center(114) + '│')
                print(end)
                n = input('  > Chọn: ').upper()
                if n == 'A':
                    self.add()
                elif n == 'D':
                    self.delete()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!'.center(114))
                    time.sleep(1)
            else:
                print('  │' + "Không có tài khoản nào, vui lòng thêm tài khoản!".center(114) + '│')
                make_empty_line(5)
                print('  │' + "[A] Thêm    |    [Q] Thoát".center(114) + '│')
                print(end)
                n = input('  > Chọn: ').upper()
                if n == 'A':
                    self.add()
                elif n != 'Q':
                    print('Cú pháp không hợp lệ!'.center(116))
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
            print('  │' + "Chọn đội hình để xem chi tiết".center(114) + '│')
            make_empty_line(1)
            j = 1
            for i in Team.teams[mana]:
                print('  │'.ljust(5) + f'[{j}] {", ".join(i)}'.ljust(112) + '│')
                j += 1
            make_empty_line(1)
            print('  │' + "[Q] Thoát".center(114) + '│')
            print(end)
            select = input('  > Chọn đội hình: ').upper()
            if select.isdigit() and (int(select) - 1 >= 0 and int(select) - 1 < len(Team.teams[mana])):
                n = None
                select = int(select) - 1
                while (n != 'Q' and n != 'B'):
                    team = Team.teams[mana][select]
                    kda = History.kda(mana, team)
                    os.system('cls')
                    header("Thông tin")
                    print('  │' + 'Đội của bạn'.center(114) + '│')
                    print('  │' + f'{", ".join(team)}'.center(114) + '│')
                    print('  │' + f"Thắng: {kda[0]} / Thua: {kda[1]} / Hoà: {kda[2]} / {kda[3]} trận".center(114) + '│')
                    print(break_line)
                    p = []
                    print('  │' + 'Các đội đã thắng đội của bạn'.center(114) + '│')
                    make_empty_line(1)
                    if len(History.history) != 0:
                        if kda[3] != 0:
                            e_team = []
                            for i in History.history[mana]:
                                if i['team1']['team'] == team:
                                    result = i['result']
                                    if result[7:] == 'Lost':
                                        e_team.append(i['team2']['team'])
                            for i in e_team:
                                if p.count(i) == 0:
                                    p.append(i)
                            for i in range(len(p)):
                                print('  │'.ljust(2) + f"┌ [{i+1}] {', '.join(p[i])}".ljust(114) + '│')
                                print('  │' + f'└ Đánh bại bạn {e_team.count(p[i])} lần'.ljust(114) + '│')
                                make_empty_line(1)
                            print('  │' + "Nhập số của đội hình để sao chép".center(114) + '│')
                        else:
                            make_empty_line(4)
                            print('  │' + "Không có lịch sử".center(114) + '│')
                            make_empty_line(5)
                    print('  │' + "[B] Trở lại    |    [Q] Thoát".center(114) + '│')
                    print(end)
                    n = input('  > Chọn: ').upper()
                    if n.isdigit() and int(n) - 1 < len(p) and int(n) - 1 >= 0:
                        Team.copyTeam(mana, p[int(n)-1])
                    elif n == 'Q':
                        select = 'Q'
                    elif n != 'B':
                        print('Cú pháp không hợp lệ!'. center(116))
                        time.sleep(1)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!'. center(116))
                time.sleep(1)

    def kda(mana, team):
        if len(History.history) > 0:
            won = 0 
            lost = 0
            drawn = 0
            match = 0
            if History.history.get(mana) != None:
                for i in range(len(History.history[mana])):
                    if History.history[mana][i]['team1']['team'] == team:
                        if History.history[mana][i]['result'] == 'Battle Won': won += 1
                        if History.history[mana][i]['result'] == 'Battle Lost': lost += 1
                        if History.history[mana][i]['result'] == 'Drawn': drawn += 1
                match = won + lost + drawn
            return [won, lost, drawn, match]
        else:
            return [0, 0, 0, 0]

    def delete(mana, team):
        length = len(History.history[mana])
        i = 0
        while(i < length):
            myTeam = History.history[mana][i]['team1']['team']
            if myTeam == team:
                History.history[mana].pop(i)
                length = len(History.history[mana])
                i -=1
            i += 1
        History.historyFile.wJSon(History.history)


    def writeHistory(username):
        response = requests.get('https://api2.splinterlands.com/battle/history2?player=' + username)
        history = json.loads(response.text)
        mana_cap = history['battles'][0]['mana_cap']
        player_1 = username
        if history['battles'][0]['player_2'] != username:
            player_2 = history['battles'][0]['player_2']
        else:
            player_2 = history['battles'][0]['player_1']
        
        winner = history['battles'][0]['winner']
        result = None
        if winner == player_1:
            result = "Battle Won"
        elif winner == player_2:
            result = "Battle Lost"
        else:
            result = "Drawn"
        team1 = []
        team2 = []
        sw_t1 = 'team1'
        sw_t2 = 'team2'
        if history['battles'][0]['player_2'] == username:
            sw_t1 = 'team2'
            sw_t2 = 'team1' 
        summoner = history['battles'][0]['details'][sw_t1]['summoner']['card_detail_id']
        team1.append(Card.getNameById(summoner))
        monsters = history['battles'][0]['details'][sw_t1]['monsters']
        for monster in monsters:
            team1.append(Card.getNameById(monster['card_detail_id']))
        summoner = history['battles'][0]['details'][sw_t2]['summoner']['card_detail_id']
        team2.append(Card.getNameById(summoner))
        monsters = history['battles'][0]['details'][sw_t2]['monsters']
        for monster in monsters:
            team2.append(Card.getNameById(monster['card_detail_id']))
        match = {'result': result, "team1": {"player": player_1, 'team': team1}, "team2": {"player": player_2, 'team': team2}}
        mana_cap = str(mana_cap)
        if History.history.get(mana_cap) == None:
            History.history[mana_cap] = []
            History.history[mana_cap].append(match)
        else:
            History.history[mana_cap].append(match)
        History.historyFile.wJSon(History.history)

class Team:
    try:
        teamFile = File('data/team.json')
        teams = teamFile.rJSon()
    except:
        teams = {}
    manaList = ('12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '99')
 
    def inputMana():
        mana = input('  > Mana: ')
        while (not mana.isdigit() or not (mana in Team.manaList)):
            os.system('cls')
            print('Số mana không hợp lệ, thử lại!')
            print(f'Những mana hợp lệ: {", ".join(Team.manaList)}\n')
            mana = input('  > Mana: ')
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
        listName = None
        summoner_card = Card.sortNames(Card.getSummoner())
        monster_card = Card.sortNames(Card.getMonsters())
        temp = []
        while (select != 'Q'):
            os.system('cls')
            print()
            if len(teamAdding) == 0:
                header("Thẻ Summoner")
                Card.showNames(summoner_card, False)
                listName = summoner_card
            else:
                header("Thẻ Monster")
                Card.showNames(monster_card, False)
                listName = monster_card
            make_empty_line(1)
            print('  ├' + ' Đang chọn '.center(114, "─") + '┤')
            print('  │' + f'Mana: {Team.currentMana(teamAdding)}/{mana}'.center(114) + '│')
            for i in teamAdding:
                print('  │'.ljust(8) + i.ljust(109) + '│')
            make_empty_line(1)
            print('  │' + '[S] Lưu    |    [C] Xoá bỏ tất cả    |    [M] Sửa mana    |    [D] Xoá thẻ bài vừa chọn    |    [Q] Thoát'.center(114) + '│')
            print(end)
            select = input('  > Chọn: ').upper()
            if (select.isdigit() and int(select) - 1 < len(Card.ownerCards) and int(select) - 1 >= 0):
                select = int(select) - 1
                card_selected = listName[select]
                teamAdding.append(card_selected)
                if len(teamAdding) > 1:
                    temp.append(card_selected)
                    monster_card.remove(card_selected)
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
                summoner_card = Card.sortNames(Card.getSummoner())
                monster_card = Card.sortNames(Card.getMonsters())
            elif (select == 'M'):
                os.system('cls')
                mana = Team.inputMana()
            elif (select == 'D'):
                if len(teamAdding) > 1:
                    monster_card.append(temp[-1])
                    monster_card = sorted(monster_card)
                    temp.pop(-1)
                if len(teamAdding) > 0: teamAdding.pop(-1)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!')
                time.sleep(1)

    def delete():
        os.system('cls')
        mana = None
        lt = None
        while True:
            os.system('cls')
            mana = input('  > Nhập mana: ')
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
            td = input('  > Chọn: ')
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
            acpt = input(f'Đội hình đã được chọn:\n{st}\n\nBạn có muốn xoá đội hình này? [Y/N]\n  > Chọn: ').upper()
            if acpt != 'Y' and acpt != 'N':
                print("Cú pháp không hợp lệ! Thử lại.")
            else:
                break
        if acpt == 'Y':
            try:
                History.delete(mana, st)
            except:
                pass
            finally:
                Team.teams[mana].pop(int(td) - 1)
                if len(Team.teams[mana]) == 0: Team.teams.pop(mana)
                Team.teamFile.wJSon(Team.teams)
                os.system('cls')
                print('Đã xoá thành công!')
                time.sleep(1)


    def stringList(li):
        return '["' + '", "'.join(li) + '"]'
    
    def randomTeam(team):
        if len(team) == 1:
            return team[0]
        else:
            a = random.randrange(0, len(team))
            return team[a]

    def randomBot(p_src, mana):
        mana = int(mana)
        soup = BeautifulSoup(p_src, 'html.parser')
        x = soup.find_all(class_='deck-builder-page2__cards')
        y = x[0].find_all(class_='card-name-name')
        color = []
        for i in y:
            color.append(Card.getColor(i.text))

        color = set(color)
        color = list(color)
        color.remove('Gold')
        monster = Card.getMonsters(color[0])
        summoner = Card.getSummoner(color[0])
        p = []
        r = random.randint(0, len(summoner) - 1)
        p.append(summoner[r]['name'])
        i = 0
        while i <= mana:
            r = random.randint(0, len(monster) - 1)
            t = monster[r]
            if (Team.currentMana(p) + Card.getMana(t['name']) >= mana) or len(p) > 7:
               break
            else:
                p.append(t['name'])
                monster.pop(r)
                i  += Card.getMana(t['name'])
        return p

    def teamSelector(p_src, mana):
        mana = str(mana)
        team = Team.teams.get(mana)
        teamSelected = None
        if team is not None:
            teamSelected = Team.randomTeam(team)
        else:
            teamSelected = Team.randomBot(p_src, mana)

        summoner = '["' + teamSelected[0] + '"]'
        monster = Team.stringList(teamSelected[1:])
        color = Card.getColor(teamSelected[1])
        return {'summoner': summoner, 'monster': monster, 'color': color}
    
    def copyTeam(mana, team):
        n = None
        while (n != 'N'):
            os.system('cls')
            header("Thông tin sao chép")
            print('  │' + f"{', '.join(team)}".center(114) + '│')
            make_empty_line(5)
            print('  │' + "Bạn có muốn sao chép đội hình này?".center(114) + '│')
            print('  │' + "[Y] Có    |    [N] Không".center(114) + '│')
            print(end)
            n = input('  > Chọn: ').upper()
            if n == "Y":
                if (Team.teams.get(mana) != None):
                    Team.teams[mana].append(team)
                else:
                    Team.teams[mana] = []
                    Team.teams[mana].append(team)
                Team.teams = Team.teamSorted(Team.teams)
                Team.teamFile.wJSon(Team.teams)
                os.system('cls')
                print('Đã sao chép thành công!'.center(116))
                time.sleep(1)
                n = 'N'
            elif n != 'N':
                print('Cú pháp không hợp lệ!'.center(116))
                time.sleep(1)

    def checkTeam():
        if len(Team.teams) < 20:
            teamNA = []
            for mana in Team.manaList:
                if Team.teams.get(mana) == None:
                    teamNA.append(mana)
            print(break_line)
            print('  │' + "CHÚ Ý!".center(114) + '│')
            print('  │' + "Bạn chưa thêm đủ đội hình, vì thế những đội hình nào chưa có chúng tôi sẽ chọn đội hình mặc định để chiến đấu,".center(114) + '│')
            print('  │' + "và kết quả có thể sẽ không như mong muốn!".center(114) + '│')
            make_empty_line(1)
            print('  │' + "Những đội hình có mana sau chưa được thêm:".center(114) + '│')
            print('  │' + f'{", ".join(teamNA)}'.center(114) + '│')

    def numOfCard():
        listCard = Card.sortNames(Card.allCards)
        numCard = {}
        for i in range(1, len(listCard) + 1):
            numCard[listCard[i - 1]] = str(i)
        return numCard

    def topCard(mana):
        if len(History.history) > 0:
            header("Thẻ bài được đối thủ chọn nhiều nhất")
            team = {}
            for i in History.history[mana]:
                enemyTeam = i['team2']['team']
                for j in enemyTeam:
                    if team.get(j) == None:
                        team[j] = 1
                    else:
                        team[j] += 1
            items_sorted = sorted(team.items(), reverse=True, key=lambda x: x[1])
            print('  │'.ljust(46) + f'{"Tên thẻ bài":>12}{"Số lần chọn":>16}'.ljust(71) + '│')
            j = 1
            for i in items_sorted:
                print('  │'.ljust(44) + f'{j:>2} {i[0]:<20} {i[1]:>2}'.ljust(73) + '│')
                j += 1
            print(break_line)

    def show():
        select = ''
        while (select != 'Q'):
            os.system('cls')
            header("Danh sách đội hình")
            won = lost = drawn = match = 0
            if len(Team.teams) > 0:
                for mana in Team.teams:
                    print('  ├'.ljust(5, '─') + f" Mana {mana} ".ljust(112, '─') + '┤')
                    make_empty_line(1)
                    k = 1
                    for i in Team.teams[mana]:
                        kda = History.kda(mana, i)
                        winRate = 0.0
                        if kda[3] != 0: winRate = int(kda[0]) / int(kda[3]) * 100
                        team = ", ".join(i)
                        print('  │'.ljust(2) + f"┌{team}".ljust(114) + '│')
                        won += int(kda[0])
                        lost += int(kda[1])
                        drawn += int(kda[2])
                        match += int(kda[3])
                        print('  │' + f'└Thắng: {kda[0]} / Thua: {kda[1]} / Hoà: {kda[2]} / {kda[3]} trận | Tỉ lệ thắng {round(winRate, 2)}%'.ljust(114) + '│')
                        k += 1
                        make_empty_line(1)
            sumOfWinRate = 0.0
            if match != 0: sumOfWinRate = won / match * 100
            Team.checkTeam()
            print(break_line)
            print('  │' + f"Tổng cộng: {match} trận đấu  |   Tỉ lệ thắng {round(sumOfWinRate, 2)}%".center(114) + '│')
            print(break_line)
            print('  │' + "Nhập số mana để xem chi tiết, hoặc:".center(114) + '│')
            print('  │' + "[A] Thêm    |    [D] Xoá    |    [Q] Thoát".center(114) + '│')
            print(end)
            select = input('  > Chọn: ').upper()
            if select == 'A':
                Team.add()
            elif select == 'D':
                Team.delete()
            elif select.isdigit() and (Team.teams.get(select) != None):
                History.analys(select)
            elif select != 'Q':
                print('Cú pháp không hợp lệ!'.center(116))
                time.sleep(1)
def showLog(log, email):
    time_log = time.strftime("%H:%M:%S", time.localtime())
    print(f'[{time_log}] [{email}] {log}')


def battle(account, match):
    service = ChromeService(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get('https://splinterlands.com')
    driver.find_element(By.ID, 'log_in_button').click()
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body")))
    time.sleep(1)
    driver.find_element(By.ID, 'email').send_keys(account['mail'])
    driver.find_element(By.ID, 'password').send_keys(account['pwd'])
    driver.find_element(By.ID, 'loginBtn').click()

    try:
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[2]/div[2]/div')))
        driver.execute_script("document.getElementsByClassName('close')[0].click();")
    except Exception as e:
        print(e)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    username = soup.find(class_='bio__name__display').text
    driver.get('https://splinterlands.com/?p=battle_history')
    try:
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div[1]")))
        driver.execute_script("document.getElementsByClassName('modal-close-new')[0].click();")
    except Exception as e:
        print(e)

    driver.execute_script('''var row = document.getElementsByClassName('row')[1].innerHTML;
            var reg = /HOW TO PLAY|PRACTICE|CHALLENGE|RANKED/;
            var result = row.match(reg);
            while(result != 'RANKED') {
                document.getElementsByClassName('slider_btn')[1].click();
                row = document.getElementsByClassName('row')[1].innerHTML;
                result = row.match(reg);
                };''')
    mana = 0
    def findMatch():
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#battle_category_btn')))
        driver.execute_script("document.getElementsByClassName('big_category_btn red')[0].click();")
        showLog('Đang tìm đối thủ...', username)

    def joinMatch():
        nonlocal mana
        WebDriverWait(driver, 30).until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
        time.sleep(1)
        mana = driver.find_element(By.CSS_SELECTOR, 'div.col-md-3:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
        showLog('Đang khởi tạo đội hình...', username)
        driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")

    def createTeam():
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
        showLog('Đang chọn thẻ bài...', username)
        time.sleep(7)
        team = Team.teamSelector(driver.page_source, mana)
        driver.execute_script("var team = "+ team['summoner'] + ";let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[0]){cimg[j].click();break;}}")
        try:
            WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="splinter_selection_modal"]/div/div')))
            color = team['color']
            if color == 'Black':
                driver.find_element(By.XPATH, '//*[@id="splinter_selection_modal"]/div/div/div[2]/div/div[5]').click()
            elif color == 'Red':
                driver.find_element(By.XPATH, '//*[@id="splinter_selection_modal"]/div/div/div[2]/div/div[1]').click()
            elif color == 'Blue':
                driver.find_element(By.XPATH, '//*[@id="splinter_selection_modal"]/div/div/div[2]/div/div[2]').click()
            elif color == 'Green':
                driver.find_element(By.XPATH, '//*[@id="splinter_selection_modal"]/div/div/div[2]/div/div[3]/label').click()
            elif color == 'White':
                driver.find_element(By.XPATH, '//*[@id="splinter_selection_modal"]/div/div/div[2]/div/div[4]').click()
        except:
            pass
        finally:
            driver.execute_script("var team = "+ team['monster'] + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")


    def startMatch():
        showLog('Đang chờ đối thủ...', username)
        WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnSkip')))
        showLog('Đang bỏ qua...', username)
        driver.find_element(By.ID, "btnSkip").click()
        showLog('Kết thúc trận đấu', username)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
        driver.execute_script('document.getElementsByClassName("btn btn--done")[0].click()')
        showLog('Đang lưu lịch sử trận đấu...', username)
        

    def checkErr():
        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="play_now"]/div/div/div/div/button')))
            return -1
        except:        
            try:
                WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
                return 0
            except:
                try:
                    WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
                    return 1
                except:         
                    try:
                        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
                        return 2
                    except:               
                        try:
                            WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnSkip')))
                            return 3
                        except:
                            return -2

    def checkPoint0():
        try:
            findMatch()
            checkPoint1()
            return 0
        except:
            return -1

    def checkPoint1():
        try:
            joinMatch()
            checkPoint2()
            return 0
        except:
            return -1

    def checkPoint2():
        try:
            createTeam()
            checkPoint3()
            return 0
        except:
            return -1

    def checkPoint3():
        try:
            startMatch()
            History.writeHistory(username)
            showLog('Xong', username)
            return 0
        except:
            return -1

    def tryAgain(x):
        c = -1
        if x == -1:
            driver.get('https://splinterlands.com/?p=battle_history')
            checkPoint0()
        elif x == 0:
            c = checkPoint0()
        elif x == 1:
            c = checkPoint1()
        elif x == 2:
            c = checkPoint2()
        elif x == 3:
            c = checkPoint3()
        return c


    for i in range(int(match)):
        showLog(f'Bắt đầu trận thứ [{i + 1}/{match}]', username)
        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
            checkPoint0()
        except:
            q = None
            while (q != 0):
                driver.refresh()
                cp = checkErr()
                if cp != -2:
                    q = tryAgain(cp)
    driver.quit()
    return 'Q'

def mbattle(account_list, match):
    proc = {}
    for i in range(len(account_list)):
        keys = 'p' + str(i + 1)
        proc[keys] = multiprocessing.Process(target=battle, args=(account_list[i], match))
    for b in proc:
        proc[b].start()
    response = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/splint.py')
    if response:
        File('splint.py').wText(response.text)
    for k in proc:
        proc[k].join()

class Launcher:
    keyFile = File('data/key')
    versionFile = File('data/version')
    updateFile = File('update.py')

    def menu():
        Launcher.update()
        accountManager = AccountManager()
        select = None
        while (select != 'Q'):
            os.system('cls')
            header("Menu")
            make_empty_line(5)
            # print(f"\t\t\t\t\t\t     Bản dựng {'.'.join(str(x) for x in Launcher.version())}")
            print('  │'.ljust(52) + '[1] Vào game'.ljust(65) + '│')
            print('  │'.ljust(52) + '[2] Đội hình'.ljust(65) + '│')
            print('  │'.ljust(52) + '[3] Tài khoản'.ljust(65) + '│')
            print('  │'.ljust(52) + '[4] Thẻ bài'.ljust(65) + '│')
            print('  │'.ljust(52) + '[5] Phản hồi'.ljust(65) + '│')
            make_empty_line(2)
            print('  │'.ljust(52) + '[Q] Thoát'.ljust(65) + '│')
            make_empty_line(6)
            print(end)
            select = input('  > Chọn: ').upper()
            
            if select == '1':
                Launcher.battle()
            elif select == '2':
                Team.show()
            elif select == '3':
                accountManager.show()
            elif select == '4':
                Card.show()
            elif select == '5':
                Launcher.feedback()
            elif select != 'Q':
                print('Cú pháp không hợp lệ! Thử lại.'.center(116))
                time.sleep(1)
        

    def shutDown(mess):
        for i in range(3,0,-1):
            os.system('cls')
            print(mess)
            print(f'Ứng dụng sẽ đóng trong {i}')
            time.sleep(1)

    def battle():
        accountManager = AccountManager()
        account_list = accountManager.account
        account_selected = []
        temp = []
        if len(account_list) > 0:
            select = None
            while (select != 'Q'):
                os.system('cls')
                header("Chọn tài khoản")
                print('  │' + f'Đã chọn {len(account_selected)} tài khoản'.center(114) + '│')
                if len(account_selected) > 0:
                    t = 1
                    for account in account_selected:
                        print('  │'.ljust(5) + f"{t}. {account['mail']}".ljust(112) + '│')
                        t += 1
                make_empty_line(1)
                print(break_line)
                make_empty_line(1)
                if len(account_list) >= 0:
                    j = 1
                    for k in account_list:
                        print('  │'.ljust(5) + f'[{j}] {k["mail"]}'.ljust(112) + '│')
                        j += 1
                    make_empty_line(4)
                    Team.checkTeam()
                    print('  │' + '[S] Bắt đầu    |    [C] Xoá lựa chọn trước đó    |    [A] Chọn tất cả    |    [Q] Thoát'.center(114) + '│')
                    print(end)
                    select = input('  > Chọn: ').upper()
                    if select.isdigit() and int(select) - 1 < len(account_list) and int(select) - 1 >= 0:
                        select = int(select)
                        select -= j
                        account_selected.append(account_list[select])
                        account_list.pop(select)
                    elif select == 'S' and len(account_selected) > 0:
                        os.system('cls')
                        match = None
                        while (match != 'Q'):
                            os.system('cls')
                            print('Nhập sô trận đấu')
                            print('[Q] Thoát\n')
                            match = input('> Chọn: ').upper()
                            if match.isdigit() and int(match) > 0:
                                if len(account_selected) == 1:
                                    battle(account_selected[0], match)
                                else:
                                    mbattle(account_selected, match)
                                break
                            if match != 'Q':
                                print('Vui lòng nhập một số hợp lệ!')
                                time.sleep(1)
                    elif select == 'S' and len(account_selected) == 0:
                        print('Vui lòng chọn ít nhất một tài khoản!'.center(116))
                        time.sleep(1)
                    elif select == 'C' and len(account_selected) > 0:
                        account_list.append(account_selected[-1])
                        account_selected.pop(-1)
                    elif select == 'A':
                        if len(account_list) > 0:
                            account_selected = account_list.copy()
                            account_list.clear()
                    elif select != 'Q':
                        print('Cú pháp không hợp lệ!'.center(116))
                        time.sleep(1)
        else:
            m = ''
            while (m != 'Q'):
                os.system('cls')
                print("CHỌN TÀI KHOẢN")
                print("\nKhông có tài khoản nào, vui lòng thêm tài khoản!")
                print('\n[Q] Thoát')
                m = input('  > Chọn: ').upper()
                if m != 'Q':
                    print('Cú pháp không hợp lệ!')
                    time.sleep(1)
        return 'Q'

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
            get_update = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/update.py')
            Launcher.updateFile.wText(get_update.text)
            from update import update_lib
            update_lib()
            Launcher.versionFile.wJSon(new_ver)
            try:
                os.remove('update.py')
            except:
                pass

    def feedback():
        os.system('cls')
        print('Mô tả nội dung phản hồi')
        print('[Q] Thoát\n')
        content = input('  > ')
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