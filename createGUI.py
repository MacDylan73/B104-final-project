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

import tkinter as tk
from statistical_analysis import analyze

class gui:
    def __init__(self, root):
        self.root = root
        self.root.title('B104 Final Project - Dylan Folscroft & T.J. Godley')
        self.root.geometry('500x500') 
        self.plot_type_var = tk.StringVar(self.root)

        self.lightTheme = {
            "window_bg": "#f5f5f5", "header_bg": "#e0e0e0", "header_fg": "#2c2c2c",
            "content_bg": "#ffffff", "content_fg": "#3c3c3c", "button_bg": "#d6d6d6", 
            "button_fg": "#2c2c2c", "accent": "#cccccc",
        }
        
        self.darkTheme = {
            "window_bg": "#1a1a1a", "header_bg": "#3a3a3a", "header_fg": "#e0e0e0",
            "content_bg": "#2c2c2c", "content_fg": "#d0d0d0", "button_bg": "#444444", 
            "button_fg": "#f0f0f0", "accent": "#555555",
        }

        self.current_theme = self.lightTheme
        self.setup_ui()
        self.apply_theme() # Apply theme after creating widgets


    def apply_theme(self):

        bg_color = self.current_theme["window_bg"]
        fg_color = self.current_theme["content_fg"]
        button_bg = self.current_theme["button_bg"]
        button_fg = self.current_theme["button_fg"]

        self.root.configure(bg=bg_color)


        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=bg_color)
                for child_widget in widget.winfo_children():
                    if isinstance(child_widget, (tk.Label, tk.OptionMenu)):
                         child_widget.configure(bg=bg_color, fg=fg_color)
                    elif isinstance(child_widget, tk.Button):
                        child_widget.configure(bg=button_bg, fg=button_fg)
            
            if isinstance(widget, (tk.Label, tk.OptionMenu)):
                widget.configure(bg=bg_color, fg=fg_color)
            elif isinstance(widget, tk.Button):
                widget.configure(bg=button_bg, fg=button_fg)

    def toggle_theme(self):
        if self.current_theme == self.lightTheme:
            self.current_theme = self.darkTheme
        else:
            self.current_theme = self.lightTheme
        self.apply_theme() 


    def setup_ui(self):
        title = tk.Label(self.root, text='2023 YRBS Data Analysis\n Compared against Suicide Attempts', font=("Helvetica", 16, "bold"))
        title.pack(pady=10)

        options = ['Stat Plot', 'Bar Graph'] 
        self.plot_type_var.set(options[0])
        menu = tk.Label(self.root, text='Choose Chart Type:')
        menu.pack(pady=5)
        plot = tk.OptionMenu(self.root, self.plot_type_var, *options)
        plot.pack(pady=5)
        
        theme = tk.Button(self.root, text="Toggle Theme", command=self.toggle_theme)
        theme.pack(pady=5)

        main_button_frame = tk.Frame(self.root)
        main_button_frame.pack(pady=10, padx=10)

        def buttons(frame, index, col, label):
            Label = tk.Label(frame, text=label, font=('Helvetica', 10, 'bold'))
            Label.grid(row=0, column=index, pady=5, padx=5)

            Everyone = tk.Button(frame, text='Everyone', command=lambda: self.run_analysis(col, label, gender=None))
            Everyone.grid(row=1, column=index, pady=2, padx=5, sticky='ew')

            Male = tk.Button(frame, text='Male', command=lambda: self.run_analysis(col, label, gender=1))
            Male.grid(row=2, column=index, pady=2, padx=5, sticky='ew')

            Female = tk.Button(frame, text='Female', command=lambda: self.run_analysis(col, label, gender=2))
            Female.grid(row=3, column=index, pady=2, padx=5, sticky='ew')

        buttons(main_button_frame, 0, 'q65', 'Sexual Identity')
        buttons(main_button_frame, 1, 'q58', 'Sexual Activity')
        buttons(main_button_frame, 2, 'q67', 'Weight Management')

        
    def run_analysis(self, name, label, gender=None):
        
        plot_type = self.plot_type_var.get() 
        data_frame, result_str = analyze(name, label, gender, plot_type)


