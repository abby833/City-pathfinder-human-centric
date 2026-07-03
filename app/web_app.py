import streamlit as st
import streamlit.components.v1 as components
import subprocess
import visualizer
import os

def normalizeaza_text(text):
    tabel = str.maketrans("ăâîșțĂÂÎȘȚ", "aaistAAIST")
    return text.translate(tabel)

# Configurare pagina
st.set_page_config(layout="wide", page_title="Navigator Iași")

st.title("Navigator Iași")

# Incarc lista strazi
@st.cache_data
def incarca_lista_strazi():
    if os.path.exists("src/nume_strazi.txt"):
        with open("src/nume_strazi.txt", "r", encoding="utf-8") as f:
            strazi = [linie.split(',')[0] for linie in f]
            return sorted(list(set(strazi)))
    return []

lista_strazi = incarca_lista_strazi()

# Interfata
col1, col2 = st.columns(2)
with col1:
    start = st.selectbox("Punct de plecare", lista_strazi, index=None, placeholder="Alege strada...")
with col2:
    end = st.selectbox("Destinație", lista_strazi, index=None, placeholder="Alege strada...")

# Buton calcul
if st.button("Calculează ruta optimă"):
    start_curat = normalizeaza_text(start)
    end_curat = normalizeaza_text(end)
    if start and end:
        with st.spinner("Motorul C++ calculează..."):
            result = subprocess.run(["src/navigator.exe", start_curat, end_curat])
            
            if result.returncode == 0:
                #generez harta
                harta_path = visualizer.genereaza_harta_html()
                
                if harta_path and os.path.exists(harta_path):
                    st.success("Traseu calculat cu succes!")
                    #afisez harta
                    with open(harta_path, "r", encoding='utf-8') as f:
                        components.html(f.read(), height=600)
                else:
                    st.error("Eroare: Executabilul a rulat, dar nu a generat fișierul de hartă.")
            else:
                # Eroare în C++
                st.error(f"Eroare în C++: {result.stderr}")
    else:
        st.warning("Te rog să selectezi ambele străzi!")