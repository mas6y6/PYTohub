from .main import run, download_program
import sys

if __name__ == "__main__":
    program = sys.argv[0]
    sys.argv.pop(0)
    if sys.argv[0] == '--download':
        download_program()
    else:
        run()