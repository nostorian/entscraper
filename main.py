# made with hands by nostorian, discord: @fw.nos
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

def create_startup_script():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    f = open(startup_path + "\\entStartup.bat", "w")
    f.write("@echo off\n")
    f.write("cd " + f"\"{startup_path}" + "\\EntScraper\"\n")
    f.write("python " + f"\"{startup_path}" + "\\EntScraper\\startup.py\"\n")
    f.write("pause\n")
    f.close()

def add_to_startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    folderName = "EntScraper"
    os.makedirs(os.path.join(startup_path, folderName), exist_ok=True)
    os.system(f'copy entrar_backend.py "{os.path.join(startup_path, folderName)}" >logs')
    os.system(f'copy startup.py "{os.path.join(startup_path, folderName)}" >logs')
    os.system(f'copy credentials.json "{os.path.join(startup_path, folderName)}" >logs')
    create_startup_script()
    
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Added to startup{Fore.RESET}")

def main():
    clear()
    banner = """
┏┓   ┏┓           
┣ ┏┓╋┗┓┏┏┓┏┓┏┓┏┓┏┓
┗┛┛┗┗┗┛┗┛ ┗┻┣┛┗ ┛ 
            ┛     
"""
    Write.Print(Center.XCenter(banner), color=Colors.red, interval=0.00)
    print("\n")
    Write.Print(Center.XCenter("Kindly be mindful of your usage of this tool."), color=Colors.cyan, interval=0.00)
    print("\n\n")
    if not execution():
        username = Write.Input("(->) Enter your username: ", color=Colors.green, interval=0.00).upper()
        password = Write.Input("(->) Enter your password: ", color=Colors.green, interval=0.00)
        # Save the entered credentials to the JSON file
        with open("credentials.json", "w") as f:
            json.dump({"username": username, "password": password}, f)
    else:
        with open("credentials.json", "r") as f:
            data = json.load(f)
            username = data["username"]
            password = data["password"]
    scraping_choice = Write.Input("(?) Do you want to scrape data to json(y/n)?: ", color=Colors.light_blue, interval=0.00)
    # CHECK IF ANY OF THEM IS EMPTY
    if username == "" or password == "":
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Please fill in all fields.{Fore.RESET}")
        input("Press any key to continue...")
        main()
    if scraping_choice == "y" or scraping_choice == "Y":
        scrape = True
    elif scraping_choice == "n" or scraping_choice == "N":
        scrape = False
    else:
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid choice, defaulting to no scraping.{Fore.RESET}")
        scrape = False
    e = Scraper(username, password, scrape)
    try:
        u = e.get_username()
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Logged in as {u}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}An error occurred: {e}{Fore.RESET}")
        input()
    
    # print please wait message
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Setting up the tool, please wait...{Fore.RESET}")
    time.sleep(3)
    clear()
    
    # print the banner again
    Write.Print(Center.XCenter(banner), color=Colors.red, interval=0.00)
    print("\n")
    Write.Print(Center.XCenter("Kindly be mindful of your usage of this tool."), color=Colors.cyan, interval=0.00)
    print("\n")
    # print logged in as username
    print(f"\n{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Logged in as {u}{Fore.RESET}")
    print("\n\n")
    # print the options
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}1{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Get Announcements{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}2{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Get Assignments{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}3{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Join Online Class{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}4{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Add to Startup{Fore.RESET}")
    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}5{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Exit{Fore.RESET}")

    choice = Write.Input("(->) Enter your choice: ", color=Colors.green, interval=0.00)
    choices = ["1", "2", "3", "4", "5"]
    if choice not in choices:
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid choice!{Fore.RESET}")
        input("Press any key to continue...")
        main()
    if choice == "1":
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Fetching announcements...{Fore.RESET}")
        try:
            announcements = e.scrape_announcements()
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Announcements fetched successfully.{Fore.RESET}")
            print("\n")
            for announcement in announcements:
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.YELLOW}{announcement['announcement_tag']}: {announcement['announcement']}{Fore.RESET}")
            input()
        except Exception as e:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}An error occurred: {e}{Fore.RESET}")
            input()
    elif choice == "2":
        download_choice = Write.Input("(?) Do you want to download the attachments(y/n)?: ", color=Colors.light_blue, interval=0.00)
        if download_choice == "y" or download_choice == "Y":
            download = True
        elif download_choice == "n" or download_choice == "N":
            download = False
        else:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid choice, defaulting to no downloading.{Fore.RESET}")
            time.sleep(3)
            download = False
        # the only subjects available are: {"physics": "91", "english": "92", "maths": "98", "computers": "124", "chemistry": "138", "economics": "139"}
        # print menu
        clear()
        Write.Print(Center.XCenter(banner), color=Colors.red, interval=0.00)
        print("\n")
        Write.Print(Center.XCenter("Kindly be mindful of your usage of this tool."), color=Colors.cyan, interval=0.00)
        print("\n")
        # print logged in as username
        print(f"\n{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Logged in as {u}{Fore.RESET}")
        print("\n\n")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}1{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Physics{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}2{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}English{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}3{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Maths{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}4{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Computers{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}5{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Chemistry{Fore.RESET}")
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}6{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.WHITE}Economics{Fore.RESET}")
        subject = Write.Input("(->) Enter the choice of subject: ", color=Colors.green, interval=0.00)
        try:
            a = {"1": "physics", "2": "english", "3": "maths", "4": "computers", "5": "chemistry", "6": "economics"}
            subject = a[subject]
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Fetching assignments...{Fore.RESET}")
            assignments = e.scrape_assignments(subject, download_links=download)
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Assignments fetched successfully.{Fore.RESET}")
            print("\n")
            for assignment in assignments:
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}{assignment['assign_tag']}: {assignment['assign_desc']}:-\n{Fore.WHITE}Assignment Link: {assignment['attach_link']}\nIssued Date: {assignment['start_date']}\nDue Date: {assignment['end_date']}{Fore.RESET}")
                print("\n\n")
            input("Press any key to continue...")
            main()
        except Exception as e:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}An error occurred: {e}{Fore.RESET}")
            input()
    
    elif choice == "3":
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Attempting to join online class...{Fore.RESET}")
        try:
            e.join_online_class()
        except Exception as e:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}An error occurred: {e}{Fore.RESET}")
            input()
    elif choice == "5":
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Exiting...{Fore.RESET}")
        input("Press any key to continue...")
        return
    elif choice == "4":
        # add a warning  confirmation
        w_ch = Write.Input("(?) Are you sure you want to add this tool to startup(y/n)?: ", color=Colors.light_blue, interval=0.00)
        if w_ch.lower() == "y":
            # check if the tool is already in startup
            startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
            if os.path.exists(startup_path + "\\entStartup.bat") and os.path.exists(startup_path + "\\EntScraper"):
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}The tool is already in startup!{Fore.RESET}")
                input("Press any key to continue...")
                main()
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Adding to startup...{Fore.RESET}")
            time.sleep(5)
            add_to_startup()
            input("Press any key to continue...")
            main()
        elif w_ch.lower() == "n":
            # tell them aight 
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Alright, not adding to startup.{Fore.RESET}")
            input("Press any key to continue...")
            main()
        else:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid choice!{Fore.RESET}")
            input("Press any key to continue...")
            main()
    else:
        print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}!{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid choice!{Fore.RESET}")
        input("Press any key to continue...")
        main()
main()
