import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from pandas.plotting import register_matplotlib_converters


register_matplotlib_converters()
plt.style.use('ggplot')

#load in data from previous video
df = pd.read_csv('data/clean_data/cleaned_btc_weekly.csv')


#change timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

#drop duplicates
df.drop_duplicates(subset=['timestamp'],
                   keep='first',
                   inplace=True)
df.reset_index(inplace=True)

plt.plot(df.timestamp, df.close)