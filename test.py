from splint import *
class Battle:
    def __init__(self, account):
        self.team = []
        self.mana = 0
        self.account = account
        options = webdriver.ChromeOptions()
        #chrome_options.add_argument("user-data-dir="+filePath)
        self.driver = webdriver.Chrome('chromedriver', options = options)

    def showLog(self, log, email):
        time_log = time.strftime("%H:%M:%S", time.localtime())
        print(f'[{time_log}] [{email}] {log}')

    def start(self, match):
        self.showLog('Đang khởi động trình duyệt...', self.account['mail'])
        wait = WebDriverWait(self.driver, 60)
        self.driver.get('https://splinterlands.com/?p=battle_history')
        self.driver.find_element(By.ID, 'log_in_button').click()
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal-body")))
        time.sleep(1)
        self.driver.find_element(By.ID, 'email').send_keys(self.account['mail'])
        self.driver.find_element(By.ID, 'password').send_keys(self.account['pwd'])
        self.driver.find_element(By.CSS_SELECTOR,'form.form-horizontal:nth-child(2) > div:nth-child(3) > div:nth-child(1) > button:nth-child(1)').click()
        try:
            WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[2]/div[2]/div')))
            self.driver.execute_script("document.getElementsByClassName('close')[0].click();")
        except:
            pass
        self.driver.get('https://splinterlands.com/?p=battle_history')
        try:
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div[1]/div[1]")))
            self.driver.execute_script("document.getElementsByClassName('modal-close-new')[0].click();")
        except:
            pass

        self.driver.execute_script('''var row = document.getElementsByClassName('row')[1].innerHTML;
                var reg = /HOW TO PLAY|PRACTICE|CHALLENGE|RANKED/;
                var result = row.match(reg);
                while(result != 'RANKED') {
                    document.getElementsByClassName('slider_btn')[1].click();
                    row = document.getElementsByClassName('row')[1].innerHTML;
                    result = row.match(reg);
                    };''')
    
        checkPoint = None
        clone_i = 0
        for i in range(int(match)):
            clone_i = i + 1
            self.showLog(f'Bắt đầu trận thứ [{i + 1}/{match}]', self.account['mail'])
            wait.until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
            saveHistoryPoint = i + 1

            # Save history 1 time every 5 matches
            if saveHistoryPoint % 5 == 0:
                time.sleep(3)
                try:
                    self.showLog('Đang lưu lịch sử trận đấu...', self.account['mail'])
                    History.writeHistory(self.driver, 20)
                    self.showLog('Xong', self.account['mail'])
                except Exception as e:
                    self.showLog('Lỗi lưu lịch sử:' + e, self.account['mail'])
                finally:
                    checkPoint = saveHistoryPoint

            # Start
            try:
                self.checkPoint0(self.account['mail'])
            except:
                q = None
                while (q != 0):
                    self.driver.refresh()
                    saveHistoryPoint = self.checkErr()
                    if saveHistoryPoint != -2: q = self.tryAgain(saveHistoryPoint)
        time.sleep(3)

        # Save history when time < 5
        x = clone_i - checkPoint
        if x > 0:
            try:
                self.showLog('Đang lưu lịch sử trận đấu...', self.account['mail'])
                History.writeHistory(self.driver, x)
                self.showLog('Xong', self.account['mail'])
            except:
                self.showLog('Lỗi lưu lịch sử', self.account['mail'])
            finally:
                self.driver.quit()
        return 'Q'

    def findMatch(self):
        time.sleep(1)
        self.driver.execute_script("document.getElementsByClassName('big_category_btn red')[0].click();")
        self.showLog('Đang tìm đối thủ...', self.account['mail'])

    def joinMatch(self):
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
        time.sleep(1)
        mana = self.driver.find_element(By.CSS_SELECTOR,
            'div.col-md-3:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
        self.team = Team.teamSelector(mana)
        self.showLog('Đang khởi tạo đội hình...', self.account['mail'])
        self.driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")

    def createTeam(self):
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
        self.showLog('Đang chọn thẻ bài...', self.account['mail'])
        time.sleep(7)
        self.driver.execute_script(
            "var team = " + self.team + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")

    def startMatch(self):
        self.showLog('Đang chờ đối thủ...', self.account['mail'])
        WebDriverWait(self.driver, 150).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
        self.driver.execute_script("document.getElementsByClassName('btn-battle')[0].click()")
        self.showLog('Đang bắt đầu trận...', self.account['mail'])
        time.sleep(3.5)
        self.showLog('Đang bỏ qua...', self.account['mail'])
        self.driver.execute_script("document.getElementsByClassName('btn-battle')[1].click()")

    def skipMatch(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
        self.driver.execute_script("document.getElementsByClassName('btn btn--done')[0].click();")
        self.showLog('Kết thúc trận đấu', self.account['mail'])

    def checkErr(self):
        try:
            WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="play_now"]/div/div/div/div/button')))
            return -1
        except:
            pass
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
            return 0
        except:
            pass
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
            return 1
        except:
            pass
        try:
            WebDriverWait(self.driver, 1).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
            return 2
        except:
            pass
        try:
            WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
            return 3
        except:
            pass
        try:
            WebDriverWait(self.driver, 1.5).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
            return 4
        except:
            pass
        return -2

    def checkPoint0(self):
        try:
            self.findMatch()
            self.checkPoint1()
            return 0
        except:
            return -1

    def checkPoint1(self):
        try:
            self.joinMatch()
            self.checkPoint2()
            return 0
        except:
            return -1

    def checkPoint2(self):
        try:
            self.createTeam()
            self.checkPoint3()
            return 0
        except:
            return -1

    def checkPoint3(self):
        try:
            self.startMatch()
            self.checkPoint4()
            return 0
        except:
            return -1

    def checkPoint4(self):
        try:
            self.skipMatch()
            return 0
        except:
            return -1

    def tryAgain(self, x):
        c = -1
        if x == -1:
            self.driver.get('https://splinterlands.com/?p=battle_history')
            self.checkPoint0()
        elif x == 0:
            c = self.checkPoint0()
        elif x == 1:
            c = self.checkPoint1()
        elif x == 2:
            c = self.checkPoint2()
        elif x == 3:
            c = self.checkPoint3()
        elif x == 3:
            c = self.checkPoint4()
        return c




class multiBattle(Battle):
    def __init__(self):
        super.__init__()

    def run(self, match, account_list):
        if len(account_list) == 1:
            self.start(match)
        else:
            try:
                proc = {}
                for i in range(len(account_list)):
                    keys = 'p' + str(i + 1)
                    proc[keys] = multiprocessing.Process(target=self.start, args=(match, account_list[i]))
                for b in proc:
                    proc[b].start()
                response = requests.get(
                    'https://raw.githubusercontent.com/tmkha/Splint/main/splint.py')
                if response:
                    File('splint.py').wText(response.text)
                for k in proc:
                    proc[k].join()
            finally:
                os.remove('splint.py')




def pick():
    account_list = [{'mail': 'admin', 'pwd': 'admin',}, {'mail': 'user', 'pwd': 'user',}]
    account_selected = []
    if len(account_list) > 0:
        select = None
        while (select != 'Q'):
            os.system('cls')
            Team.checkTeam()
            print("CHỌN TÀI KHOẢN")
            print(f'\nĐã chọn {len(account_selected)} tài khoản')
            if len(account_selected) > 0:
                t = 1
                for account in account_selected:
                    print(f"{t}. {account['mail']}")
                    t += 1
            print('\n\n')
            print('_' * 30)
            if len(account_list) >= 0:
                j = 1
                for k in account_list:
                    print(f'[{j}] {k["mail"]}')
                    j += 1
                print('\n[S] Bắt đầu    |    [C] Xoá lựa chọn trước đó    |    [Q] Thoát')
                select = input('>> Chọn: ').upper()
                if select.isdigit() and int(select) - 1 < len(account_list) and int(select) - 1 >= 0:
                    select = int(select)
                    select -= j
                    account_selected.append(account_list[select])
                    account_list.pop(select)
                elif select == 'S' and len(account_selected) > 0:
                    os.system('cls')
                    match = input('Số trận đấu: ')

                    while (not (match.isdigit() and int(match) > 0)):
                        os.system('cls')
                        print('Vui lòng nhập một số!')
                        match = input('Số trận đấu: ')
                    print('Da chay/289')
                    time.sleep(1)
                    os.system('cls')

                elif select == 'S' and len(account_selected) == 0:
                    print('Vui lòng chọn ít nhất một tài khoản!')
                    time.sleep(1)
                elif select == 'C' and len(account_selected) > 0:
                    account_list.append(account_selected[-1])
                    account_selected.pop(-1)
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


pick()