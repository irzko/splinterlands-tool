class Battle:

    def initDriver():
        options = webdriver.ChromeOptions()
        #chrome_options.add_argument("user-data-dir="+filePath)
        driver = webdriver.Chrome('chromedriver', options = options)
        return driver

    def status(stt, mail):
        named_tuple = time.localtime()
        time_string = time.strftime("%H:%M:%S", named_tuple)
        print(f'[{time_string}] [{mail}] {stt}')

    def start(match, acc):
        Battle.status('Đang khởi động trình duyệt...', acc['mail'])
        driver = Battle.initDriver()
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
            Battle.status('Đang tìm đối thủ...', acc['mail'])

        def checkPoint_1():
            nonlocal team
            nonlocal mana
            wait.until(EC.visibility_of_element_located(
                (By.XPATH, "/html/body/div[3]/div/div/div/div[2]/div[3]/div[2]/button")))
            time.sleep(1)
            mana = driver.find_element_by_css_selector(
                'div.col-md-3:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)').text
            team = team.teamSelector(mana)
            Battle.status('Đang khởi tạo đội hình...', acc['mail'])
            driver.execute_script("document.getElementsByClassName('btn btn--create-team')[0].click();")

        def checkPoint_2():
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="page_container"]/div/div[1]/div')))
            Battle.status('Đang chọn thẻ bài...', acc['mail'])
            time.sleep(7)
            driver.execute_script(
                "var team = " + team + ";for (let i = 0; i < team.length; i++) {let card = document.getElementsByClassName('card beta');let cimg = document.getElementsByClassName('card-img');var reg = /[A-Z]\\w+( \\w+'*\\w*)*/;for (let j = 0; j < card.length; j++){let att_card = card[j].innerText;let result = att_card.match(reg);let name = result[0];if (name == team[i]){cimg[j].click();break;}}}document.getElementsByClassName('btn-green')[0].click();")

        def checkPoint_3():
            Battle.status('Đang chờ đối thủ...', acc['mail'])
            WebDriverWait(driver, 150).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#btnRumble')))
            driver.execute_script("document.getElementsByClassName('btn-battle')[0].click()")
            Battle.status('Đang bắt đầu trận...', acc['mail'])
            time.sleep(3.5)
            Battle.status('Đang bỏ qua...', acc['mail'])
            driver.execute_script("document.getElementsByClassName('btn-battle')[1].click()")

        def checkPoint_4():
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="dialog_container"]/div/div/div/div[1]/h1')))
            driver.execute_script("document.getElementsByClassName('btn btn--done')[0].click();")
            Battle.status('Kết thúc trận đấu', acc['mail'])

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
                Battle.checkPoint_0()
                Battle.isCheckPoint_1()
                return 0
            except:
                return -1

        def isCheckPoint_1():
            try:
                Battle.checkPoint_1()
                Battle.isCheckPoint_2()
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
            status(f'Bắt đầu trận thứ [{i + 1}/{match}]', acc['mail'])
            wait.until(EC.visibility_of_element_located((By.ID, "battle_category_btn")))
            vf = i + 1
            if vf % 5 == 0:
                time.sleep(3)
                try:
                    status('Đang lưu lịch sử trận đấu...', acc['mail'])
                    history.writeHistory(driver, 20)
                    status('Xong', acc['mail'])
                except Exception as e:
                    status('Lỗi lưu lịch sử:' + e, acc['mail'])
                finally:
                    check_point = vf
            try:
                Battle.isCheckPoint_0()
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
                status('Đang lưu lịch sử trận đấu...', acc['mail'])
                history.writeHistory(driver, times_when_smaller_20)
                status('Xong', acc['mail'])
            except:
                status('Lỗi lưu lịch sử', acc['mail'])
            finally:
                driver.quit()
        return 'Q'

    def multiBattle():
        accounts_list = []
        if len(account.account) > 0:
            select = ''
            while (select != 'Q'):
                os.system('cls')
                team.checkTeam()
                print("CHỌN TÀI KHOẢN")
                print(f'\nĐã chọn {len(accounts_list)} tài khoản')
                if len(accounts_list) > 0:
                    t = 1
                    for account in accounts_list:
                        print(f"{t}. {account['mail']}")
                        t += 1
                print('\n\n')
                print('_' * 30)
                if len(account.account) >= 0:
                    j = 1
                    for k in account.account:
                        print(f'[{j}] {k["mail"]}')
                        j += 1
                    print('\n[S] Bắt đầu    |    [C] Xoá lựa chọn trước đó    |    [Q] Thoát')
                    select = input('>> Chọn: ').upper()
                    if select.isdigit() and int(select) - 1 < len(account.account) and int(select) - 1 >= 0:
                        select = int(select)
                        select -= j
                        accounts_list.append(account.account[select])
                        account.account.pop(select)
                    elif select == 'S' and len(accounts_list) > 0:
                        os.system('cls')
                        match = input('Số trận đấu: ')
                        while (not (match.isdigit() and int(match) > 0)):
                            os.system('cls')
                            print('Vui lòng nhập một số!')
                            match = input('Số trận đấu: ')
                        os.system('cls')
                        if len(accounts_list) == 1:
                            start(match, accounts_list[0])
                        else:
                            try:
                                pross = {}
                                for i in range(len(accounts_list)):
                                    keys = 'p' + str(i + 1)
                                    pross[keys] = multiprocessing.Process(target=start, args=(match, acc[i]))
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