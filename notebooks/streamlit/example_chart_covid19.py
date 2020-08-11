import streamlit as st
import numpy as np
import pandas as pd
import chart_ipynb
from chart_ipynb import time_series
import urllib
from datetime import time, datetime
from IPython.display import display
import streamlit.components.v1 as components
import json

@st.cache
def get_data():
    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'
    df = pd.read_csv(url)
    return df.set_index("state")

try:
    df = get_data()
except urllib.error.URLError as e:
    st.error(
        """
        **This demo requires internet access.**
        Connection error: %s
    """
        % e.reason
    )

@st.cache
def get_state_data(data, state, start=None, end=None):
    """
    data: pd.DataFrame
    state: a str of state or a list of states
    """
    if start is None:
        start = data.iloc[0].date
    if end is None:
        end = data.iloc[-1].date
    data = data[(data.date >= start) & (data.date <= end)]
    states = data.reset_index().groupby('state')
    if isinstance(state, str):
        state = [state]
    state_data = dict()
    for s in state:
        idx = states.groups[s]
        state_data[s] = data.iloc[idx].reset_index(drop=True)
    return state_data

@st.cache
def get_daily_increase(data, state, start=None, end=None):
    df = get_state_data(data, state)
    daily_df = {}
    for i in df:
        temp = df[i].set_index('date')[['cases','deaths']].diff().reset_index().fillna(0)
        if start is None:
            start = temp.iloc[0].date
        if end is None:
            end = temp.iloc[-1].date
        daily_df[i] = temp[(temp.date >= start) & (temp.date <= end)]
    return daily_df

def get_data(time_scale, data, state, start=None, end=None):
    if time_scale == 'accumulated':
        return get_state_data(data=data, state=state, start=start, end=end)
    else:
        return get_daily_increase(data=data, state=state, start=start, end=end)

def draw_chart(chart_type, states, col, input_datasets):
    chart = time_series.time_series_Chart(chart_type, states, col, date_col = 'date', 
                        data_provide = True, title = 'Covid-19 - %s chart'%chart_type,
                        input_dataset = input_dataset)
    html_script = chart.html_script(chart)
    return html_script

states = st.multiselect(
        "Choose countries", list(set(df.index)), ["New York"]
    )
date_time = sorted(list(set(df['date'].values)))
date = st.slider('Select a range of date', value=(datetime.strptime(date_time[0],'%Y-%m-%d'), datetime.strptime(date_time[-1],'%Y-%m-%d')))
start = date[0].strftime("%Y-%m-%d")
end = date[-1].strftime("%Y-%m-%d")
col = st.selectbox('Which statistic you would like to see?', ('cases','deaths'))
cum = st.selectbox('How woule like to see the statistics', ('accumulated','daily increase'))
if not states:
    st.error("Please select at least one country.")
else:
    data = get_data(cum, df.reset_index(), states, start, end)
    input_dataset = [data[s] for s in states]
    html_script = draw_chart('line', states, col, input_dataset)
    components.html(html_script,width=800, height=600)