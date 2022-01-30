import os, requests

def download_resource():
    response = requests.get('https://raw.githubusercontent.com/tmkha/Splint/main/splint.py')
    if response:
        with open('splint.py', mode="w", encoding="utf-8") as f:
            f.write(response.text)
            f.close()
    else: print(response)

if __name__ == "__main__":
    try:
        download_resource()
        from splint import Launcher
        Launcher.menu()
    except Exception as e:
        os.system('cls')
        print('Lỗi:', e)
        os.system('pause>nul|set/p =Nhấn phím bất kì để thoát ...')