import streamlit as st
import pandas as pd
from KPI import nb_campagnes_marketing, engagement_digital, nb_followers_campagnes, performance_volume_partenariats,taux_transformation_partenariat,nb_partenariats_conclus,nb_partenariats_inities

from Formulairr import afficher_formulaire_et_tableau


import plotly.express as px


def afficher_onglet4():

    # =========================
    # CONFIG PAGE
    # =========================

    # --- Personnalisation CSS ---
    st.markdown("""
        <style>
        :root { --ucamwal-red: #C8102E; }
        h1, h2, h3 { color: var(--ucamwal-red); }
        div.stButton > button:first-child {
            background-color: var(--ucamwal-red);
            color: white;
            border: none;
            border-radius: 8px;
            height: 3em;
            font-weight: bold;
            transition: 0.3s;
        }
        div.stButton > button:first-child:hover {
            background-color: #a00c25;
            color: #fff;
        }
        .stDataFrame table thead th {
            background-color: var(--ucamwal-red) !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
        }
        .stDataFrame table tbody td { text-align: center !important; }
        section[data-testid="stSidebar"] { background-color: #fff5f5; }
        footer {
            background-color: #f5f5f5;
            color: #666;
            padding: 10px;
            text-align: center;
            border-top: 2px solid var(--ucamwal-red);
        }
        .metric-card {
            padding: 20px 25px;
            border-radius: 12px;
            background-color: #f9f9f9;
            box-shadow: 0px 3px 10px rgba(0,0,0,0.10);
            text-align: center;
            margin-bottom: 10px;
        }
        .metric-title { font-size: 14px; color: #555; font-weight: 500; margin-bottom: 5px; }
        .metric-value { font-size: 28px; color: #1f77b4; font-weight: 700; }
        </style>
    """, unsafe_allow_html=True)


    # --- Chargement des données ---
    donné = pd.read_excel('../Imamiah Monney.xlsx', sheet_name=None)
    clé = list(donné.keys())
    Partenariat_df = donné[clé[0]]
    Campagne_df = donné[clé[1]]


    # --- Fonction pour afficher une carte KPI ---
    def metric_card(label, value):
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    Partenariat_init = nb_partenariats_inities(Partenariat_df)
    Partenariat_conclus = nb_partenariats_conclus(Partenariat_df)
    taux_transformations_partenariats =taux_transformation_partenariat(Partenariat_df)
    nb_campagnes_marketings = nb_campagnes_marketing(Campagne_df)
   


    
     # --- Affichage des KPI ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Partenariats Inities", Partenariat_init)
    with col2:
        metric_card("Partenariats Conclus", Partenariat_conclus)
    with col3:
        metric_card("Taux de Transformation", f"{taux_transformations_partenariats:.2f}%")
    with col4:
        metric_card("Campagnes Marketing", nb_campagnes_marketings)
    
    
    #st.write("Taux de Transformation des Partenariats:", taux_transformations_partenariats)