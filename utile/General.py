import streamlit as st
import pandas as pd
from KPI import (
    nombre_clients, montant_souscrit_total, plot_histogramme_statut,
    taux_conversion, delai_median_conversion, pipeline_dormant,
    plot_pie_souscription_objectif
)
from filtre import clients_Anné, filtrer_par_mois, filtrer_par_commercial
import plotly.express as px

def afficher_onglet1():
    # =========================
    # CONFIG PAGE
    # =========================
    

    # --- Chargement des données ---
    df = pd.read_excel('../Dataset commercial.xlsx')

    # --- Styles pour les cartes KPI ---
    st.markdown("""
        <style>
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

    # --- Paramètres de filtrage ---
    Commerciale = df['Commercial'].unique().tolist()
    Commerciale.insert(0, "Tous les commerciaux")

    with st.expander("⚙️ Configuration des paramtres", expanded=False):
        col1, col2 = st.columns([1, 1])
        Commercial = col1.selectbox(
            "Sélectionner un commercial",
            options=Commerciale,
            key="select_commercial"  # clé unique
        )
        moi = col2.number_input(
            "Période d'analyse",
            min_value=1,
            max_value=12,
            value=3,
            step=1,
            key="periode_analysis_onglet1"  # clé unique
        )

    # --- Filtrage des données ---
    if Commercial != "Tous les commerciaux":
        df = filtrer_par_commercial(df, Commercial)

    df = filtrer_par_mois(df, moi)

    Objectif_souscription_2026 = 120_000_000_000   # Objectif annuel de souscription en FCFA

    # --- Calcul des KPI ---
    Objectif_realise_Annee = montant_souscrit_total(clients_Anné(df, 2026))
    Taux_souscription_Annee = (Objectif_realise_Annee / Objectif_souscription_2026) * 100
    nombre_client = nombre_clients(df)
    montant_total = montant_souscrit_total(df)
    taux_conv = taux_conversion(df)
    delai_median, delai_moyen, variance_delai = delai_median_conversion(df)

    # --- KPI principaux ---
    st.subheader("🎯 Objectifs et performance")
    #st.info(f"🎯 Objectif de souscription 2026 : {Objectif_souscription_2026:,.0f} FCFA")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Objectif 2026", f"{Objectif_souscription_2026:,.0f} FCFA")
    with col2:
        metric_card("Réalisation 2026", f"{Objectif_realise_Annee:,.0f} FCFA")
    with col3:
        metric_card("Taux de souscription 2026", f"{Taux_souscription_Annee:.2f} %")

    # --- Graphiques ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_histogramme_statut(df), use_container_width=True,key="histogramme_statut_onglet1")
    with col2:
        st.plotly_chart(plot_pie_souscription_objectif(df, Objectif_souscription_2026), use_container_width=True,key="pie_souscription_objectif_onglet1")

    st.divider()

    # --- KPI secondaires ---
    st.subheader("📊 Indicateurs clés de performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Nombre de clients acquis", f"{nombre_client:,}")
    with col2:
        metric_card("Taux de conversion global", f"{taux_conv:.2f} %")
    with col3:
        metric_card("Montant souscrit total", f"{montant_total:,.0f} FCFA")
    with col4:
        metric_card("Délai moyen de conversion", f"{delai_moyen:.0f} jours")

    st.divider()

    # --- Pipeline dormant ---
    st.subheader("🛌 Pipeline dormant")
    prospects_converti = pipeline_dormant(df)
    st.info(f"Nombre de prospects dans le pipeline dormant : {prospects_converti}")

  
