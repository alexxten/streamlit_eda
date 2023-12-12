import pandas as pd
import streamlit as st

from vars import DATA_PREPARED


@st.cache_data
def load_data():
    return pd.read_csv(DATA_PREPARED)