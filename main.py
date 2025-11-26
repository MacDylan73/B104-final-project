"""
B104 Final Project - Dylan Folscroft and Travis Godley
11/25/2025

Run this file, main.py, with the following files in the same folder:
    - createGUI.py
    - loading.py
    - statistical_analysis.py
    - YBRSS_COMBINED.csv
"""


import tkinter as tk
from createGUI import gui

if __name__ == "__main__":
    window = tk.Tk()
    appScreen = gui(window)
    window.mainloop()
