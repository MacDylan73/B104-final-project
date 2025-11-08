"""
Project main.py file

Application must be run from this file with the following files in the same folder or directory:
1. createGUI.py
2. ........

"""

from tkinter import *
from createGUI import gui

if __name__ == "__main__":
    window = Tk()
    appScreen = gui(window)
    window.mainloop()
