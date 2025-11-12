# Testings Pandas 
import pandas as pd
import matplotlib.pyplot as plt

"""
https://pandas.pydata.org/pandas-docs/stable/index.html
https://www.geeksforgeeks.org/python/how-to-plot-bar-graph-in-python-using-csv-file/
"""

data = pd.read_csv("C:/Users/chill/Desktop/B104_Final/B104-final-project-clone1/YBRSS_COMBINED.csv")

dataFrame = pd.DataFrame(data)


print(dataFrame.iloc[:, 7])

test = dataFrame.iloc[:, 1].value_counts().sort_index()

ax = test.plot.bar()

for container in ax.containers:
    ax.bar_label(container)
    
#ax.set_ylim(0, 700)
