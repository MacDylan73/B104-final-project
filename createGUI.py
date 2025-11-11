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

Import functions from a statisiticalAnalysis.py file to display data visualization in mid frame.
Attach these functions to the event handlers (changeQuestion, changeQuestionChoice, changeDemographic) rather than
coding them in this file to keep logic clean and separate
"""

# import Tkinter module
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font


# Class for Tkinter GUI
class gui:

    # Initialize the GUI and its variables
    def __init__(self, window):
        # Window Init
        self.window = window
        self.title = "Suicide Correlation Data Analysis"                # CHANGE TITLE OF WINDOW IF NEEDED
        self.window.title(self.title)
        # self.window.iconphoto(True, tk.PhotoImage(file="PATH_HERE"))  # CHANGE ICON IF NEEDED
        self.window.geometry("1400x800")

        # GUI Constants
        self.questions = ("Transgender", "Weight", "Sexual Activity")
        
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
        self.activeQuestion = "Transgender"
        
        self.demographics = ["No Filter","No Filter","No Filter","No Filter","No Filter","No Filter","No Filter"]

        self.isThemeToggled = False

        self.init_gui()


    # Initialize Tkinter Widgets and Place them on the screen
    def init_gui(self):
        # Frames for easier organization
        rootFrame = tk.Frame(self.window, bg=self.lightTheme["window_bg"])
        rootFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

        self.upperFrame = tk.Frame(rootFrame, bg=self.lightTheme["header_bg"], relief="groove")
        self.upperFrame.place(rely=0, relwidth=1, relheight=.075)
        #self.upperFrame.grid(row=0, column=0, sticky="NSEW")

        self.midFrame = tk.Frame(rootFrame, bg=self.lightTheme["content_bg"])
        self.midFrame.place(rely=.075, relwidth=1, relheight=.8)

        self.lowerFrame = tk.Frame(rootFrame, bg=self.lightTheme["footer_bg"])
        self.lowerFrame.place(rely= .875, relwidth=1, relheight=.125)

        # Title
        self.titleLabel = tk.Label(self.upperFrame, text=self.title, padx=10, pady=5, font=font.Font(size=32, weight="bold"), bg=self.lightTheme["header_bg"], fg=self.lightTheme["header_fg"])

        # Theme
        self.themeToggle = tk.Button(self.lowerFrame, text="Dark Mode", activebackground=self.lightTheme["button_bg"], foreground=self.lightTheme["button_fg"], command=self.toggleTheme)

        # Question Selection Dropdown
        self.questionLabel = tk.Label(self.lowerFrame, text="Comparison", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])

        self.questionComboBox = ttk.Combobox(self.lowerFrame)
        self.questionComboBox.state(["readonly"])
        self.questionComboBox["values"] = self.questions
        self.questionComboBox.bind("<<ComboboxSelected>>", self.changeQuestion)


        # Demographic Selection Dropdown
        self.demographicLabel = tk.Label(self.lowerFrame, text="Filter by Demographic", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])
        self.demographicButton = tk.Button(self.lowerFrame, text="Open Filter Settings", activebackground=self.lightTheme["button_bg"], foreground=self.lightTheme["button_fg"], command=self.filterWindow)


        # Init Dropdowns
        self.questionComboBox.set("Transgender")

        # Names
        self.namesLabel = tk.Label(self.lowerFrame, text="B104 Final Project: Dylan Folscroft and Travis Godley", padx=10, pady=5, font=font.Font(size=8), bg=self.lightTheme["footer_bg"], fg=self.lightTheme["footer_fg"])

        # Place Elements
        self.titleLabel.place(relx=.5, rely=.5, anchor="center")
        self.namesLabel.place(relx=1, rely=1, anchor="se")

        self.themeToggle.place(relx=.05, rely=.5, anchor="center")

        self.questionLabel.place(relx=.35, rely=.3, anchor="center")
        self.questionComboBox.place(relx=.35, rely=.6, anchor="center")

        self.demographicLabel.place(relx=.65, rely=.3, anchor="center")
        self.demographicButton.place(relx=.65, rely=.6, anchor="center")


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

        self.upperFrame.config(bg=theme["header_bg"])
        self.titleLabel.config(bg=theme["header_bg"], fg=theme["header_fg"])

        self.midFrame.config(bg=theme["content_bg"])

        self.lowerFrame.config(bg=theme["footer_bg"])
        
        self.questionLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])
        self.questionComboBox.config()
        
        self.demographicLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])
        self.demographicButton.config(bg=theme["button_bg"], fg=theme["button_fg"])
        self.namesLabel.config(bg=theme["footer_bg"], fg=theme["footer_fg"])
        
        self.settingsWindow.config(bg=theme["footer_bg"])
        
        for label in [self.ageFilterLabel, self.sexFilterLabel, self.gradeFilterLabel, self.isHispanicFilterLabel, self.raceFilterLabel, self.heightFilterLabel, self.weightFilterLabel]:
            label.config(bg=theme["footer_bg"], fg=theme["footer_fg"])

    # Dropdown Selection Change Event Handlers
    # !!!NOTE Imported functions from a seperate py file such as dataAnalysis.py can be called here
    def changeQuestion(self, event):
        self.activeQuestion = self.questionComboBox.get()
        print(f"Selected Question: {self.activeQuestion}")

        # DO SOEMTHING


    def filterWindow(self):
        self.settingsWindow = tk.Toplevel(self.window)
        self.settingsWindow.title("Demographics Filtering Settings")
        self.settingsWindow.geometry("400x600")
        
        theme = self.darkTheme if self.isThemeToggled else self.lightTheme
        self.settingsWindow.config(bg=theme["footer_bg"])
        
        # All demographics options dropdowns
        # Age
        self.ageFilterLabel = tk.Label(self.settingsWindow, text="Filter Age", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.ageFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.ageFilterComboBox.state(["readonly"])
        self.ageFilterComboBox["values"] = ["No Filter", "12 years or younger", "13 years old", "14 years old", "15 years old", "16 years old", "17 years old", "18 years or older"]
        self.ageFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 0, self.ageFilterComboBox.get()))
        
        self.ageFilterLabel.place(relx=.5, rely=.04, anchor="center")
        self.ageFilterComboBox.place(relx=.5, rely=.09, anchor="center")
        self.ageFilterComboBox.set(self.demographics[0])
        
        # Sex
        self.sexFilterLabel = tk.Label(self.settingsWindow, text="Filter Sex", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.sexFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.sexFilterComboBox.state(["readonly"])
        self.sexFilterComboBox["values"] = ["No Filter", "Female", "Male"]
        self.sexFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 1, self.sexFilterComboBox.get()))
        
        self.sexFilterLabel.place(relx=.5, rely=.17, anchor="center")
        self.sexFilterComboBox.place(relx=.5, rely=.22, anchor="center")
        self.sexFilterComboBox.set(self.demographics[1])
        
        # Grade
        self.gradeFilterLabel = tk.Label(self.settingsWindow, text="Filter Grade", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.gradeFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.gradeFilterComboBox.state(["readonly"])
        self.gradeFilterComboBox["values"] = ["No Filter", "9th grade", "10th grade", "11th grade", "12th grade", "Ungraded or other grade"]
        self.gradeFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 2, self.gradeFilterComboBox.get()))
        
        self.gradeFilterLabel.place(relx=.5, rely=.3, anchor="center")
        self.gradeFilterComboBox.place(relx=.5, rely=.35, anchor="center")
        self.gradeFilterComboBox.set(self.demographics[2])
        
        # isHispanic
        self.isHispanicFilterLabel = tk.Label(self.settingsWindow, text="Filter Hispanic/Latino", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.isHispanicFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.isHispanicFilterComboBox.state(["readonly"])
        self.isHispanicFilterComboBox["values"] = ["No Filter", "Yes", "No"]
        self.isHispanicFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 3, self.isHispanicFilterComboBox.get()))
        
        self.isHispanicFilterLabel.place(relx=.5, rely=.43, anchor="center")
        self.isHispanicFilterComboBox.place(relx=.5, rely=.48, anchor="center")
        self.isHispanicFilterComboBox.set(self.demographics[3])
        
        # Race
        self.raceFilterLabel = tk.Label(self.settingsWindow, text="Filter Race", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.raceFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.raceFilterComboBox.state(["readonly"])
        self.raceFilterComboBox["values"] = ["No Filter", "American Indian or Alaska Native", "Asian", "Black or African American", "Native Hawaiian or Other Pacific Islander", "White"]
        self.raceFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 4, self.raceFilterComboBox.get()))
        
        self.raceFilterLabel.place(relx=.5, rely=.56, anchor="center")
        self.raceFilterComboBox.place(relx=.5, rely=.61, anchor="center")
        self.raceFilterComboBox.set(self.demographics[4])
        
        # Height
        self.heightFilterLabel = tk.Label(self.settingsWindow, text="Filter Height", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.heightFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.heightFilterComboBox.state(["readonly"])
        self.heightFilterComboBox["values"] = ["No Filter", "INSERT RANGE 1", "INSERT RANGE 2"]
        self.heightFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 5, self.heightFilterComboBox.get()))
        
        self.heightFilterLabel.place(relx=.5, rely=.69, anchor="center")
        self.heightFilterComboBox.place(relx=.5, rely=.74, anchor="center")
        self.heightFilterComboBox.set(self.demographics[5])
        
        # Weight
        self.weightFilterLabel = tk.Label(self.settingsWindow, text="Filter Weight", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["footer_bg"], fg=theme["footer_fg"])

        self.weightFilterComboBox = ttk.Combobox(self.settingsWindow)
        self.weightFilterComboBox.state(["readonly"])
        self.weightFilterComboBox["values"] = ["No Filter", "INSERT RANGE 1", "INSERT RANGE 2"]
        self.weightFilterComboBox.bind("<<ComboboxSelected>>", lambda event: self.changeDemographic(event, 6, self.weightFilterComboBox.get()))
        
        self.weightFilterLabel.place(relx=.5, rely=.82, anchor="center")
        self.weightFilterComboBox.place(relx=.5, rely=.87, anchor="center")
        self.weightFilterComboBox.set(self.demographics[6])
        


    def changeDemographic(self, event, index, selection):
        self.demographics[index] = selection
        print(f"Selected Demographic: {self.demographics}")

        # DO SOMETHING


"""
Sources:
- Bing AI Overview for photoicon change
- Python Tkinter module and documentation (overall)
    https://docs.python.org/3/library/tkinter.html
- tkdocs documentation (overall)
    tkdocs.com
- Light/Dark Mode Idea: NeuralNine YouTube
    https://m.youtube.com/watch?v=UdEtHBlirvo
"""
