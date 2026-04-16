import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML

st.title("Atliktų darbų aktas")

worker = st.text_input("Darbus atliko")
client = st.text_input("Užsakovas")
work_date = st.date_input("Data", value=date.today())

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

# --- PDF GENERATION ---
def df_to_rows(df):
    rows = ""
    for i, row in df.iterrows():
        rows += "<tr>"
        for val in row:
            rows += f"<td>{val}</td>"
        rows += "</tr>"
    return rows


def generate_pdf(worker, client, work_date, darbai_df, medziagos_df):
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{ worker }}", worker)
    html = html.replace("{{ client }}", client)
    html = html.replace("{{ date }}", str(work_date))

    html = html.replace("{{ darbai_rows }}", df_to_rows(darbai_df))
    html = html.replace("{{ medziagos_rows }}", df_to_rows(medziagos_df))

    from weasyprint import HTML
    return HTML(string=html).write_pdf()

# --- BUTTON ---
if st.button("Generate PDF"):
    pdf_file = generate_pdf(worker, client, work_date, darbai_df, medziagos_df)

    st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name="atliktu_darbu_aktas.pdf",
        mime="application/pdf"
    )
