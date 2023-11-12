import os
import time
import sys
import subprocess
import requests
import urllib.request
import tkinter as tk
import tkinter.filedialog as fbox
import tkinter.messagebox as box
from .logging import log
from .textcolors import textcolors
from .legohub import listallports, hubconnection
from .menu import main_menu, second_menu, options_menu
from getkey import getkey, keys
import progressbar
sys.setrecursionlimit(50000)

version = '1.5'
hub_version = 'unknown'
pbar = None
conn = None
processes = {}
ports = []
retry = False
hub = None


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def print_text_logo(version,hub_version):
    print(
        f""" ______   __  __     ______   ______     __  __     __  __     ______    
/\  == \ /\ \_\ \   /\__  _\ /\  __ \   /\ \_\ \   /\ \/\ \   /\  == \   
\ \  _-/ \ \____ \  \/_/\ \/ \ \ \/\ \  \ \  __ \  \ \ \_\ \  \ \  __<   
 \ \_\    \/\_____\    \ \_\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_____\ 
  \/_/     \/_____/     \/_/   \/_____/   \/_/\/_/   \/_____/   \/_____/
  
            (Version: {version}, Hub Version: {hub_version})
                                                                        
""")

def findhub():
    o = 0
    ports = listallports()
    if ports == []:
        log.warning("There is no hubs connected to this computer.")
        print("Start the program on the hub before running PYToHub to list the hub")
        log.fatul("Terminated", exitcode=1)
    elif len(ports) == 1:
        print(
            "There is only one hub connected to this computer do you want to connect it (Y/n)"
        )

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
        elif key == "q":
            exit()
        else:
            pass


def tryconnect(r):
    global hub, retry, hub_version
    log.log("Connecting...")
    for i in range(11):
        if i == 10:
            log.error("Failed to connect to hub (Maybe you disconnected it?)")
            log.fatul("Terminated", exitcode=1)

        try:
            if retry == False:
                hub = hubconnection(r)

            if hub.send_ping(None) == None:
                log.warning("No data. retrying...")
            else:
                log.success("Connected")
                time.sleep(1)
                log.log("Loading hub version")
                hub_version = hub.send_command('version',[])
                if hub_version == None:
                    log.error('Unable to get hub version')
                else:
                    log.log('Received')
                log.log("Loading main menu...")
                break
        except Exception as e:
            log.error(f"An error occurred ({e}). Retrying...")


def upload_file():
    global hub
    log.log("Asking for file to upload...")
    
    window = tk.Tk()
    w = fbox.askopenfilename(
        filetypes=[("Python Files", "*.py")],
    )
    window.destroy()
    log.log(f"Uploading: {w}")
    while True:
        qa = input(f"Do you want to upload {w} (Y/n)")
        if qa == "Y" or qa == "y":
            break
        elif qa == "N" or qa == "n":
            return
        else:
            pass
    filename1 = w.split("/")
    filename = filename1[len(filename1) - 1]
    log.log("Uploading...")
    log.warning("DO NOT DISCONNECT YOUR HUB OR THE FILE WILL BECOME CORRUPTED")
    out = hub.send_command("start_file_upload", [filename])
    time.sleep(1)
    if out["packet-type"] == 4:
        log.error(f"An error occurred: {out['error']}")
        
    widgets = [
        progressbar.Percentage(),
        " ",
        progressbar.ETA(),
        " ",
        textcolors.YELLOW,
        textcolors.BOLD,
        progressbar.Bar(marker="#", left="[", right="]"),
        " ",
        progressbar.Counter(),
        " Lines uploaded",
        textcolors.END
    ]
    f = open(w, "r")
    lines = f.readlines()
    pbar = progressbar.ProgressBar(max_value=len(lines), widgets=widgets)
    pbar.start()
    
    i2 = 0
    for i in lines:
        hub.send_packet(i)
        i2 += 1
        pbar.update(i2)
        time.sleep(0.45)

    log.success("Uploaded successfully")
    log.log("Finishing")
    time.sleep(0.25)
    out = hub.send_command("close_file", [])
    if out["packet-type"] == 4:
        log.error(f"An error occurred: {out['error']}")
        time.sleep(4)
    
    out = hub.send_command("chdir", ['/'])
    if out["packet-type"] == 4:
        log.error(f"An error occurred: {out['error']}")
        time.sleep(4)
    
    out = hub.send_command("chdir", ['modules'])
    if out["packet-type"] == 4:
        log.error(f"An error occurred: {out['error']}")
        time.sleep(4)
    
    out = hub.send_command("stop_upload", [])
    if out["packet-type"] == 4:
        log.error(f"An error occurred: {out['error']}")
        time.sleep(4)
    
    log.success("Finished successfully")
    log.log("Please wait for 3 seconds before returning to main menu")
    time.sleep(1)
    log.log("Please wait for 2 seconds before returning to main menu")
    time.sleep(1)
    log.log("Please wait for 1 seconds before returning to main menu")
    time.sleep(1)


def start_main_menu():
    global version, hub_version
    while True:
        out = main_menu(version,hub_version['return'])
        if out[1] == 0:
            log.log("Restarting hub Please wait...")
            hub.send_command("end_conn", [])
            log.success("Command sent")
            log.log(
                "Your hub will restart because if you uploaded data to it changes directorys and glitches the hub"
            )
            exit()
        elif out[1] == 1:
            while True:
                out2 = second_menu(
                "Manage", options=["Upload a python file", "Upload a module"]
                )
                if out2[1] == 0:
                    upload_file()
                elif out2[1] == 1:
                    pass
                elif out2[1] == 2:
                    break
                else:
                    pass
        elif out[1] == 2:
            while True:
                out2 = second_menu(
                    "Manage", options=["View mods", "Delete mods", "Delete files"]
                )
                if out2[1] == 0:
                    pass
                elif out2[1] == 1:
                    pass
                elif out2[1] == 2:
                    pass
                elif out2[1] == 3:
                    break
                else:
                    pass
        else:
            pass


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        widgets = [
            progressbar.Percentage(),
            " ",
            progressbar.ETA(),
            " ",
            textcolors.YELLOW,
            textcolors.BOLD,
            progressbar.Bar(marker="#", left="[", right="]"),
            textcolors.END,
        ]
        pbar = progressbar.ProgressBar(maxval=total_size, widgets=widgets)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


def download(file, url):
    urllib.request.urlretrieve(url, file, show_progress)

def download_program():
    clear()
    print(
        textcolors.BOLD
        + textcolors.PURPLE
        + "PYToHub is made by @mas6y6 on github\n"
        + textcolors.END
    )
    time.sleep(3)
    print("Loading download menu")
    h = options_menu(
        menuname="Download selection",
        desc="Please pick the lego hub that you are currently using",
        options=[
            "LEGO 45678 Education Spike Prime Hub",
            "LEGO 51515 MINDSTORMS Robot Inventor hub",
        ],
        include_exit=True,
    )
    if h[1] == 0:
        log.log("Requesting where to download...")
        dir = fbox.askdirectory()
        if dir == "":
            log.fatul("You did not select a directory...")
        log.log(f"Selected {dir}")
        log.log(f"Downloading... PYToHub.llsp to {dir}")
        try:
            download(
                f"{dir}/PYToHub.llsp",
                "https://github.com/mas6y6/PyToHub-assets/raw/main/PYToHub.llsp",
            )
        except Exception as e:
            log.fatul(
                f"""An unexpeted error has occured 
if you think this is by mistake then report this to (@mas6y6 on github)
{e}"""
            )
        log.success("Downloaded")
        log.log('Make sure that you upload this file to your Spike Prime hub')
    elif h[1] == 1:
        log.log("Requesting where to download...")
        dir = fbox.askdirectory()
        if dir == "":
            log.fatul("You did not select a directory...")
            
        log.log(f"Selected {dir}")
        log.log(f"Downloading... PYToHub.lms to {dir}")
        try:
            download(
                f"{dir}/PYToHub.lms",
                "https://github.com/mas6y6/PyToHub-assets/raw/main/PYTohub.lms",
            )
        except Exception as e:
            log.fatul(
                f"""An unexpeted error has occured 
if you think this is by mistake then report this to (@mas6y6 on github)
{e}"""
            )
        log.success("Downloaded")
        log.log('Make sure that you upload this file to your Mindstorms hub')
    else:
        log.fatul("Unknown error")


def run():
    global hub
    clear()
    print(
        textcolors.BOLD
        + textcolors.PURPLE
        + "PYToHub is made by @mas6y6 on github\n"
        + textcolors.END
    )
    time.sleep(3)
    while True:
        if not hub == None:
            start_main_menu()
        r = findhub()
        tryconnect(r)