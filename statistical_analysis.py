import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from loading import displayLoadingScreen, endLoadingScreen, animate


# Define variables for the data file and columns 
DATA = 'YBRSS_COMBINED.csv'
COLUMNS = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q29', 'q58', 'q65', 'q67']

# Map responses to integers that can be used for analysis. 
Q29_MAP = {1: '0 times', 2: '1 time', 3: '2 or 3 times', 4: '4 or 5 times', 5: '6+ times'}
Q58_MAP = {1: '0 partners', 2: '1 partner', 3: '2 partners', 4: '3 partners', 5: '4 partners', 6: '5 partners', 7: '6+ partners', 8: 'Did not answer'}
Q65_MAP = {1: 'Yes, Transgender', 2: 'No, Not Transgender', 3: 'Not Sure', 4: 'Prefer not to answer'}
Q67_MAP = {1: 'Trying to lose weight', 2: 'Trying to gain weight', 3: 'Trying to stay the same weight', 4: 'Not trying to change weight', 5: 'Did not answer'}
Q2_MAP = {1: 'Male', 2: 'Female'}
MAP_LOOKUP = {'q29': Q29_MAP, 'q58': Q58_MAP, 'q65': Q65_MAP, 'q67': Q67_MAP, 'q2': Q2_MAP}

# Theme variables (for gradient bar colors)
barColorsLight = {
    0: "#b3c9dc",  
    1: "#94b5d0",
    2: "#759fc3",
    3: "#5d89b6",
    4: "#4c72b0",  
    5: "#3f639f",
    6: "#33558d",  
}

barColorsDark = {
    0: "#2a3f57",  
    1: "#2a3f57",
    2: "#385474",
    3: "#466991",
    4: "#4c72b0",  
    5: "#5f86bd",
    6: "#7299c9",  
}

# more theme variables (for background/labels)
lightTheme = {
    "content_bg": "#ffffff",
    "content_fg": "#3c3c3c",
}
darkTheme = {
    "content_bg": "#2c2c2c",
    "content_fg": "#d0d0d0",
}


def process(path, col, gender=None):

    # Read the data from the csv inport into the dataframe and handle errors due to no values
    df = pd.read_csv(path, usecols=COLUMNS)
    df['q29'] = pd.to_numeric(df['q29'], errors='coerce')
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df['q2'] = pd.to_numeric(df['q2'], errors='coerce')
    df = df.dropna(subset=['q2', 'q29', col])
    df = df[df['q2'].isin(MAP_LOOKUP['q2'].keys())]
    df = df[df['q29'].isin(MAP_LOOKUP['q29'].keys())]

    # Remove responses that do not have statistical relevance    
    if gender is not None:
        df = df[df['q2'] == gender]
    if col == 'q58':
        df = df[df[col] != 8]
    if col == 'q67':
        df = df[df[col] != 5]
    elif col == 'q65':
        df = df[df[col] != 4]
    return df, None


# Primamry analysis function calls the process to get the cleaned data
def analyze(col, label, gender, plot, frame, theme, classItem):
    # init loading screen to cover up graph reconfig/changes
    ani, fr = displayLoadingScreen(classItem)
    
    # get cleaned data using process, call selector to continue graph generation
    df, _ = process(DATA, col, gender)
    animate(ani, "-", fr)
    if gender is None:
        desc = 'Everyone'
    else:
        desc = MAP_LOOKUP['q2'].get(gender, 'Filtered Sample')
    result_text = f"--- {desc} | {plot} ---\n"
    result_text += f"Analysis for Q29 vs {label}:\n" 
    animate(ani, "´", fr)
    selector(df, label, col, desc, plot, frame, theme, classItem, ani, fr)
    return df, result_text + '\nNote: No statistical tests were performed.'


# Function to call either bar graph or stat plot
def selector(df, label, name, desc, plot, frame, theme, classItem, ani, fr):
    animate(ani, "'", fr)
    if plot == 'Bar Graph':
        bar_graph(df, label, name, desc, frame, theme, classItem, ani, fr)
    if plot == 'Stat Plot':
        stat_plot(df, label, name, desc, frame, theme, classItem, ani, fr)


# Function to create Bar Graph by suicide attempts
def bar_graph(df, label, name, desc, frame, theme, classItem, ani, fr):
    plt.figure(figsize=(8, 4.8))
    
    code = sorted(df[name].unique())
    avg_attempts = df.groupby(name)['q29'].mean().sort_index()
    avg_attempts = avg_attempts.reindex(code)
    avg_attempts.index = [MAP_LOOKUP[name].get(idx, f'Code {idx}') for idx in avg_attempts.index]
    
    # get theme
    if theme:
        toggleTheme = darkTheme
        barColor = barColorsDark
    else: 
        toggleTheme = lightTheme
        barColor = barColorsLight
    animate(ani, "´", fr)
    
    # Create Bar Graph
    graph = avg_attempts.plot(kind='bar')
    figure = graph.get_figure()
    
    # Add color coded bars in order of height
    order = []
    for bar in graph.patches:
        order.append(bar.get_height())
    order.sort()
    
    for i, height in enumerate(order):
        for bar in graph.patches:
            if bar.get_height() == height:
                bar.set_facecolor(barColor[i])
                
                
    # graph config
    plt.title(f'{desc}: Avg Suicide Attempts by {label}', color=toggleTheme["content_fg"])
    plt.xlabel(f'{label}', color=toggleTheme["content_fg"])
    plt.ylabel('Avg Suicide Attempts', color=toggleTheme["content_fg"])
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    
    animate(ani, "-", fr)
    
    # style tick labels
    plt.tick_params(color=toggleTheme["content_fg"])
    for label in graph.get_xticklabels():
        label.set_color(color=toggleTheme["content_fg"])
    for label in graph.get_yticklabels():
        label.set_color(color=toggleTheme["content_fg"])
    
    plt.tight_layout()
    
    # clear canvas (MUST HAVE TO DISPOSE OF OLD GRAPHS AND SHOW NEW ONES)
    for widget in frame.winfo_children():
        widget.destroy()
    
    animate(ani, "_", fr)
    # draw new graph on canvas (which is widget in midFrame) using matplotlib figure object
    canvas = FigureCanvasTkAgg(figure, frame)
    figure.patch.set_facecolor(toggleTheme["content_bg"])
    graph.set_facecolor(toggleTheme["content_bg"])
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

    # end loading screen
    endLoadingScreen(classItem)
    
    
# Function to create stat plot by suicide attempts 
def stat_plot(df, label, name, desc, frame, theme, classItem, ani, fr):
    df_plot = df.copy()
    present_numeric_codes = sorted(df_plot[name].unique())
    category_order_labels = [MAP_LOOKUP[name][code] for code in present_numeric_codes]
    df_plot[label] = df_plot[name].map(MAP_LOOKUP[name])
    animate(ani, "´", fr)
    
    # get theme
    if theme:
        toggleTheme = darkTheme
    else: toggleTheme = lightTheme
    
    # creating plot
    g = sns.catplot(x=label, y='q29', data=df_plot, kind='point', height=4, aspect=1.5, order = category_order_labels)
    g.fig.suptitle(f'{desc}: Avg Suicide Attempts by {label}', y=1.05)
    figure = g.fig
    graph = g.ax
    
    # config
    graph.title.set_color(toggleTheme["content_fg"])
    graph.xaxis.label.set_color(toggleTheme["content_fg"])
    graph.yaxis.label.set_color(toggleTheme["content_fg"])
    
    g.set_axis_labels(label, 'Avg Suicide Attempts')
    plt.title(f'{desc}: Avg Suicide Attempts by {label}', color=toggleTheme["content_fg"])
    
    # style tick labels
    graph.tick_params(color=toggleTheme["content_fg"])
    for label in graph.get_xticklabels():
        label.set_color(color=toggleTheme["content_fg"])
    for label in graph.get_yticklabels():
        label.set_color(color=toggleTheme["content_fg"])

    animate(ani, "-", fr)
    
    g.set_xticklabels(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    
    # MUST HAVE gets rid of old graph
    for widget in frame.winfo_children():
        widget.destroy()

    animate(ani, "_", fr)  
    # draw new graph on canvas (same as bar graph display)
    canvas = FigureCanvasTkAgg(figure, frame)
    figure.patch.set_facecolor(toggleTheme["content_bg"])
    graph.set_facecolor(toggleTheme["content_bg"])
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # end loading
    endLoadingScreen(classItem)
    
    # plt.show() never use this
    

"""
Sources:
- Displaying Graphs in Tkinter
    https://coderslegacy.com/figurecanvastkagg-matplotlib-tkinter/
- Bing/Google Search Overview (general)
- Matplotlib Docs
    https://matplotlib.org/stable/plot_types/index.html
- Bar Heights
    https://stackoverflow.com/questions/59724847/how-to-get-the-height-of-each-bar-in-pixels-in-matplotlib
- Stat Plot Creation and Display: Seaborn Docs
    https://seaborn.pydata.org/generated/seaborn.FacetGrid.html


"""
