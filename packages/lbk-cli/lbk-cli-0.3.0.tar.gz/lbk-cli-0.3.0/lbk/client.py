import sys

from halo import Halo
from log_symbols import LogSymbols

import lbk.api as api


def show_usage():
    print("Usage:\n\tCreate log: lbk @context")


def add_log(context, message=None):
    if message is None:
        message = ''
        line = input('> ')
        while len(line) > 0:
            message += line
            line = input('> ')

    spinner = Halo(text='Sending', spinner='bouncingBall', color='white')
    spinner.start()

    if api.send(context, message):
        spinner.stop_and_persist(symbol=LogSymbols.SUCCESS.value, text='Ok')
    else:
        spinner.stop_and_persist(symbol=LogSymbols.ERROR.value, text='Failed')


def main():
    if len(sys.argv) > 1:
        if sys.argv[1][0] == '@':
            if len(sys.argv) == 3:
                message = sys.argv[2]
            else:
                message = None
            add_log(sys.argv[1][1:], message)
        else:
            show_usage()
    else:
        show_usage()


if __name__ == '__main__':
    main()
