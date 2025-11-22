import tkinter as tk
from createGUI import gui

if __name__ == "__main__":
    window = tk.Tk()
    appScreen = gui(window)
    window.mainloop()
