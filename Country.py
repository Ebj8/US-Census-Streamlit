import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

st.title('2017 US Census Data Country Level')

@st.cache 

# A function for reading in the data. I honestly don't know why I couldn't just use read_csv()
def load_data(csv):
    data = pd.read_csv(csv)
    return data

# Load in the data
data = load_data('acs2017_census_tract_data.csv')

# Add columns with the quanitity of peopole in each category rather than a percentage
data = data.assign(NumWhite = data['TotalPop']* data['White'] * 0.01,
    NumBlack = data['TotalPop']* data['Black'] * 0.01,
    NumHispanic = data['TotalPop']* data['Hispanic'] * 0.01,
    NumNative = data['TotalPop']* data['Native'] * 0.01,
    NumAsian = data['TotalPop']* data['Asian'] * 0.01,
    NumPacific = data['TotalPop']* data['Pacific'] * 0.01
)

# Add a column to check that all of the different race columns add up to the total population
# (Spoiler alert: It doesn't!)
data = data.assign(PopCheck = data['NumWhite'] + data['NumBlack'] + data['NumHispanic']
                    + data['NumNative'] + data['NumAsian'] + data['NumPacific'])

# Add a column with the leftover population that wasn't declared as a certain race
data = data.assign(NumUndeclared = data['TotalPop'] - data['PopCheck'])

# Create a new data frame called country where each row is a state. The columns are made up 
# of the various populations of each race as awell as the total population
country = data.groupby('State', as_index=False).agg({
                                    'TotalPop': 'sum', 'NumWhite': 'sum',
                                    'NumBlack': 'sum', 'NumHispanic': 'sum',
                                    'NumNative': 'sum', 'NumAsian': 'sum',
                                    'NumPacific': 'sum', 'NumUndeclared': 'sum'
})

# Add columns with the percentage that each state is made up of each race. I don't use
# these columns ever so I may remove this code later
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

# Create a new data frame that is only one row long showing the total population of each 
# race in the US
country_agg = country.groupby('country', as_index=False).agg({
    'TotalPop': 'sum', 'NumWhite': 'sum', 'NumBlack': 'sum', 'NumHispanic': 'sum',
    'NumNative': 'sum', 'NumAsian': 'sum', 'NumPacific': 'sum', 'NumUndeclared': 'sum'
})

# Add percentage columns for each race for the entire US
country_agg = country_agg.assign(
    White = country['NumWhite']/country['TotalPop'],
    Black = country['NumBlack']/country['TotalPop'],
    Hispanic = country['NumHispanic']/country['TotalPop'],
    Native = country['NumNative']/country['TotalPop'],
    Asian = country['NumAsian']/country['TotalPop'],
    Pacific = country['NumPacific']/country['TotalPop'],
    Undeclared = country['NumUndeclared']/country['TotalPop']
)

# For the percentile bar graph showing the distribution of races in the US I reformat
# the data frame to only include the percentages of each race and then melt this data
# frame into a column for the races and a column showing the percent make up of each race.
country_agg = country_agg.iloc[:,[0,9,10,11,12,13,14,15]]
country_agg = pd.melt(country_agg,id_vars=["country"], var_name='Race', value_name='Percent')

# The bar chart at the top of the first page. It shows the total population of each state.
pop_bar_chart = alt.Chart(country).mark_bar().encode(
    x = alt.X('State', sort = '-y'),
    y = alt.Y('TotalPop', title = 'Total Population'),
    tooltip = alt.Tooltip('TotalPop', format=',.0f')
).properties(
    height=400
).interactive()

st.altair_chart(pop_bar_chart, use_container_width=True)

# Create a single bar that shows the percent distribution of each race in each state
us_race_bar = alt.Chart(country_agg).mark_bar().encode(
    x = alt.X('sum(Percent)', axis=alt.Axis(format='.0%'), title=''),
    y = alt.Y('country', title = ''),
    color = 'Race',
    order = alt.Order('Percent', sort='descending'),
    tooltip=alt.Tooltip('Percent', format='.0%')
).properties(
    height=200
).interactive()

st.altair_chart(us_race_bar, use_container_width=True)

if st.checkbox('Show Data'):
    st.subheader('Data')
    st.write(country_agg)

