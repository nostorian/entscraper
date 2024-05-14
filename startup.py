import os
import time
import json
from pystyle import *
from colorama import Fore, init
from entrar_backend import Scraper


init(convert=True)

def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return

def execution():
    os.system("title EntScraper")
    # check if credentials.json exists and if it doesn't, create it
    if not os.path.exists("credentials.json"):
        with open("credentials.json", "w") as f:
            f.write('{"username": "", "password": ""}')
        return False
    # check if the file is empty
    elif os.stat("credentials.json").st_size == 0:
        with open("credentials.json", "w") as f:
            f.write('{"username": "", "password": ""}')
        return False
    # check if values are empty
    elif os.stat("credentials.json").st_size != 0:
        with open("credentials.json", "r") as f:
            data = json.load(f)
            if data.get("username") == "" or data.get("password") == "":
                return False
            else:
                return True
            

def main():
    clear()
    startup_ch = Write.Input("(?) Do you want to continue with joining(y/n)?: ", color=Colors.light_blue, interval=0.00)
    if startup_ch.lower() == "n":
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Exiting...{Fore.RESET}")
        input()
        exit()
    elif startup_ch.lower() == "y":
        pass
    else:
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid option{Fore.RESET}")
        time.sleep(3)
        main()
    if not execution():
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}we don roll like that g get sum credentials to fw the startup shi{Fore.RESET}")
        input()
        exit()
    with open("credentials.json", "r") as f:
        data = json.load(f)
        username = data.get("username")
        password = data.get("password")
    e = Scraper(username, password, False)
    try:
        e.join_online_class()    
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Exiting...{Fore.RESET}")
            exit()
        else:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}An error occured: {e}{Fore.RESET}")
            exit()


if __name__ == "__main__":
    main()