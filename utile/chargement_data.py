import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data
def load_commercial_data():

    """Charge et nettoie les données commerciales depuis le cache."""
    file_path = Path(__file__).parent.parent / "Dataset commercial.xlsx"
    
    try:
        df = pd.read_excel(file_path)
        
        # Pré-traitement effectué UNE SEULE FOIS ici, pour toute l'application
        df['Date_premier_contact'] = pd.to_datetime(df['Date_premier_contact'], errors='coerce')
        df['Date_conversion'] = pd.to_datetime(df['Date_conversion'], errors='coerce')
        
        return df
    except FileNotFoundError:
        st.error(f"Erreur : Le fichier {file_path.name} est introuvable.")
        st.stop() # Stoppe l'exécution proprement dans l'interface UI


@st.cache_data
def load_partenariats_data():
    """Charge les données de partenariats et campagnes."""
    file_path = Path(__file__).parent.parent / "suivi_partenariats.xlsx"
    
    try:
        # sheet_name=None charge toutes les feuilles dans un dictionnaire
        donnees = pd.read_excel(file_path, sheet_name=None)
        return donnees
    except FileNotFoundError:
        st.error("Erreur : Le fichier de suivi des partenariats est introuvable.")
        st.stop()