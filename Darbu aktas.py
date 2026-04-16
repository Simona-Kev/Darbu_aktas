import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML
import os

st.set_page_config(layout="wide")

st.title("Atliktų darbų aktas")

# --- HEADER (same level fix) ---
col1, col2 = st.columns(2)

with col1:
    worker = st.text_input("Darbus atliko:", "UAB „MASI Baltic“")

with col2:
    client = st.text_input("Užsakovas")

work_title = st.text_input("Darbų pavadinimas")

work_date = st.date_input("Data", value=date.today())

st.divider()

# --- DARBAI ---
st.subheader("Darbai")

darbai_df = st.data_editor(
    pd.DataFrame({
        "Darbo pavadinimas": [""],
        "Aprašymas": [""],
        "Atlikimo laikas": [""],
        "Pastabos": [""],
    }),
    num_rows="dynamic",
    use_container_width=True
)

# auto numbering with dot
darbai_df.insert(0, "Eil. Nr.", [f"{i}." for i in range(1, len(darbai_df) + 1)])

# --- MEDŽIAGOS ---
st.subheader("Medžiagos")

medziagos_df = st.data_editor(
    pd.DataFrame({
        "Medžiagos pavadinimas": [""],
        "Kiekis": [""],
        "Pastabos": [""],
    }),
    num_rows="dynamic",
    use_container_width=True
)

medziagos_df.insert(0, "Eil. Nr.", [f"{i}." for i in range(1, len(medziagos_df) + 1)])

st.divider()

# --- SIGNATURES ---
col3, col4 = st.columns(2)

with col3:
    perdave_company = st.text_input("Perdavė: Įmonė", "UAB „MASI Baltic“")
    perdave_position = st.text_input("Perdavė: Pareigos")
    perdave_name = st.text_input("Perdavė: Vardas Pavardė")

with col4:
    prieme_company = st.text_input("Priėmė: Įmonė")
    prieme_name = st.text_input("Priėmė: Vardas Pavardė")

# --- HTML ROW BUILDER ---
def df_to_rows(df):
    rows = ""
    for _, row in df.iterrows():
        rows += "<tr>"
        for val in row:
            rows += f"<td>{val}</td>"
        rows += "</tr>"
    return rows

# --- PDF ---
def generate_pdf():
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    replacements = {
        "{{ worker }}": worker,
        "{{ client }}": client,
        "{{ work_title }}": work_title,
        "{{ date }}": str(work_date),

        "{{ darbai_rows }}": df_to_rows(darbai_df),
        "{{ medziagos_rows }}": df_to_rows(medziagos_df),

        "{{ perdave_company }}": perdave_company,
        "{{ perdave_position }}": perdave_position,
        "{{ perdave_name }}": perdave_name,

        "{{ prieme_company }}": prieme_company,
        "{{ prieme_name }}": prieme_name,
    }

    for k, v in replacements.items():
        html = html.replace(k, str(v))

    base_path = os.path.abspath(".")
    return HTML(string=html, base_url=base_path).write_pdf()

# --- DOWNLOAD ---
if st.button("Generate PDF"):
    pdf = generate_pdf()

    st.download_button(
        "Download PDF",
        pdf,
        file_name="atliktu_darbu_aktas.pdf",
        mime="application/pdf"
    )
