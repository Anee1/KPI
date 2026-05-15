import streamlit as st
from KPI import nombre_clients, montant_souscrit_total, plot_histogramme_statut, taux_conversion, delai_median_conversion,pipeline_dormant,plot_pie_souscription_objectif
from filtre import clients_Anné, filtrer_par_Semaine, filtrer_par_mois, filtrer_par_commercial
from Formulaire import afficher_formulaire_et_tableau
import streamlit as st
from chargement_data import load_commercial_data, load_partenariats_data

def afficher_onglet2():

    # =========================
    # CONFIG PAGE
    # =========================

  


    # --- Chargement des données ---
    df = load_commercial_data()

    #df = pd.read_excel('Dataset commercial.xlsx')

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

    # --- Expander paramètres ---
    with st.expander("⚙️ Configuration des paramtres", expanded=False):
        periode = st.number_input(
            "Période d'analyse (en semaines)",
            min_value=1,
            max_value=20000,
            value=12,
            step=1,
            key="periode_analysis"
        )

    # --- Filtrage des données ---
    df = filtrer_par_commercial(df, "KOUASSI NELLY")
    df = filtrer_par_Semaine(df, periode)
    Objectif_souscription_2026 = 33_333_333_335   # Objectif annuel de souscription en FCFA

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
        st.plotly_chart(plot_histogramme_statut(df), use_container_width=True,key="histogramme_statut")
    with col2:
        st.plotly_chart(plot_pie_souscription_objectif(df, Objectif_souscription_2026), use_container_width=True,key="pie_souscription_objectif")

    st.divider()

    # --- Dataframe des clients convertis ---
    st.subheader(f"📋 Détails des clients convertis sur les {periode} dernières semaines")
    show_clients = st.checkbox(
        "Afficher les détails des clients convertis",
        value=True,
        key="show_clients_checkbox"
    )
    if show_clients:
        st.dataframe(df)

    st.divider()

    # --- KPI secondaires ---
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

    st.divider()

    # --- Pipeline dormant ---
    st.subheader("🛌 Pipeline dormant")
    prospects_converti = pipeline_dormant(df)
    st.info(f"Nombre de prospects dans le pipeline dormant : {prospects_converti}")

    st.divider()

    # --- Appel de formulaire et tableau ---
    afficher_formulaire_et_tableau(form_key="form_personne_physique",df_key="editor_prospects_Phys")  # Assurez-vous que cette fonction n'a pas de widgets avec des key dupliquées

   
    


   

    
