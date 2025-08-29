import streamlit as st
import sqlite3
import pandas

url = ''

st.title('IN Mapa🏠')
st.set_page_config(
    page_title="INN Mapa pronájmů",
    page_icon="🏠",
)

def filter_data(df):
    filtered_df = df.copy()
    if more_flats:
        filtered_df = filtered_df[filtered_df.groupby('gps')['gps'].transform('count') >= 2]

    if same_street_check:
        filtered_df = filtered_df[filtered_df['street'].duplicated(keep=False)]

    if unique_address:
        filtered_df = filtered_df.drop_duplicates(subset=['gps'])
        
    if selected_streets:
        filtered_df = filtered_df[filtered_df['street'].isin(selected_streets)]

    if selected_cities:
        filtered_df = filtered_df[filtered_df['city'].isin(selected_cities)]

    return filtered_df

@st.cache_data
def load_data():
    df = pandas.read_csv(url, skiprows=2)
    df[['lat', 'lon']] = df['gps'].str.split(',', expand=True)
    df['lat'] = df['lat'].astype(float)
    df['lon'] = df['lon'].astype(float)
    return df

with st.sidebar:
    st.image("./logo.png")
    more_flats = st.checkbox("Zobrazit jen místa, kde jsou 2 a více bytů")
    same_street_check = st.checkbox("Zobrazit jen stejnou ulici")
    unique_address = st.checkbox("Zobrazovat jen unikátní adresu")

df = load_data()
with st.sidebar:
    cities = df['city'].unique()
    selected_cities = st.multiselect('Select City', cities)
    if selected_cities:
        streets = df[df['city'].isin(selected_cities)]['street'].unique()
    else:
        streets = df['street'].unique()
    selected_streets = st.multiselect('Select Street', streets)
    
    
filtered = filter_data(df)
st.metric("Počet řádků v tabulce", len(filtered.index))
st.map(filtered, size=1)



