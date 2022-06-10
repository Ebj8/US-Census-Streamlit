import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title('2017 US Census Data Country Level')

@st.cache 
def load_data(csv):
    data = pd.read_csv(csv)
    return data

data = load_data('acs2017_census_tract_data.csv')

data = data.assign(NumWhite = data['TotalPop']* data['White'] * 0.01,
    NumBlack = data['TotalPop']* data['Black'] * 0.01,
    NumHispanic = data['TotalPop']* data['Hispanic'] * 0.01,
    NumNative = data['TotalPop']* data['Native'] * 0.01,
    NumAsian = data['TotalPop']* data['Asian'] * 0.01,
    NumPacific = data['TotalPop']* data['Pacific'] * 0.01
)

data = data.assign(PopCheck = data['NumWhite'] + data['NumBlack'] + data['NumHispanic']
                    + data['NumNative'] + data['NumAsian'] + data['NumPacific'])

data = data.assign(NumUndeclared = data['TotalPop'] - data['PopCheck'])

country = data.groupby('State', as_index=False).agg({
                                    'TotalPop': 'sum', 'NumWhite': 'sum',
                                    'NumBlack': 'sum', 'NumHispanic': 'sum',
                                    'NumNative': 'sum', 'NumAsian': 'sum',
                                    'NumPacific': 'sum', 'NumUndeclared': 'sum'
})

country = country.assign(
    pct_white = country['NumWhite']/country['TotalPop'],
    pct_black = country['NumBlack']/country['TotalPop'],
    pct_hispanic = country['NumHispanic']/country['TotalPop'],
    pct_native = country['NumNative']/country['TotalPop'],
    pct_asian = country['NumAsian']/country['TotalPop'],
    pct_pacific = country['NumPacific']/country['TotalPop'],
    pct_undeclared = country['NumUndeclared']/country['TotalPop'],
    country = 'USA'
    )

country_agg = country.groupby('country', as_index=False).agg({
    'TotalPop': 'sum', 'NumWhite': 'sum', 'NumBlack': 'sum', 'NumHispanic': 'sum',
    'NumNative': 'sum', 'NumAsian': 'sum', 'NumPacific': 'sum', 'NumUndeclared': 'sum'
})

country_agg = country_agg.assign(
    pct_white = country['NumWhite']/country['TotalPop'],
    pct_black = country['NumBlack']/country['TotalPop'],
    pct_hispanic = country['NumHispanic']/country['TotalPop'],
    pct_native = country['NumNative']/country['TotalPop'],
    pct_asian = country['NumAsian']/country['TotalPop'],
    pct_pacific = country['NumPacific']/country['TotalPop'],
    pct_undeclared = country['NumUndeclared']/country['TotalPop']
)

country_agg = country_agg.iloc[:,[0,9,10,11,12,13,14,15]]
country_agg = pd.melt(country_agg,id_vars=["country"])

pop_bar_chart = alt.Chart(country).mark_bar().encode(
    x = alt.X('State', sort = '-y'),
    y = 'TotalPop'
)

st.altair_chart(pop_bar_chart, use_container_width=True)

us_race_bar = alt.Chart(country_agg).mark_bar().encode(
    x = alt.X('sum(value)'),
    y = 'country',
    color = 'variable'
)

st.altair_chart(us_race_bar)

if st.checkbox('Show Data'):
    st.subheader('Data')
    st.write(country_agg)