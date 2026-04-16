import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML

st.set_page_config(layout="wide")

st.title("Atliktų darbų aktas")

# --- HEADER INPUTS ---
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
        "Eil. Nr.": [1],
        "Darbo pavadinimas": [""],
        "Aprašymas": [""],
        "Atlikimo laikas": [""],
        "Pastabos": [""],
    }),
    num_rows="dynamic",
    use_container_width=True
)

# --- MEDŽIAGOS ---
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

# --- HTML TABLE ROW BUILDER ---
def df_to_rows(df):
    rows = ""
    for i, row in df.iterrows():
        rows += "<tr>"
        for val in row:
            rows += f"<td>{val}</td>"
        rows += "</tr>"
    return rows

# --- PDF GENERATOR ---
def generate_pdf():
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{ worker }}", worker)
    html = html.replace("{{ client }}", client)
    html = html.replace("{{ date }}", str(work_date))

    html = html.replace("{{ darbai_rows }}", df_to_rows(darbai_df))
    html = html.replace("{{ medziagos_rows }}", df_to_rows(medziagos_df))

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
