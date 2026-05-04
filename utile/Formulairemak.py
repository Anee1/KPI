import streamlit as st
import pandas as pd
import os

# Nom du fichier mis à jour pour correspondre au nouveau contexte
DB_FILE = "suivi_partenariats.xlsx"

def charger_donnees():
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_excel(DB_FILE)
            if 'date_premier_contact' in df.columns:
                df['date_premier_contact'] = pd.to_datetime(df['date_premier_contact']).dt.date
            return df
        except Exception:
            return créer_nouveau_df()
    return créer_nouveau_df()

def créer_nouveau_df():
    # Colonnes basées strictement sur l'en-tête de votre image
    return pd.DataFrame(columns=[
        "nom_partenaire", "type_partenaire", "commercial_responsable", 
        "date_premier_contact", "statut", "origine_contact", 
        "objectif_volume", "volume_realise"
    ])

def sauvegarder_donnees(df):
    try:
        df.to_excel(DB_FILE, index=False)
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")

def afficher_formulaire_et_tableau():
    if 'df' not in st.session_state:
        st.session_state.df = charger_donnees()

    st.title("🤝 Gestion des Partenariats")

    

    # --- SECTION 1 : ENREGISTREMENT ---
    with st.expander("➕ Ajouter un nouveau partenaire", expanded=True):
        with st.form("form_partenaire", clear_on_submit=True):
            col1, col2, col3 = st.columns(3)
            nom = col1.text_input("Nom du partenaire")
            type_p = col2.selectbox("Type de partenaire", ["Apporteur d'affaires", "Institutionnel", "Distributeur", "Autre"])
            d_contact = col3.date_input("Date du premier contact")
            c1, c2, c3 = st.columns(3)
            
            origine = c1.text_input("Origine du contact (ex: LinkedIn, Salon)")
            stat = c2.selectbox("Statut", ["Prospect", "En discussion", "Actif", "Inactif"])
            mail = c3.text_input("Email de contact")



            c4, c5 , c6= st.columns(3)
            obj_vol = c4.number_input("Objectif volume (XOF)", min_value=0)
            vol_real = c5.number_input("Volume réalisé (XOF)", min_value=0)
            contact = c6.number_input("Contact téléphonique")

            if st.form_submit_button("💾 Enregistrer le partenaire"):
                new_row = pd.DataFrame([{
                    "nom_partenaire": nom,
                    "type_partenaire": type_p,
                    "commercial_responsable": "Imamiah",  # Valeur par défaut, à adapter selon votre logique métier 
                    "date_premier_contact": d_contact,
                    "statut": stat,
                    "origine_contact": origine,
                    "objectif_volume": obj_vol,
                    "volume_realise": vol_real,
                    "Contact": contact,
                    "Mail": mail


                }])
                
                st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
                sauvegarder_donnees(st.session_state.df)
                st.success("Partenaire ajouté avec succès !")
                st.rerun()


    # --- SECTION 2 : VISUALISATION ET MODIFICATION ---

    st.subheader("📋 Liste des Partenariats")

    df_display = st.session_state.df.copy()
    
    df_edited = st.data_editor(
        df_display,
        column_config={
            "statut": st.column_config.SelectboxColumn(
                "Statut", 
                options=["Prospect", "En discussion", "Actif", "Inactif"]
            ),
            "date_premier_contact": st.column_config.DateColumn("Premier Contact"),
            "objectif_volume": st.column_config.NumberColumn("Objectif", format="%d XOF"),
            "volume_realise": st.column_config.NumberColumn("Réalisé", format="%d XOF"),
            "Performance (%)": st.column_config.ProgressColumn("Performance", min_value=0, max_value=100)
        },
        num_rows="dynamic",
        key="editor_partenariats"
    )

    if st.button("💾 Sauvegarder les modifications Excel"):
        # On retire la colonne de calcul 'Performance (%)' avant de sauvegarder
        df_save = df_edited
            
        st.session_state.df = df_save
        sauvegarder_donnees(df_save)
        st.success("Base de données mise à jour !")


