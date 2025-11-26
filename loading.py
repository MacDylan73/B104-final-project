"""
Loading.py

Must be imported into statistical analysis

Makes the slightly jarring and uncomfortable flashing when the graph is being changed
slightly more bearable.  Also displays a cool burger flipping animation

Not fully essential to function, improves QOL
"""
import time
import tkinter as tk
from tkinter import font

    
def displayLoadingScreen(classItem):
    frame = classItem.midFrameParent
    inner = classItem.midFrame
    
    print("loading")
    
    theme = classItem.lightTheme if not classItem.isThemeToggled else classItem.darkTheme 
    frame.config(bg=theme["content_bg"])
    
    loadingLabel = tk.Label(frame, text="Loading", padx=10, pady=5, font=font.Font(size=16, weight="bold"), bg=theme["content_bg"], fg=theme["content_fg"])
    loadingLabel.place(relx=.5, rely=.3, anchor="center")
    
    animation = tk.Label(frame, text="_", font=font.Font(size=100, weight="bold"), bg=theme["content_bg"], fg=theme["content_fg"])
    animation.place(relx=.5, rely=.5, anchor="center")
    
    frame.place(rely=.075, relwidth=1, relheight=.8)
    inner.place_forget()
    frame.update()
    
    return animation, frame


def animate(label, text, frame):
    label.config(text=text)
    frame.update()
    time.sleep(.05)
    
    
def endLoadingScreen(classItem):
    frame = classItem.midFrameParent
    inner = classItem.midFrame
    
    print("loading done")
    time.sleep(.13)
    
    # remove label
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()
    
    inner.place(relwidth=1, relheight=1)
    
    
"""
Sources:
- Loading Animation
    https://stackoverflow.com/questions/2685435/cooler-ascii-spinners
    https://raw.githubusercontent.com/sindresorhus/cli-spinners/master/spinners.json
- Overlay Destroy
    https://www.geeksforgeeks.org/python/how-to-clear-out-a-frame-in-the-tkinter/

"""
