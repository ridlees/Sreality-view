import streamlit as st
import sqlite3
import pandas

url = '

st.title('IN data🏠')
st.set_page_config(
    page_title="IN Data pronájmů",
    page_icon="🏠",
)
def filter_data(df):
    filtered_df = df.copy()
    if town:
        filtered_df = filtered_df[filtered_df['city'].str.lower().isin([t.lower() for t in town])]

    if same_location_check:
        filtered_df = filtered_df[filtered_df['gps'].duplicated(keep=False)]

    if same_street_check:
        filtered_df = filtered_df[filtered_df['street'].duplicated(keep=False)]

    if unique_address:
        filtered_df = filtered_df.drop_duplicates(subset=['gps'])
    return filtered_df

@st.cache_data
def load_data():
    df = pandas.read_csv(url, skiprows=2)
    df = df.drop_duplicates(subset='appartment_id', keep='first')
    return df

with st.sidebar:
    st.image("./logo.png")
    town = st.multiselect(
    "Město",
    ["Praha", "Brno", "České Budějovice"]
)
    same_location_check = st.checkbox("Zobrazit jen stejnou adresu")
    same_street_check = st.checkbox("Zobrazit jen stejnou ulici")
    unique_address = st.checkbox("Zobrazovat jen unikátní adresu")

df = load_data()
filtered = filter_data(df)
st.metric("Počet řádků v tabulce", len(filtered.index))
st.dataframe(filtered)
