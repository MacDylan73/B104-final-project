import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA = 'YBRSS_COMBINED.csv'
COLUMNS = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q29', 'q58', 'q65', 'q67']

Q29_MAP = {1: '0 times', 2: '1 time', 3: '2 or 3 times', 4: '4 or 5 times', 5: '6+ times'}
Q58_MAP = {1: '0 partners', 2: '1 partner', 3: '2 partners', 4: '3 partners', 5: '4 partners', 6: '5 partners', 7: '6+ partners', 8: 'Did not answer'}
Q65_MAP = {1: 'Yes, Transgender', 2: 'No, Not Transgender', 3: 'Not Sure', 4: 'Prefer not to answer'}
Q67_MAP = {1: 'Trying to lose weight', 2: 'Trying to gain weight', 3: 'Trying to stay the same weight', 4: 'Not trying to change weight', 5: 'Did not answer'}
Q2_MAP = {1: 'Male', 2: 'Female'}
MAP_LOOKUP = {'q29': Q29_MAP, 'q58': Q58_MAP, 'q65': Q65_MAP, 'q67': Q67_MAP, 'q2': Q2_MAP}

def process(path, col, gender=None):

    df = pd.read_csv(path, usecols=COLUMNS)
    df['q29'] = pd.to_numeric(df['q29'], errors='coerce')
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df['q2'] = pd.to_numeric(df['q2'], errors='coerce')
    df = df.dropna(subset=['q2', 'q29', col])
    df = df[df['q2'].isin(MAP_LOOKUP['q2'].keys())]
    df = df[df['q29'].isin(MAP_LOOKUP['q29'].keys())]
    
    if gender is not None:
        df = df[df['q2'] == gender]
    if col == 'q58':
        df = df[df[col] != 8]
    if col == 'q67':
        df = df[df[col] != 5]
    elif col == 'q65':
        df = df[df[col] != 4]
    return df, None

def analyze(col, label, gender, plot):

    df, _ = process(DATA, col, gender)
    if gender is None:
        desc = 'Everyone'
    else:
        desc = MAP_LOOKUP['q2'].get(gender, 'Filtered Sample')
    result_text = f"--- {desc} | {plot} ---\n"
    result_text += f"Analysis for Q29 vs {label}:\n" 
    selector(df, label, col, desc, plot)
    return df, result_text + '\nNote: No statistical tests were performed.'

def selector(df, label, name, desc, plot):

    if plot == 'Bar Graph':
        bar_graph(df, label, name, desc)
    if plot == 'Stat Plot':
        stat_plot(df, label, name, desc)

def bar_graph(df, label, name, desc):
    plt.figure(figsize=(10, 6))
    
    code = sorted(df[name].unique())
    avg_attempts = df.groupby(name)['q29'].mean().sort_index()
    avg_attempts = avg_attempts.reindex(code)
    avg_attempts.index = [MAP_LOOKUP[name].get(idx, f'Code {idx}') for idx in avg_attempts.index]
    
    avg_attempts.plot(kind='bar', color=sns.color_palette("Paired"))
    plt.title(f'{desc}: Avg Suicide Attempts by {label}')
    plt.xlabel(f'{label}')
    plt.ylabel('Avg Suicide Attempts')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

def stat_plot(df, label, name, desc):
    df_plot = df.copy()
    present_numeric_codes = sorted(df_plot[name].unique())
    category_order_labels = [MAP_LOOKUP[name][code] for code in present_numeric_codes]
    df_plot[label] = df_plot[name].map(MAP_LOOKUP[name])
    g = sns.catplot(x=label, y='q29', data=df_plot, kind='point', height=6, aspect=1.5, order = category_order_labels)
    g.fig.suptitle(f'{desc}: Avg Suicide Attempts by {label}', y=1.05)
    g.set_axis_labels(label, 'Avg Suicide Attempts')
    g.set_xticklabels(rotation=45, ha='right')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


