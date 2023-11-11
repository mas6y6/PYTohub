from .main import run, download_program
import sys

class textcolors:
    """ ANSI color codes """
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    BROWN = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    YELLOW = "\033[33m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    LIGHT_YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

class log:
    def fatul(text,exitcode=1):
        print(
            textcolors.RED
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
            textcolors.RED
            + "[ERROR] "
            + text
            + textcolors.END
        )
    
    def warning(text):
        print(
            textcolors.YELLOW
            + "[WARNING] "
            + text
            + textcolors.END
        )
    
    def success(text):
        print(
            textcolors.GREEN
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
        
    def successblue(text):
        print(
            textcolors.BLUE
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
    
    def successcyan(text):
        print(
            textcolors.CYAN
            + "[SUCCESS] "
            + text
            + textcolors.END
        )
    
    def log(text):
        print(
            "[INFO] "
            + text
        )

def show_help():
    print("")

if __name__ == "__main__":
    program = sys.argv[0]
    if not len(sys.argv) == 1:
        if '--download' in sys.argv:
            download_program()
            
        elif '--help' in sys.argv:
            show_help()
            
        else:
            log.fatul(f"Unknown argument {sys.argv[1]} for help use \"--help\"")
    else:
        run()