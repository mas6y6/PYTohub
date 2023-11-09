import os
import time
import subprocess
import requests
from .legohub import listallports, hubconnection
from .menu import main_menu, second_menu
from getkey import getkey, keys

conn = None
processes = {}
ports = []
retry = False
hub = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

class textcolors:
    HEADER = "\033[95m"
    BACKGROUND = "\033[107m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def print_text_logo():
    print(""" ______   __  __     ______   ______     __  __     __  __     ______    
/\  == \ /\ \_\ \   /\__  _\ /\  __ \   /\ \_\ \   /\ \/\ \   /\  == \   
\ \  _-/ \ \____ \  \/_/\ \/ \ \ \/\ \  \ \  __ \  \ \ \_\ \  \ \  __<   
 \ \_\    \/\_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_/     \/_____/     \/_/   \/_____/   \/_/\/_/   \/_____/   \/_____/                                                                      
""")

class log:
    def fatul(text,exitcode=1):
        print(
            textcolors.FAIL
            + textcolors.BOLD
            + "[FATUL] "
            + text
            + " ("
            + str(exitcode)
            + ")"
            + textcolors.END
        )
        exit(exitcode)
    
    def error(text):
        print(
            textcolors.FAIL
            + "[ERROR] "
            + text
            + textcolors.END
        )
    
    def warning(text):
        print(
            textcolors.WARNING
            + "[WARNING] "
            + text
            + textcolors.END
        )
    
    def success(text):
        print(
            textcolors.OKGREEN
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
        
    def successblue(text):
        print(
            textcolors.OKBLUE
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
    
    def successcyan(text):
        print(
            textcolors.OKCYAN
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
    
    def log(text):
        print(
            "[INFO] "
            + text
        )

def findhub():
    o = 0
    ports = listallports()
    if ports == []:
        log.warning("There is no hubs connected to this computer.")
        print("Start the program on the hub before running PYToHub to list the hub")
        log.fatul("Terminated",exitcode=1)
    elif len(ports) == 1:
        print("There is only one hub connected to this computer do you want to connect it (Y/n)")
        
        
    while True:
        clear()
        print("Please select one of your hubs below")
        print("↑↑↑")
        print(ports[o])
        print("↓↓↓")
        print()
        print(f"{o + 1} out of {len(ports)}")
        print()
        print("Navigate using UP/DOWN arrow keys")
        print("Press Q to exit program")
        key = getkey()
        if key == keys.UP:
            if not o == len(ports) - 1:
                o += 1
        elif key == keys.DOWN:
            if not o == 0:
                o -= 1
        elif key == keys.ENTER:
            clear()
            return ports[o]
        elif key == 'q':
            exit()
        else:
            pass

def tryconnect(r):
    global hub, retry
    for i in range(11):
        if i == 10:
            log.error("Failed to connect to hub (Maybe you disconnected it?)")
            log.fatul("Terminated",exitcode=1)
            
        log.log("Connecting...")
        try:
            if retry == False:
                hub = hubconnection(r)
            

            if hub.send_ping(None) == None:
                log.warning("No data. retrying...")
            else:
                log.success("Connected")
                time.sleep(1)
                log.log("Loading main menu...")
                break
        except Exception as e:
            log.error(f"An error occurred ({e}). Retrying...")

def start_main_menu():
    while True:
        out = main_menu()
        if out[1] == 0:
            log.log("Restarting hub Please wait...")
            hub.send_command("end_conn",[])
            log.success("Command sent")
            log.log("Your hub will restart because if you uploaded data to it changes directorys and glitches the hub")
            exit()
        elif out[1] == 1:
            out2 = second_menu()
        else:
            pass

def run(args=None):
    global hub
    clear()
    print(textcolors.BOLD+textcolors.HEADER+"PYToHub is made by @mas6y6 on github\n"+textcolors.END)
    time.sleep(3)
    while True:
        if not hub == None:
            start_main_menu()
        r = findhub()
        tryconnect(r)