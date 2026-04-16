import streamlit as st
import pandas as pd
from datetime import date
from weasyprint import HTML
import os
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(layout="wide")

st.title("Atliktų darbų aktas")

# -----------------------------
# SESSION STATE INIT (IMPORTANT)
# -----------------------------
if "darbai_df" not in st.session_state:
    st.session_state.darbai_df = pd.DataFrame({
        "Darbo pavadinimas": [""],
        "Aprašymas": [""],
        "Atlikimo laikas": [""],
        "Pastabos": [""],
    })

if "medziagos_df" not in st.session_state:
    st.session_state.medziagos_df = pd.DataFrame({
        "Medžiagos pavadinimas": [""],
        "Kiekis": [""],
        "Pastabos": [""],
    })

# -----------------------------
# HEADER INPUTS
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    worker = st.text_input("Darbus atliko")

with col2:
    client = st.text_input("Užsakovas")

work_title = st.text_input("Darbų pavadinimas")

work_date = st.date_input("Data", value=date.today())

st.divider()

# -----------------------------
# DARBAI
# -----------------------------
st.subheader("Darbai")

st.session_state.darbai_df = st.data_editor(
    st.session_state.darbai_df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="darbai_editor"
)

# delete darbai
del_d = st.number_input("Ištrinti darbų eilutę", min_value=1, step=1)

if st.button("Ištrinti darbą"):
    df = st.session_state.darbai_df
    if len(df) >= del_d:
        st.session_state.darbai_df = df.drop(df.index[del_d - 1]).reset_index(drop=True)
        st.rerun()

# -----------------------------
# MEDŽIAGOS
# -----------------------------
st.subheader("Medžiagos")

st.session_state.medziagos_df = st.data_editor(
    st.session_state.medziagos_df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="medziagos_editor"
)

del_m = st.number_input("Ištrinti medžiagų eilutę", min_value=1, step=1)

if st.button("Ištrinti medžiagą"):
    df = st.session_state.medziagos_df
    if len(df) >= del_m:
        st.session_state.medziagos_df = df.drop(df.index[del_m - 1]).reset_index(drop=True)
        st.rerun()

st.divider()

# -----------------------------
# SIGNATURES
# -----------------------------
col3, col4 = st.columns(2)

with col3:
    perdave_company = st.text_input("Perdavė įmonė", "UAB „MASI Baltic“")
    perdave_position = st.text_input("Perdavė: Pareigos")
    perdave_name = st.text_input("Perdavė vardas")

with col4:
    prieme_company = st.text_input("Priėmė įmonė", "Klientas")
    prieme_name = st.text_input("Priėmė vardas")

st.subheader("Perdavė parašas")

canvas_perdave = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=150,
    width=300,
    drawing_mode="freedraw",
    key="sig_perdave"
)

st.subheader("Priėmė parašas")

canvas_prieme = st_canvas(
    fill_color="rgba(255, 255, 255, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#ffffff",
    height=150,
    width=300,
    drawing_mode="freedraw",
    key="sig_prieme"
)

def get_image(canvas):
    if canvas.image_data is None:
        return None

    img = Image.fromarray((canvas.image_data).astype("uint8"))
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

# -----------------------------
# HTML ROWS
# -----------------------------
def df_to_rows(df):
    rows = ""
    for i, row in enumerate(df.values, 1):
        rows += "<tr>"
        rows += f"<td>{i}.</td>"
        for v in row:
            rows += f"<td>{v}</td>"
        rows += "</tr>"
    return rows

# -----------------------------
# PDF GENERATION
# -----------------------------
def generate_pdf():
    with open("template.html", "r", encoding="utf-8") as f:
        html = f.read()
    perdave_sig = get_image(canvas_perdave)
    prieme_sig = get_image(canvas_prieme)
    
    replacements = {
        "{{ worker }}": worker,
        "{{ client }}": client,
        "{{ work_title }}": work_title,
        "{{ date }}": str(work_date),

        "{{ darbai_rows }}": df_to_rows(st.session_state.darbai_df),
        "{{ medziagos_rows }}": df_to_rows(st.session_state.medziagos_df),

        "{{ perdave_company }}": perdave_company,
        "{{ perdave_position }}": perdave_position,
        "{{ perdave_name }}": perdave_name,

        "{{ prieme_company }}": prieme_company,
        "{{ prieme_name }}": prieme_name,
        "{{ perdave_sig }}": f'<img src="data:image/png;base64,{perdave_sig}" style="height:60px;">' if perdave_sig else "",
        "{{ prieme_sig }}": f'<img src="data:image/png;base64,{prieme_sig}" style="height:60px;">' if prieme_sig else "",
    }
    
    for k, v in replacements.items():
        html = html.replace(k, str(v))

    base_path = os.path.abspath(".")
    return HTML(string=html, base_url=base_path).write_pdf()

# -----------------------------
# DOWNLOAD
# -----------------------------
if st.button("Generate PDF"):
    pdf = generate_pdf()

    st.download_button(
        "Download PDF",
        pdf,
        file_name="atliktu_darbu_aktas.pdf",
        mime="application/pdf"
    )
