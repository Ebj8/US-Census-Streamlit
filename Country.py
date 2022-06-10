import streamlit as st
import pandas as pd
import numpy as np

st.title('2017 US Census Data Country Level')

@st.cache
def load_data(csv):
    data = pd.read_csv(csv)
    return data

data = load_data('acs2017_census_tract_data.csv')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)