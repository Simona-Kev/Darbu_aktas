import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(layout="wide")

st.title("Atliktų darbų aktas")

# --- HEADER ---
col1, col2 = st.columns(2)

with col1:
    worker = st.text_input("Darbus atliko")

with col2:
    client = st.text_input("Užsakovas")

work_date = st.date_input("Data", value=date.today())

st.divider()

# --- DARBAI TABLE ---
st.subheader("Darbai")

darbai_df = st.data_editor(
    pd.DataFrame({
        "Eil. Nr.": [1],
        "Darbo pavadinimas": [""],
        "Aprašymas": [""],
        "Atlikimo laikas": [""],
        "Pastabos": [""],
    }),
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

# --- MEDŽIAGOS TABLE ---
st.subheader("Medžiagos")

medziagos_df = st.data_editor(
    pd.DataFrame({
        "Eil. Nr.": [1],
        "Medžiagos pavadinimas": [""],
        "Kiekis": [""],
        "Pastabos": [""],
    }),
    num_rows="dynamic",
    use_container_width=True
)

st.divider()

# --- OUTPUT ---
if st.button("Generate preview"):
    st.subheader("Preview")

    st.write("**Darbus atliko:**", worker)
    st.write("**Užsakovas:**", client)
    st.write("**Data:**", work_date)

    st.write("### Darbai")
    st.dataframe(darbai_df)

    st.write("### Medžiagos")
    st.dataframe(medziagos_df)
