import streamlit as st 
import pandas as pd
import sqlite3

con = sqlite3.connect("faces.db") 
cur = con.cursor()

df = pd.read_sql_query("SELECT * FROM faces", con)

st.title("Food Truck Data Visualization")
st.text("Faces seen:")
st.write(df)

st.bar_chart(df)

st.text("Currently this is keeping track of how many frames (y) have x people")

st.slider('Slider for fun', 0, 100, disabled=False)