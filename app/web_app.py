import streamlit as st
import streamlit.components.v1 as components
import requests 
import visualizer
import os

def normalizeaza_text(text):
    tabel = str.maketrans("ăâîșțĂÂÎȘȚ", "aaistAAIST")
    return text.translate(tabel)

st.set_page_config(layout="wide", page_title="Navigator Iași")

st.title("Navigator Iași")

@st.cache_data
def incarca_lista_strazi():
    if os.path.exists("src/nume_strazi.txt"):
        with open("src/nume_strazi.txt", "r", encoding="utf-8") as f:
            strazi = [linie.split(',')[0] for linie in f]
            return sorted(list(set(strazi)))
    return []

lista_strazi = incarca_lista_strazi()

col1, col2 = st.columns(2)
with col1:
    start = st.selectbox("Punct de plecare", lista_strazi, index=None, placeholder="Alege strada...")
with col2:
    end = st.selectbox("Destinație", lista_strazi, index=None, placeholder="Alege strada...")

if st.button("Calculează ruta optimă"):
    if start and end:
        start_curat = normalizeaza_text(start)
        end_curat = normalizeaza_text(end)
        
        with st.spinner("Motorul C++ calculează instant..."):
            url = "http://127.0.0.1:8085/get_route"
            params = {
                "start": start_curat,
                "end": end_curat
            }
            
            try:
                response = requests.get(url, params=params)
                
                if response.status_code == 200:
                    continut_raspuns = response.text
                    
                    if "EROARE:" in continut_raspuns:
                        st.error(continut_raspuns)
                    else:
                        os.makedirs("src", exist_ok=True)
                        with open("src/traseu.txt", "w", encoding="utf-8") as outFile:
                            outFile.write(continut_raspuns)
                        
                        harta_path = visualizer.genereaza_harta_html()
                        
                        if harta_path and os.path.exists(harta_path):
                            st.success("Traseu calculat cu succes!")
                    
                            with open(harta_path, "r", encoding='utf-8') as f:
                                components.html(f.read(), height=600)
                        else:
                            st.error("Eroare: Traseul a fost primit, dar nu s-a putut genera fișierul de hartă.")
                else:
                    st.error(f"Eroare de la serverul C++: Cod status {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Eroare critică: Nu m-am putut conecta la motorul C++. Asigură-te că 'navigator.exe' rulează în fundal într-un terminal!")
    else:
        st.warning("Te rog să selectezi ambele străzi!")