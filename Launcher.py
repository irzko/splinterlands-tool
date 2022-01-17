import os, time, requests

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

def download_resource():
    print('\n\n\n\n\n\n\n')
    print(logo)
    print('\t\t\t\t\t           Đang tải dữ liệu...')
    response = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/splint.py')
    if response:
        with open('splint.py', mode="w", encoding="utf-8") as f:
            f.write(response.text)
            f.close()
    else: print(response)

if __name__ == "__main__":
    os.system('title Splint Tool')
    try:
        download_resource()
        from splint import Launcher
        Launcher.menu()
    except Exception as e:
        os.system('cls')
        print('\n\n\n\n\n\n\n')
        print(logo)
        print('Lỗi:', e)
        os.system('pause>nul|set/p =Nhấn phím bất kì để thoát ...')