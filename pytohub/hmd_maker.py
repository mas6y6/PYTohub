from .menu import *
import time
from .textcolors import textcolors
from tkinter.filedialog import askdirectory
import os
from .logging import log

file = None

def run_lmod_maker():
    print(
        textcolors.BOLD
        + textcolors.PURPLE
        + "PYToHub is made by @mas6y6 on github\n"
        + textcolors.END
    )
    time.sleep(3)

