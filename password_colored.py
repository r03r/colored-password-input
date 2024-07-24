#!/usr/bin/env python3
import sys
import tty
import termios
from colorama import Fore, init

init(autoreset=True)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getpass_color_asterisk(prompt='[sudo] password for user: '):
    colors = [Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    pwd = ""
    color_index = 0
    sys.stderr.write(prompt)
    sys.stderr.flush()
    while True:
        char = getch()
        if char == '\r' or char == '\n':
            sys.stderr.write('\n')
            return pwd
        elif char == '\x7f':  # backspace
            if len(pwd) > 0:
                sys.stderr.write('\b \b')
                pwd = pwd[:-1]
                color_index = (color_index - 1) % len(colors)
        else:
            sys.stderr.write(colors[color_index] + '*')
            pwd += char
            color_index = (color_index + 1) % len(colors)

if __name__ == "__main__":
    password = getpass_color_asterisk()
    print(password)
