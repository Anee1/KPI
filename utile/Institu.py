import streamlit as st
import pandas as pd
from KPI import nombre_clients, montant_souscrit_total, plot_histogramme_statut, taux_conversion, delai_median_conversion,pipeline_dormant,plot_pie_souscription_objectif
from filtre import clients_Anné, filtrer_par_Semaine, filtrer_par_mois, filtrer_par_commercial
from Formulairr import afficher_formulaire_et_tableau


import plotly.express as px


def afficher_onglet3():

    # =========================
# CONFIG PAGE
# =========================
    st.set_page_config(
    page_title="Tableau de Bord Institutionnel",
    page_icon="https://businesstodayng.com/wp-content/uploads/2025/06/IMG_0855.jpeg",
    layout="wide"
)

# --- Personnalisation CSS ---
    st.markdown("""
        <style>
        /* Couleur principale : rouge UCAMWAL */
        :root {
            --ucamwal-red: #C8102E;
        }

        /* Titres */
        h1, h2, h3 {
            color: var(--ucamwal-red);
        }

        /* Boutons */
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

        /* Tableau : entête rouge */
        .stDataFrame table thead th {
            background-color: var(--ucamwal-red) !important;
            color: white !important;
            font-weight: bold !important;
            text-align: center !important;
        }

        /* Corps du tableau */
        .stDataFrame table tbody td {
            text-align: center !important;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #fff5f5;
        }

        /* Pied de page */
        footer {
            background-color: #f5f5f5;
            color: #666;
            padding: 10px;
            text-align: center;
            border-top: 2px solid var(--ucamwal-red);
        }
        </style>
    """, unsafe_allow_html=True)


    Objectif_souscription_2026 = 70_000_000_000 # Objectif annuel de souscription en FCFA

    # --- Chargement des données ---
    df = pd.read_excel('Dataset commercial.xlsx')

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
        .metric-title {
            font-size: 14px;
            color: #555;
            font-weight: 500;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 28px;
            color: #1f77b4;
            font-weight: 700;
        }
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


    

    with st.expander("⚙️ Configuration des paramtres",expanded=False):
        periode = st.number_input ("Periode d'anlyse", min_value=1, max_value=200, value=12, step=1,key="nombre_3")
      

    df = filtrer_par_commercial (df, "KOUASSI NELLY")

    df = filtrer_par_Semaine (df, periode)

    # --- Calcul des KPI ---
    
    Objectif_realise_Annee = montant_souscrit_total(clients_Anné(df,2026))
    Taux_souscription_Annee = (Objectif_realise_Annee / Objectif_souscription_2026) * 100
    nombre_client = nombre_clients(df)
    montant_total = montant_souscrit_total(df)
    taux_conv = taux_conversion(df)
    delai_median, delai_moyen, variance_delai = delai_median_conversion(df)


    # --- KPI principaux (focus sur les objectifs annuels) ---
    st.subheader("🎯 Objectifs et performance")
    #st.info(f"🎯 Objectif de souscription 2026 : {Objectif_souscription_2026:,.0f} FCFA")
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Objectif 2026", f"{Objectif_souscription_2026:,.0f} FCFA")
       
    with col2:
        metric_card("Réalisation 2026", f"{Objectif_realise_Annee:,.0f} FCFA")
       
    with col3:
        metric_card("Taux de souscription 2026", f"{Taux_souscription_Annee:.2f} %")
       


    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(plot_histogramme_statut(df), use_container_width=True,key="hist_3")
    with col2:
        st.plotly_chart(plot_pie_souscription_objectif(df,Objectif_souscription_2026), use_container_width=True,key="pie_3")
    st.divider()


    #--- Dataframe des clients convertis ---

    st.subheader(f"📋 Détails des clients convertis sur les {periode} derniere semaines")
    show_clients = st.checkbox("Afficher les détails des clients convertis", value=True)
    
    if show_clients:
        st.dataframe(df)

    st.divider()

    # --- KPI secondaires (performance opérationnelle) ---
    st.subheader("📊 Indicateurs clés de performance")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Nombre de clients acquis", f"{nombre_client:,}")
    with col2:
        metric_card("Montant souscrit total", f"{montant_total:,.0f} FCFA")
    with col3:
        metric_card("Taux de conversion global", f"{taux_conv:.2f} %")
    with col4:
        metric_card("Délai moyen de conversion", f"{delai_moyen:.0f} jours")
    
        
        #metric_card("Délai moyen de conversion", f"{delai_moyen:.0f} jours")

    st.divider()

    # --- Pipeline dormant ---
    st.subheader("🛌 Pipeline dormant")
    prospects_converti = pipeline_dormant(df)
    st.info(f"Nombre de prospects dans le pipeline dormant : {prospects_converti}")


    st.divider()

  
# Appel de la fonction
    afficher_formulaire_et_tableau(form_key="form_institution",df_key="editor_prospects_instit")  # Assurez-vous que cette fonction n'a pas de widgets avec des key dupliquées

 
