import streamlit as st
import sqlite3
from pandas import DataFrame

st.title('Sreality data🏠')
st.set_page_config(
    page_title="Sreality Data pronájmů",
    page_icon="🏠",
)

def add_street_and_town(df):
    "https://www.sreality.cz/detail/pronajem/byt/5+kk/praha-kolovraty-medunkova/3809104460"
    parts = df['Link'].str.split('-', expand=True)
    df['Town'] = parts[0].str.split('/', expand=True).iloc[:, -1] 
    subset = parts.iloc[:, 2:]    
    joined = subset.astype(str).agg('-'.join, axis=1)
    df['Street'] = joined.str.split('/', expand=True).iloc[:, 0].replace("-", " ")
    return df
    
def filter_data_rentier(df, rentier_filter):
    filtered_df = df.copy()

    if rentier_filter:
        filtered_df = filtered_df[filtered_df['RentierCompany'].isin(rentier_filter)]

    if town:
        filtered_df = filtered_df[filtered_df['Town'].str.lower().isin([t.lower() for t in town])]

    if same_location_check:
        filtered_df = filtered_df[filtered_df['Location'].duplicated(keep=False)]

    if same_street_check:
        filtered_df = filtered_df[filtered_df['Street'].duplicated(keep=False)]

    if unique_address:
        filtered_df = filtered_df.drop_duplicates(subset=['Location'])
    return filtered_df
@st.cache_data
def load_data():
    con = sqlite3.connect("offers.db")
    cur = con.cursor()
    data = cur.execute("""
        SELECT Id, Link, Name, Price, RentierName, RentierCompany, Location, Date, DateOfUnlisting
        FROM offers;
""")
    df = DataFrame(data.fetchall())
    df.columns = [desc[0] for desc in data.description]
    df = add_street_and_town(df)
    return df
with st.sidebar:
    st.image("./logo.png")
    st.write("Filtry:")
    rentier = st.pills("Výběr pronajímatele", ["Dokonalý nájemník", "STÁLÝ nájem", "Ideální nájemce"], selection_mode="multi")

    town = st.multiselect(
    "Město",
    ["Praha", "Brno", "České Budějovice"]
)
    same_location_check = st.checkbox("Zobrazit jen stejnou adresu")
    same_street_check = st.checkbox("Zobrazit jen stejnou ulici")
    unique_address = st.checkbox("Zobrazovat jen unikátní adresu")

df = load_data()
filtered = filter_data_rentier(df,rentier)
st.metric("Počet řádků v tabulce", len(filtered.index))
st.dataframe(filtered)
#st.data_editor(data)
#t.subheader(map)
#st.map(data)
