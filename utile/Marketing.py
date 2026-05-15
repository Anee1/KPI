

import streamlit as st
from KPI import graph_funnel_partenariats, graph_interactif_performance, nb_campagnes_marketing, engagement_digital, nb_followers_campagnes, performance_volume_partenariats,taux_transformation_partenariat,nb_partenariats_conclus,nb_partenariats_inities

from Formulairemak import afficher_formulaire_et_tableau

from chargement_data import load_commercial_data, load_partenariats_data

def afficher_onglet4():

    # =========================
    # CONFIG PAGE
    # =========================



    # --- Chargement des données ---
    donné = load_partenariats_data()

    #donné = pd.read_excel('Imamiah Monney.xlsx', sheet_name=None)
    '''
    clé = list(donné.keys())
    Partenariat_df = donné[clé[0]]
    Campagne_df = donné[clé[1]] 
    '''


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

    Partenariat_init = nb_partenariats_inities(donné)
    Partenariat_conclus = nb_partenariats_conclus(donné)
    taux_transformations_partenariats =taux_transformation_partenariat(donné)
    #nb_campagnes_marketings = nb_campagnes_marketing(donné)
   

    
     # --- Affichage des KPI ---
    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Partenariats Inities", Partenariat_init)
    with col2:
        metric_card("Partenariats Conclus", Partenariat_conclus)
    with col3:
        metric_card("Taux de Transformation", f"{taux_transformations_partenariats:.2f}%")
   
    
    '''
     # --- Affichage des graphiques ---
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(graph_funnel_partenariats(Partenariat_init, Partenariat_conclus), use_container_width=True)

    with col2:
        st.plotly_chart(graph_interactif_performance(donné), use_container_width=True )
    '''

    afficher_formulaire_et_tableau()
