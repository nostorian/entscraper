# made withhands by fw-real, discord: @nostorian
import os
import re
import json
import time
import requests
import threading
import urllib.parse as urlparse
from pystyle import *
from os.path import splitext
from bs4 import BeautifulSoup

from datetime import datetime
from colorama import Fore, init
import chromedriver_autoinstaller
from seleniumwire import webdriver





class Scraper:
    """
    A class used to scrape assignments and announcements from entrar.in

    ## Parameters
    ----------
    username : str
        The username of the student
    password : str
        The password of the student
    save_data : bool
        Whether to save the scraped data to a json file or not
        By default it is set to False

    ## Methods
    ----------
    scrape_assignments(subject)
        Scrapes the assignments of the given subject and returns a list of dictionaries
    scrape_announcements()
        Scrapes the announcements and returns a list of dictionaries
    join_online_class()
        Joins the first online class available for today


    """
    def __init__(self, username, password, save_data=False):
        self.username = username
        self.password = password
        self.save_data = save_data
        self.subject_dict = {"physics": "91", "english": "92", "maths": "98", "computers": "124", "chemistry": "138", "economics": "139"}
        self.session = None
    
    def _download_chrome_driver(self):
        chromedriver_autoinstaller.install()

    def _login(self):
        login_url = 'https://entrar.in/login/auth/'
        login_payload = {
            'username': self.username,
            'password': self.password
        }
        self.session = requests.Session()
        real = self.session.post(login_url, data=login_payload)
        auth_soup = BeautifulSoup(real.text, 'html.parser')
        if auth_soup.find('li', class_='user-profile header-notification') == None:
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}Invalid Credentials were provided.{Fore.RESET}")
            exit()
        

    def _get_headers(self):
        phpsessid = self.session.cookies.get('PHPSESSID')
        serverid = self.session.cookies.get('SERVERID')
        cflb = self.session.cookies.get('__cflb')

        headers = {
            "Accept-Language": "en-US,en;q=0.6",
            "Cookie": f"PHPSESSID={phpsessid}; SERVERID={serverid}; __cflb={cflb}",
            "Origin": "https://entrar.in",
            "Referer": "https://entrar.in/pp_assignment/classassignment",
            "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Brave\";v=\"116\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Gpc": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        }
        return headers

    def get_username(self):
        self._login()
        headers = self._get_headers()
        r = self.session.get("https://entrar.in/parent_portal/student_full_profile", headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        user_profile = soup.find('li', class_='user-profile header-notification')
        user_name = user_profile.find('span').text.strip()
        return user_name

    def scrape_assignments(self, subject, download_links=False):
        if subject not in self.subject_dict:
            raise Exception("Subject not found! Either Invalid Credentials or Invalid Subject were provided.")
        self._login()
        headers = self._get_headers()
        data = {"search_assignment": True}
        r = self.session.post("https://entrar.in/pp_assignment/classassignment", headers=headers, data=data)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        assignment_data = soup.find('div', id=self.subject_dict[subject], class_='panel-collapse collapse in', role="tabpanel")
        assignment_table = assignment_data.find('table', class_='table table-striped table-bordered table-styling table-xs')

        assignment_list = []

        def scrape_assignment_data(row):
            columns = row.find_all('td')
            s_no = columns[0].text.strip()
            subject_data = columns[1].text.strip()  # convert to list
            subject, teacher = subject_data.split('/')
            assignment_tag = columns[2].text.strip()
            assignment_description = columns[3].text.strip()
            start_date = columns[4].text.strip() # convert to list
            start_list = start_date.split('/')
            attachment_link = columns[6].find('a')['href'] if columns[6].find('a') else None

            text = start_list[0]
            words = re.findall(r'\b\w+\b', text)
            start_date = None
            end_date = None

            # Iterate through the words to find date patterns
            for i in range(len(words) - 2):
                if words[i] == "Start" and words[i + 1] == "Date":
                    start_date = words[i + 2] + "-" + words[i + 3] + "-" + words[i + 4]
                elif words[i] == "End" and words[i + 1] == "Date":
                    end_date = words[i + 2] + "-" + words[i + 3] + "-" + words[i + 4]

            # Create a dictionary for the current assignment
            assignment_dict = {
                "s_no": s_no,
                "subject": subject,
                "teacher": teacher,
                "assign_tag": assignment_tag,
                "assign_desc": assignment_description,
                "start_date": start_date,
                "end_date": end_date,
                "attach_link": attachment_link
            }

            # Append the assignment dictionary to the list
            assignment_list.append(assignment_dict)

        threads = []
        for row in assignment_table.find_all('tr')[1:]:
            thread = threading.Thread(target=scrape_assignment_data, args=(row,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if self.save_data == True:
            with open("assignments.json", "w") as f:
                json.dump(assignment_list, f, indent=4)

            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Assignments saved to {Fore.YELLOW}assignments.json{Fore.RESET}")
        
        # what if user wants every assignment link to be downloaded 
        if download_links == True:
            for assignment in assignment_list:
                if not os.path.exists(subject):
                    os.mkdir(subject)
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTBLUE_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.LIGHTBLUE_EX}Downloading {assignment['assign_tag']}...{Fore.RESET}")
                if assignment['attach_link'] != None:
                    attachment_link = assignment['attach_link']
                    attachment_name = attachment_link.split('/')[-1]
                    attachment = self.session.get(attachment_link, headers=headers)
                    attachment_name = os.path.join(subject, assignment['assign_tag'])
                    file_ext = splitext(urlparse.urlparse(attachment_link).path)[1]
                    with open(f"{attachment_name}{file_ext}", 'wb') as f:
                        f.write(attachment.content)
                    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Downloaded {os.path.join(os.getcwd(), f'{attachment_name}{file_ext}')}{Fore.RESET}")
                else:
                    print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}No attachment link available for {assignment['assign_tag']}{Fore.RESET}")

        return assignment_list

    def scrape_announcements(self):
        self._login()
        headers = self._get_headers()
        data = {"announcementlist": True, "session": "undefined"}
        r = self.session.post("https://entrar.in/pp_announcement/announcement", headers=headers, data=data)

        soup = BeautifulSoup(r.text, 'html.parser')
        announcement_table = soup.find('table', class_='table table-striped table-bordered nowrap', id='simpletable')
        if announcement_table == None:
            raise Exception("Invalid Credentials were provided.")

        announcement_list = []

        def scrape_announcement_data(row):
            columns = row.find_all('td')
            s_no = columns[0].text.strip()
            start_date = columns[1].text.strip()
            announcement_tag = columns[2].text.strip()
            announcement = columns[3].text.strip()
            announcement = " ".join(announcement.split())
            attachment_link = columns[4].find('a')['href'] if columns[4].find('a') else None

            announcement_dict = {
                "s_no": s_no,
                "start_date": start_date,
                "announcement_tag": announcement_tag,
                "announcement": announcement,
                "attach_link": attachment_link
            }

            announcement_list.append(announcement_dict)

        threads = []

        for row in announcement_table.find_all('tr')[1:]:
            thread = threading.Thread(target=scrape_announcement_data, args=(row,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if self.save_data == True:
            with open("announcements.json", "w") as f:
                json.dump(announcement_list, f, indent=4)

            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Announcements saved to {Fore.YELLOW}announcements.json{Fore.RESET}")
        return announcement_list
    
    def join_online_class(self):
        self._login()
        headers = self._get_headers()
        today = datetime.today()
        formatted_date = today.strftime("%Y-%m-%d")
        data = {"filter": True, "from": formatted_date}
        r = self.session.post("https://entrar.in/classroom_creation_crm_new/s_display", headers=headers, data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        class_table = soup.find('table', class_='table table-striped table-bordered nowrap table-styling text-wrap')
        if class_table == None:
            raise Exception("Either Invalid Credentials were provided or no classes are available for today.")
        
        class_list = []
        def scrape_class_data(row):
            columns = row.find_all('td')
            s_no = columns[0].text.strip()
            class_title = columns[1].text.strip()
            start_date = columns[2].text.strip()
            duration = columns[3].text.strip()
            try:
                join_link = columns[4].find('a')['href']
            except:
                join_link = "No Link Available"
            class_dict = {
                "s_no": s_no,
                "class_title": class_title,
                "start_date": start_date,
                "duration": duration,
                "join_link": join_link
            }
            class_list.append(class_dict)

        threads = []
        for row in class_table.find_all('tr')[1:]:
            thread = threading.Thread(target=scrape_class_data, args=(row,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        if self.save_data == True:
            with open("online_classes.json", "w") as f:
                json.dump(class_list, f, indent=4)
        
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Online classes saved to {Fore.YELLOW}online_classes.json{Fore.RESET}")
        if len(class_list) == 0:
            raise Exception("No classes available for today.")
        elif class_list[0]["join_link"] == "No Link Available":
            raise Exception("No link available for the class.")
        else:
            durations = int(class_list[0]['duration'].split(' ')[0])
            if not os.path.exists("chromedriver.exe"):
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTRED_EX}-{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.RED}ChromeDriver not found in PATH. Downloading...{Fore.RESET}")
                self._download_chrome_driver()  
                print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}ChromeDriver downloaded successfully.{Fore.RESET}")
            driver = webdriver.Chrome()
            def interceptor(request):
                del request.headers['Accept-Language']
                del request.headers['Cookie']
                del request.headers['Origin']
                del request.headers['Referer']
                del request.headers['Sec-Ch-Ua']
                del request.headers['Sec-Ch-Ua-Mobile']
                del request.headers['Sec-Ch-Ua-Platform']
                del request.headers['Sec-Fetch-Dest']
                del request.headers['Sec-Fetch-Mode']
                del request.headers['Sec-Fetch-Site']
                del request.headers['Sec-Gpc']
                del request.headers['User-Agent']
                request.headers = headers
            
            driver.request_interceptor = interceptor
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}#{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Attempting to join {class_list[0]['class_title']} for {durations} minutes...{Fore.RESET}")
            # run the code for duration of the class from online_classes.json
            driver.get(class_list[0]['join_link'])
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Joined {class_list[0]['class_title']}{Fore.RESET}")
            # run the code for duration of the class
            time.sleep(durations * 60)
            print(f"{Fore.LIGHTBLACK_EX}({Fore.RESET}{Fore.LIGHTGREEN_EX}+{Fore.RESET}{Fore.LIGHTBLACK_EX}){Fore.RESET} {Fore.GREEN}Left {class_list[0]['class_title']}{Fore.RESET}")
            driver.quit()
