import streamlit as st
import pandas as pd
import os

DB_FILE = "Dataset commercial.xlsx"

def charger_donnees():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_excel(DB_FILE)
            for col in ['Date_premier_contact', 'Date_conversion']:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col]).dt.date
            return df
        except Exception as e:
            return créer_nouveau_df()
    return créer_nouveau_df()

def créer_nouveau_df():
    return pd.DataFrame(columns=[
        "Date_premier_contact", "Date_conversion", "Commercial", "Commercial_ID",
        "Prospect_Nom", "Type_Client", "Secteur_Activité", "Produit", 
        "Statut", "Montant_souscription", "Souscription_espérée", "Mail", "Contact"
    ])

def sauvegarder_donnees(df):
    try:
        df.to_excel(DB_FILE, index=False)
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")

def afficher_formulaire_et_tableau(form_key="form_prospect", df_key="editor_prospects"):
    """Fonction principale à appeler sur vos pages Streamlit"""
    
    # Initialisation de la session
    if 'df' not in st.session_state:
        st.session_state.df = charger_donnees()

    st.title("📌 CRM : Dataset commercial")

    # --- SECTION 1 : ENREGISTREMENT ---
    with st.expander("➕ Enregistrer un nouveau prospect", expanded=False):
        with st.form(form_key, clear_on_submit=True):
            col1, col2 = st.columns(2)
            d_contact = col1.date_input("Date du premier contact")
            d_conv = col2.date_input("Date de conversion (optionnel)", value=None)

            nom = st.text_input("Nom du prospect / Entreprise")
            
            c1, c2, c3 = st.columns(3)
            comm = c1.selectbox("Commercial", ["Grace", "Nelly", "Imamiah"])
            prod = c2.selectbox("Produit", ["United Capital Sapphire", "United Capital Diamond"])
            stat = c3.selectbox("Statut", ["Prospect", "En discussion", "Converti", "Perdu"])

            c4, c5 = st.columns(2)
            m_sous = c4.number_input("Montant souscrit (XOF)", min_value=0.0)
            m_esp = c5.number_input("Souscription espérée (XOF)", min_value=0.0)

            mail = st.text_input("Email de contact")
            
            if st.form_submit_button("💾 Enregistrer dans le Dataset"):
                new_row = pd.DataFrame([{
                    "Date_premier_contact": d_contact,
                    "Date_conversion": d_conv,
                    "Commercial": comm,
                    "Prospect_Nom": nom,
                    "Produit": prod,
                    "Statut": stat,
                    "Montant_souscription": m_sous,
                    "Souscription_espérée": m_esp,
                    "Mail": mail
                }])
                
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                sauvegarder_donnees(st.session_state.df)
                st.success(f"Données ajoutées au fichier {DB_FILE}")
                st.rerun()

    # --- SECTION 2 : MODIFICATION ---
    st.divider()
    st.subheader("📋 Base de données (Modification interactive)")

    df_edited = st.data_editor(
        st.session_state.df,
        column_config={
            "Statut": st.column_config.SelectboxColumn("Statut", options=["Prospect", "En discussion", "Converti", "Perdu"]),
            "Date_conversion": st.column_config.DateColumn("Date de conversion"),
            "Montant_souscription": st.column_config.NumberColumn("Montant Final", min_value=0)
        },
        num_rows="dynamic",
        key=df_key
    )

    if st.button("💾 Appliquer les modifications au fichier Excel", key=f"btn_{df_key}"):
        st.session_state.df = df_edited
        sauvegarder_donnees(df_edited)
        st.success("Fichier mis à jour !")
