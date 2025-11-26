"""
This file contains only the Tkinter GUI implementation for the project.
All GUI design and Tkinter screen related logic is contined in this file for organization

All methods and attributes for the screen and Tkinter widgets on it are contained within the gui class.

Usage in main.py:
    from createGUI import gui
    window = Tk()
    appScreen = gui(window)
    appScreen.mainloop()

Results in the Tkinter GUI window being displayed until the user closes it.

MidFrame is passed to statisical_analysis.py for the graphs to be drawn in
MidFrameParent is used in loading.py to overlay the loading animation during graph creation

Fully controls program logical and calls all graph creation. Graphs may be created
by changing the theme, graph selection, question selection, or gender filter.  

"""

# import Tkinter module
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font
from statistical_analysis import analyze


# Class for Tkinter GUI
class gui:

    # Initialize the GUI and its variables
    def __init__(self, window):
        # Window Init
        self.window = window
        self.title = "2023 YRBSS Data Analysis Compared Against Suicide Attempts"                # CHANGE TITLE OF WINDOW IF NEEDED
        self.window.title("B104 Final Project - Dylan Folscroft & T.J. Godley")
        # self.window.iconphoto(True, tk.PhotoImage(file="PATH_HERE"))  # CHANGE ICON IF NEEDED
        self.window.geometry("1400x800")

        # GUI Constants
        self.questions = ("Sexual Identity", "Weight Management", "Sexual Activity")
        self.genders = ("Everybody", "Male", "Female")
        
        self.lightTheme = {
            "window_bg": "#f5f5f5",
            "header_bg": "#e0e0e0",
            "header_fg": "#2c2c2c",
            "content_bg": "#ffffff",
            "content_fg": "#3c3c3c",
            "footer_bg": "#ebebeb",
            "footer_fg": "#2c2c2c",
            "button_bg": "#d6d6d6",
            "button_fg": "#2c2c2c",
            "combobox_bg": "#ffffff",
            "combobox_fg": "#3c3c3c",
            "accent": "#cccccc",

        }

        self.darkTheme = {
            "window_bg": "#1a1a1a",
            "header_bg": "#3a3a3a",
            "header_fg": "#e0e0e0",
            "content_bg": "#2c2c2c",
            "content_fg": "#d0d0d0",
            "footer_bg": "#3a3a3a",
            "footer_fg": "#e0e0e0",
            "button_bg": "#444444",
            "button_fg": "#f0f0f0",
            "combobox_bg": "#2c2c2c",
            "combobox_fg": "#d0d0d0",
            "accent": "#555555",
        }

        # GUI Dynamic Variables
        self.activeQuestion = "Sexual Identity"
        self.activeGender = None
        
        self.isThemeToggled = False
        self.isGraphToggled = False

        self.init_gui()
        self.createGraph()

    # Initialize Tkinter Widgets and Place them on the screen
    def createGraph(self):
        if self.activeQuestion == "Sexual Identity":
            q = "q65"
        elif self.activeQuestion == "Sexual Activity":
            q = "q58"
        else: q = "q67"
        label = self.activeQuestion
        gender = self.activeGender
        if gender == "Male": 
            gender = 1
        elif gender == "Female":
            gender = 2
        else:
            gender = None
            
        if self.isGraphToggled: 
            graph = "Stat Plot"
        elif not self.isGraphToggled: graph = "Bar Graph"
        
        analyze(q, label, gender, graph, self.midFrame, self.isThemeToggled, self)
    
    def init_gui(self):
        # Frames for easier organization
        rootFrame = tk.Frame(self.window, bg=self.lightTheme["window_bg"])
        rootFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.upperFrame = tk.Frame(rootFrame, bg=self.lightTheme["header_bg"], relief="groove")
        self.upperFrame.place(rely=0, relwidth=1, relheight=.075)
        #self.upperFrame.grid(row=0, column=0, sticky="NSEW")
        
        self.midFrameParent = tk.Frame(rootFrame, bg=self.lightTheme["content_bg"])
        self.midFrameParent.place(rely=.075, relwidth=1, relheight=.8)
        
        self.midFrame = tk.Frame(self.midFrameParent, bg=self.lightTheme["content_bg"])
        self.midFrame.place(relwidth=1, relheight=1)

        self.lowerFrame = tk.Frame(rootFrame, bg=self.lightTheme["footer_bg"])
        self.lowerFrame.place(rely= .875, relwidth=1, relheight=.125)

        # Title
        self.titleLabel = tk.Label(self.upperFrame, text=self.title, padx=10, pady=5, font=font.Font(size=32, weight="bold"), bg=self.lightTheme["header_bg"], fg=self.lightTheme["header_fg"])

        # Theme
        self.themeToggle = tk.Button(self.lowerFrame, text="Dark Mode", activebackground=self.lightTheme["button_bg"], foreground=self.lightTheme["button_fg"], command=self.toggleTheme)
        
        # Graph
        self.graphToggle = tk.Button(self.lowerFrame, text="Stat Plot", activebackground=self.lightTheme["button_bg"], foreground=self.lightTheme["button_fg"], command=self.toggleGraph)

        # Question Selection Dropdown
        self.questionLabel = tk.Label(self.lowerFrame, text="Comparison", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])

        self.questionComboBox = ttk.Combobox(self.lowerFrame)
        self.questionComboBox.state(["readonly"])
        self.questionComboBox["values"] = self.questions
        self.questionComboBox.bind("<<ComboboxSelected>>", self.changeQuestion)


        # Gender Selection Dropdown
        self.genderLabel = tk.Label(self.lowerFrame, text="Filter by Gender", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])
        self.genderCombobox = ttk.Combobox(self.lowerFrame)
        self.genderCombobox.state(["readonly"])
        self.genderCombobox["values"] = self.genders
        self.genderCombobox.bind("<<ComboboxSelected>>", self.changeGender)

        # Init Dropdowns
        self.questionComboBox.set("Sexual Identity")
        self.genderCombobox.set("Everybody")

        # Names
        self.namesLabel = tk.Label(self.lowerFrame, text="B104 Final Project: Dylan Folscroft and Travis Godley", padx=10, pady=5, font=font.Font(size=8), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])

        # Place Elements
        self.titleLabel.place(relx=.5, rely=.5, anchor="center")
        self.namesLabel.place(relx=1, rely=1, anchor="se")

        self.themeToggle.place(relx=.05, rely=.5, anchor="center")
        self.graphToggle.place(relx=.1, rely=.5, anchor="center")
        

        self.questionLabel.place(relx=.35, rely=.3, anchor="center")
        self.questionComboBox.place(relx=.35, rely=.6, anchor="center")

        self.genderLabel.place(relx=.65, rely=.3, anchor="center")
        self.genderCombobox.place(relx=.65, rely=.6, anchor="center")


    # toggleTheme function
    # reconfigures colors/styles for elements on the screen based on isThemeToggled variable
    def toggleTheme(self):
        self.isThemeToggled = not self.isThemeToggled

        if(self.isThemeToggled):
            theme = self.darkTheme
            self.themeToggle.config(text="Light Mode")
        else:
            theme = self.lightTheme
            self.themeToggle.config(text="Dark Mode")

        self.themeToggle.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.graphToggle.config(bg=theme["button_bg"], fg=theme["button_fg"])

        self.upperFrame.config(bg=theme["header_bg"])
        self.titleLabel.config(bg=theme["header_bg"], fg=theme["header_fg"])

        self.midFrame.config(bg=theme["content_bg"])

        self.lowerFrame.config(bg=theme["footer_bg"])
        
        self.questionLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])
        self.questionComboBox.config()
        
        self.genderLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.namesLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])
        
        self.createGraph()
        

    # Dropdown Selection Change Event Handlers
    # !!!NOTE Imported functions from a seperate py file such as dataAnalysis.py can be called here
    def changeQuestion(self, event):
        self.activeQuestion = self.questionComboBox.get()
        print(f"Selected Question: {self.activeQuestion}")
        
        # DO SOEMTHING
        self.createGraph()
        
    def changeGender(self, event):
        val = self.genderCombobox.get()
        
        if val == "Everybody": 
            self.activeGender = None 
        else: self.activeGender = val
        
        print(f"Selected Gender: {self.activeGender}")
        
        # DO SOMETHING
        self.createGraph()
        
    def toggleGraph(self):
        self.isGraphToggled = not self.isGraphToggled
        
        if(self.isGraphToggled):
            self.graphToggle.config(text="Bar Graph")
        else:
            self.graphToggle.config(text="Stat Plot")
        
        self.createGraph()

"""
Sources:
- Bing AI Overview (overall)
- Python Tkinter module and documentation (overall)
    https://docs.python.org/3/library/tkinter.html
- tkdocs documentation (overall)
    tkdocs.com
- Light/Dark Mode Idea: NeuralNine YouTube
    https://m.youtube.com/watch?v=UdEtHBlirvo
"""
