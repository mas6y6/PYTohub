from .main import run
import sys

if __name__ == "__main__":
    program = sys.argv[0]
    sys.argv.pop()
    run(sys.argv)