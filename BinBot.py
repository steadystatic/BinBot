import random
import requests
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import codecs
from os import getcwd, path

# Author: Mili
# Python Version: 3.6.0
# No API key needed

#
# Variables, Setup, and Misc
#



user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']

key_list = []


taglist = ['<textarea class="paste_code" id="paste_code" name="paste_code" onkeydown="return catchTab(this,event)">',
           '<textarea class="paste_textarea" id="paste_code" name="paste_code" onkeydown="return catchTab(this,event)" rows="10">',
           '</textarea>']

archive_url = "https://pastebin.com/archive/text"

url_foundation = "https://pastebin.com"

curdir = getcwd()

ConnectError = "<title>Pastebin.com - Page Removed</title>"

AccessDeniedError = "access denied"



#
# Functions
#

def random_headers():
    return {'User-Agent': random.choice(user_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

def archive_connect():
    archive_page = requests.get(archive_url,headers=random_headers())
    today = datetime.now().strftime('%x')
    now = datetime.now().strftime('%X')
    creationdate = today + '~' + now
    identifier = creationdate.replace("/", ".").replace(":", "-")
    archive_filename = "[" + str(identifier) + "]"
    return archive_page, archive_filename

def archive_engine(prescan_text):
    for k in key_list:
        if k in prescan_text:
            today = datetime.now().strftime('%x')
            now = datetime.now().strftime('%X')
            creationdate = today + '~' + now
            keyfilename = "[Keyword-" + str(k) + "]" + str(creationdate).replace("/", ".").replace(":", "-")
            keyfi = codecs.open(str(workpath)+str(keyfilename).replace(":", "-").replace(":", "-").replace("/", "-") + ".txt", 'w+', 'utf-8')
            keyfi.write(prescan_text)
            keyfi.close()
        else:
            pass

def ArchiveSearch(stop):
    arch_runs = 0
    while True:
        amode_input = input("[r]aw or [f]iltered search (filtered search will make use of the ArchiveEngine and will return fewer results): ")
        if amode_input.lower() == 'r':
            arch_mode = 'r'
            break
        elif amode_input.lower() == 'f':
            arch_mode = 'f'
            while True:
                keyword_input = input(
                    "Enter the keywords you'd like to search for, seperated by a comma: ").split(",")
                for k in keyword_input:
                    key_list.append(k)
                break
            break
        else:
            print("Invalid Input.")
            continue
    while True:
        if arch_runs > 0:
            if arch_runs >= stop:
                print("Operation Finished... [" + str(datetime.now().strftime('%X')) + "]")
                exit()
            print("Pastes fetched, cooling down for "+str(cooldown)+" seconds... ["+str(datetime.now().strftime('%X'))+"]")
            sleep(cooldown/2)
            print("Halfway through at ["+str(datetime.now().strftime('%X'))+"]")
            sleep(cooldown/2)
            print("resuming... ["+str(datetime.now().strftime('%X'))+"]")
        if arch_runs < stop or stop == 0:
            arch_page, arch_filename = archive_connect()
            arch_soup = BeautifulSoup(arch_page.text, 'html.parser')
            sleep(2)
            print("Getting archived pastes... ["+str(datetime.now().strftime('%X'))+"]")
            if AccessDeniedError in arch_page.text:
                print("IP Temporarily suspending, pausing until the ban is lifted. Estimated time: one hour... ["+str(datetime.now().strftime('%X'))+"]")
                sleep(cooldown)
                print("Process resumed... ["+str(datetime.now().strftime('%X'))+"]")
                continue
            else:
                pass
            print("Finding params... ["+str(datetime.now().strftime('%X'))+"]")


            table = arch_soup.find("table", class_="maintable") # Fetch the table of recent pastes
            while True:
                try:
                    tablehrefs = table.findAll('a', href=True) # Find the <a> tags for every paste
                    break
                except AttributeError:
                    print("IP Temporarily suspending, pausing until the ban is lifted. Estimated time: one hour... ["+str(datetime.now().strftime('%X'))+"]")
                    sleep(cooldown)
                    print("Process resumed... ["+str(datetime.now().strftime('%X'))+"]")
                    continue

            for h in tablehrefs:
                proch = h['href'] # fetch the URL param for each paste
                print("params fetched... ["+str(datetime.now().strftime('%X'))+"]")
                print("Acting on params... ["+str(datetime.now().strftime('%X'))+"]")
                full_arch_url = url_foundation + proch # Generate URLs by adding the processed parameter to the base URL
                full_archpage = requests.get(full_arch_url, headers=random_headers())
                sleep(5)
                item_soup = BeautifulSoup(full_archpage.text, 'html.parser')
                unprocessed = item_soup.find('textarea') # Fetch the raw text in the paste.
                for e in taglist:
                    unprocessed = str(unprocessed).replace(e, "") # process the raw text by removing all html elements
                if arch_mode == 'r':
                    if path.isdir(workpath) is True:
                        arch_final_file = codecs.open(str(workpath) + str(full_arch_url).replace(":", "-")
                                                      .replace(":", "-").replace("/", "-") + ".txt", 'w+', 'utf-8')
                        arch_final_file.write(unprocessed)
                        arch_final_file.close()
                        arch_runs += 1
                        continue
                    else:
                        print("Making directory... ["+str(datetime.now().strftime('%X'))+"]")
                        arch_final_file = codecs.open(str(workpath) + str(full_arch_url).replace(":", "-")
                                                      .replace(":", "-").replace("/", "-") + ".txt", 'w+', 'utf-8')
                        arch_final_file.write(unprocessed)
                        arch_final_file.close()
                        arch_runs += 1
                        continue
                elif arch_mode == 'f':
                    if path.isdir(workpath) is True:
                        print("Running engine... ["+str(datetime.now().strftime('%X'))+"]")
                        archive_engine(unprocessed)
                        arch_runs += 1
                        continue
                    else:
                        print("Running engine... ["+str(datetime.now().strftime('%X'))+"]")
                        archive_engine(unprocessed)
                        arch_runs += 1
                        continue
        else:
            print("Operation Finished... ["+str(datetime.now().strftime('%X'))+"]")
            break



if __name__ == "__main__":

    print("""
    _________________________________________
    [                                       ]
    [                                       ]
    [          Welcome to BinBot            ]
    [            Made by Mili               ]
    [                                       ]
    [_______________________________________]
    """)

    while True:
        workpath = input("Enter the path you wish to save text documents to (enter curdir for current directory): ")
        if workpath.lower() == 'curdir':
            workpath = curdir
        if path.isdir(workpath):
            print("Valid Path...")
                        if workpath.endswith('\\'):
                pass
            else:
                workpath = workpath + str('\\')
            break
        else:
            print("Invalid path, check input...")
            continue

    while True:
        try:
            stop_input = int(input("Enter the amount of successful pulls you wish to make (enter 0 for infinite): "))
            limiter = int(input("Enter the request limit you wish to use (recommended: 5): "))
            cooldown = int(input("Enter the cooldown between IP bans/Archive scrapes (recommended: 1200): "))
            break
        except ValueError:
            print("Invalid Input.")
            continue

    ArchiveSearch(stop_input)