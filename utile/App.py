import streamlit as st
import pandas as pd
#from utile.KPI import *
from filtre import *
from Institu import *
from Personne_physique import *
from General import *
from Marketing import *


st.set_page_config(page_title="Pilotage Activité Commerciale", layout="wide")

st.markdown("""
<style>
div[data-baseweb="tab"] {
    font-size: 20px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div[data-baseweb="tab-list"] {
        justify-content: space-between;
    }
    div[data-baseweb="tab"] {
        flex-grow: 1;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)


# --- Configuration générale ---
logo_url = "https://unitedcapitalplcgroup.com/wp-content/uploads/2021/08/United-Capital-logo-websites.png"
st.set_page_config(
    page_title="Tableau de Bord Commercial",
    page_icon=logo_url,
    layout="wide",
)

# --- En-tête de page ---

#st.sidebar.image(logo_url, width=250, caption="Asset Management West Africa Limited")



col1, col2 = st.columns([3, 1])

with col1:
    st.title("  ")

with col2:
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    st.image(logo_url, width=300, caption="Asset Management West Africa Limited")
    st.markdown("</div>", unsafe_allow_html=True)

#st.title("📊 Activité Commerciale")


# --- Personnalisation CSS ---


# --- Structure des onglets ---
tab_general, tab_personne_physique, tab_institutionnel, tab_marketing = st.tabs(["🌍 Vue Générale", "👤 Personne Physique", "🏢 Institutionnel","🌐 Marketing"])

with tab_general:
    Objectif_souscription_2026 = 120_000_000_000  # Objectif annuel de souscription en FCFA
    st.subheader(f"🌍  Vue d’ensemble de l'activité commerciale | {Objectif_souscription_2026:,.0f} FCFA")
    st.divider()
    afficher_onglet1()


with tab_personne_physique:
    Objectif_souscription_2026 = 90_000_000_000   # Objectif annuel de souscription en FCFA
    st.subheader(f"👤 Tableau de bord Personne Physique Objectif {Objectif_souscription_2026:,.0f} FCFA")
    st.divider()
    afficher_onglet2()


with tab_institutionnel:
    Objectif_souscription_2026 = 70_000_000_000   # Objectif annuel de souscription en FCFA
    st.subheader(f"🏢 Tableau de bord Institutionnel Objectif {Objectif_souscription_2026:,.0f} FCFA")
    st.divider()
    afficher_onglet3()

with tab_marketing:
    st.subheader("🌐 Tableau de bord Marketing")
    st.divider()
    afficher_onglet4()

st.markdown("""
        <footer>
            &copy; 2026 UCAMWAL - Research Analyst  - Tous droits réservés.
        </footer>
    """, unsafe_allow_html=True)