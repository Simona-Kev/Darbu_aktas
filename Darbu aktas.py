import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML

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

# Auto numbering
darbai_df.insert(0, "Eil. Nr.", range(1, len(darbai_df) + 1))

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

# Auto numbering
medziagos_df.insert(0, "Eil. Nr.", range(1, len(medziagos_df) + 1))

st.divider()

# --- SIGNATURE INPUTS ---
st.subheader("Parašai")

col3, col4 = st.columns(2)

with col3:
    perdave_name = st.text_input("Perdavė - vardas")
    perdave_position = st.text_input("Perdavė - pareigos")

with col4:
    prieme_name = st.text_input("Priėmė - vardas")
    prieme_position = st.text_input("Priėmė - pareigos")

# --- HTML ROW BUILDER ---
def df_to_rows(df):
    rows = ""
    for _, row in df.iterrows():
        rows += "<tr>"
        for val in row:
            rows += f"<td>{val}</td>"
        rows += "</tr>"
    return rows

# --- PDF GENERATION ---
def generate_pdf():
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    replacements = {
        "{{ worker }}": worker,
        "{{ client }}": client,
        "{{ date }}": str(work_date),
        "{{ darbai_rows }}": df_to_rows(darbai_df),
        "{{ medziagos_rows }}": df_to_rows(medziagos_df),
        "{{ perdave_name }}": perdave_name,
        "{{ perdave_position }}": perdave_position,
        "{{ prieme_name }}": prieme_name,
        "{{ prieme_position }}": prieme_position,
    }

    for key, val in replacements.items():
        html = html.replace(key, str(val))

    return HTML(string=html, base_url=".").write_pdf()

# --- BUTTON ---
if st.button("Generate PDF"):
    pdf = generate_pdf()

    st.download_button(
        "Download PDF",
        pdf,
        file_name="atliktu_darbu_aktas.pdf",
        mime="application/pdf"
    )
