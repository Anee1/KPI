import pandas as pd
import numpy as np
import plotly.express as px

#Nombre de nouveaux clients

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# 1. Nombre de clients
def nombre_clients(data):
    """Calcul du nombre total de clients dans le DataFrame."""
    try:
        data_clients = data[data['Statut'] == 'Converti']   
        return data_clients.shape[0]
    except Exception:
        return 0

# 2. Montant souscrit total
def montant_souscrit_total(data):
    """Calcul du montant total souscrit par les clients."""
    try:
        return data[data['Statut'] == 'Converti']['Montant_souscription'].sum()
    except Exception:
        return 0.0

# 3. Taux de conversion global
def taux_conversion(data):
    """Calcul du taux de conversion global."""
    try:
        total_prospects = data.shape[0]
        # Gestion de la division par 0
        if total_prospects == 0:
            return 0.0
            
        return data[data['Statut'] == 'Converti'].shape[0] / total_prospects
    except Exception:
        return 0.0

# 4. Délai médian de conversion
def delai_median_conversion(data):
    """Calcul du délai médian de conversion des prospects en clients."""
    try:
        df_conversion = data[data['Statut'] == 'Converti'].copy()
        
        # S'assurer que les dates sont bien au format datetime (ignore les erreurs)
        df_conversion['Date_conversion'] = pd.to_datetime(df_conversion['Date_conversion'], errors='coerce')
        df_conversion['Date_premier_contact'] = pd.to_datetime(df_conversion['Date_premier_contact'], errors='coerce')

        df_conversion['Delai_conversion'] = (
            df_conversion['Date_conversion'] - df_conversion['Date_premier_contact']
        ).dt.days

        delai_median = df_conversion['Delai_conversion'].median()
        delai_moyen = df_conversion['Delai_conversion'].mean()
        variance_delai = df_conversion['Delai_conversion'].var()
        
        return delai_median, delai_moyen, variance_delai
    except Exception:
        # Renvoie NaN (Not a Number) si le calcul est impossible
        return np.nan, np.nan, np.nan

# 5. Pipeline dormant
def pipeline_dormant(data):
    """Calcul du nombre de prospects dans le pipeline dormant."""
    try:
        pipeline_actif = data[data['Statut'] != 'Converti']
        return pipeline_actif['Prospect_Nom'].nunique()
    except Exception:
        return 0

# 6. Clients 2026
def clients_2026(data):
    """Calcul du nombre de clients acquis en 2026."""
    try:
        # errors='coerce' transforme les mauvaises dates en NaT au lieu de planter
        date_conv = pd.to_datetime(data['Date_conversion'], errors='coerce')
        clients_2026 = data[
            (data['Statut'] == 'Converti') &
            (date_conv.dt.year == 2026)
        ]
        return clients_2026.shape[0]
    except Exception:
        return 0

# 7. Histogramme Statut
def plot_histogramme_statut(df):
    """Affiche un graphique de répartition des clients."""
    try:
        statut_count = (
            df["Statut"]
            .dropna()
            .value_counts()
            .reset_index()
        )
        statut_count.columns = ["Statut", "Nombre"]

        if statut_count.empty:
            raise ValueError("Aucune donnée pour générer le graphique.")

        fig = px.bar(
            statut_count,
            x="Nombre",
            y="Statut",
            text="Nombre",
            orientation="h",
            title="Répartition des clients"
        )
        fig.update_traces(textposition="auto")
        fig.update_layout(
            title_x=0.5,
            xaxis_title="Nombre de clients",
            yaxis_title="Statut client",
            xaxis=dict(rangemode="tozero"),
            margin=dict(t=60, l=80, r=40, b=40)
        )
        return fig
    except Exception:
        # En cas d'erreur (DataFrame vide ou colonne inexistante), retourne un graphique vide avec un message
        fig = go.Figure()
        fig.update_layout(
            title="Répartition des clients indisponible",
            xaxis={"visible": False}, yaxis={"visible": False},
            annotations=[{"text": "Données insuffisantes", "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 20}}]
        )
        return fig

# 8. Taux effectif de souscription
def Taux_effectif_souscription(data):
    """Calcul du taux effectif de souscription."""
    try:
        souscription_esperee = data['Souscription_esperé'].sum()
        
        # Gestion de la division par 0
        if souscription_esperee == 0:
            return 0.0
            
        taux_effectif = (
            data[data['Statut'] == 'Converti']['Montant_souscription'].sum() /
            souscription_esperee
        )
        return taux_effectif
    except Exception:
        return 0.0



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_pie_souscription_objectif(df, objectif, colonne_montant="Montant_souscription"):
    """
    Affiche un diagramme circulaire comparant les souscriptions réalisées à l'objectif.
    Intègre une gestion complète des erreurs et des valeurs manquantes.
    """
    try:
        # Sécurité 1 : Vérification de la présence des données
        if df is None or df.empty or colonne_montant not in df.columns:
            raise ValueError("Données vides ou colonne introuvable.")

        # Sécurité 2 : Forcer la colonne en numérique (remplace les erreurs/textes par 0)
        montants = pd.to_numeric(df[colonne_montant], errors='coerce').fillna(0)

        # Sécurité 3 : S'assurer que l'objectif est bien un nombre
        try:
            objectif_num = float(objectif)
        except (ValueError, TypeError):
            objectif_num = 0.0

        # Calculs
        realise = montants.sum()
        reste = max(objectif_num - realise, 0)
        
        # Sécurité 4 : Éviter un graphique avec aucune donnée (0 réalisé et 0 objectif)
        if realise == 0 and reste == 0:
            raise ValueError("Aucun montant à afficher.")

        data_pie = pd.DataFrame({
            "Statut": ["Réalisées", "À atteindre"],
            "Montant": [realise, reste]
        })

        fig = px.pie(
            data_pie,
            names="Statut",
            values="Montant",
            hole=0,
            title="Souscriptions réalisées vs Objectif"
        )

        fig.update_traces(
            textinfo="percent+label",
            pull=[0.1, 0]  # mise en évidence du réalisé
        )

        fig.update_layout(
            title_x=0.5,
            showlegend=True,
            margin=dict(t=60, l=40, r=40, b=40)
        )

        return fig

    except Exception:
        # Sécurité Globale : Renvoie un graphique vide avec un message d'erreur clair
        # au lieu de faire planter l'interface avec un 'return None'
        fig = go.Figure()
        fig.update_layout(
            title="Souscriptions vs Objectif (Indisponible)",
            xaxis={"visible": False}, 
            yaxis={"visible": False},
            annotations=[{
                "text": "Données insuffisantes ou invalides", 
                "xref": "paper", 
                "yref": "paper", 
                "showarrow": False, 
                "font": {"size": 18}
            }]
        )
        return fig
    


# ─────────────────────────────────────────────
# DIGITAL_METRICS
# Colonnes : campaign_id, nom_campagne, type_campagne, canal,
#            date_lancement, date_fin, budget, impressions,
#            likes, comments, shares, followers_avant, followers_apres
# ─────────────────────────────────────────────

def nb_campagnes_marketing(data, annee=None, canal=None):
    """
    Nombre de campagnes marketing lancées.

    Args:
        data (pd.DataFrame): DIGITAL_METRICS
        annee (int, optional): Filtrer par année de lancement.
        canal (str, optional): Filtrer par canal (ex: 'LinkedIn', 'Email').

    Returns:
        int: Nombre de campagnes.
    """
    try:
        df = data.copy()
        df['date_lancement'] = pd.to_datetime(df['date_lancement'], errors='coerce')

        if annee is not None:
            df = df[df['date_lancement'].dt.year == annee]

        if canal is not None:
            df = df[df['canal'].str.strip().str.lower() == canal.strip().lower()]

        return df['campaign_id'].nunique()

    except Exception as e:
        print(f"Erreur dans nb_campagnes_marketing: {e}")
        return 0


def engagement_digital(data, annee=None, canal=None):
    """
    Visibilité & engagement digital (impressions, likes, comments, shares, taux d'engagement).

    Args:
        data (pd.DataFrame): DIGITAL_METRICS
        annee (int, optional): Filtrer par année.
        canal (str, optional): Filtrer par canal.

    Returns:
        dict: Indicateurs d'engagement.
    """
    try:
        df = data.copy()
        df['date_lancement'] = pd.to_datetime(df['date_lancement'], errors='coerce')

        if annee is not None:
            df = df[df['date_lancement'].dt.year == annee]

        if canal is not None:
            df = df[df['canal'].str.strip().str.lower() == canal.strip().lower()]

        if df.empty:
            return {
                'total_impressions': 0,
                'total_likes': 0,
                'total_comments': 0,
                'total_shares': 0,
                'taux_engagement': 0.0,
                'nb_campagnes': 0,
                'budget_total': 0.0
            }

        total_impressions = df['impressions'].sum()
        total_likes       = df['likes'].sum()
        total_comments    = df['comments'].sum()
        total_shares      = df['shares'].sum()
        budget_total      = df['budget'].sum()
        nb_campagnes      = df['campaign_id'].nunique()

        # Taux d'engagement = (likes + comments + shares) / impressions
        taux_engagement = (
            (total_likes + total_comments + total_shares) / total_impressions
            if total_impressions > 0 else 0.0
        )

        return {
            'total_impressions': int(total_impressions),
            'total_likes':       int(total_likes),
            'total_comments':    int(total_comments),
            'total_shares':      int(total_shares),
            'taux_engagement':   round(taux_engagement, 4),
            'nb_campagnes':      nb_campagnes,
            'budget_total':      round(float(budget_total), 2)
        }

    except Exception as e:
        print(f"Erreur dans engagement_digital: {e}")
        return {
            'total_impressions': 0, 'total_likes': 0,
            'total_comments': 0,   'total_shares': 0,
            'taux_engagement': 0.0,'nb_campagnes': 0,
            'budget_total': 0.0
        }


def nb_followers_campagnes(data, annee=None, canal=None):
    """
    Nombre de nouveaux followers générés par les campagnes digitales.
    Calculé comme : followers_apres - followers_avant

    Args:
        data (pd.DataFrame): DIGITAL_METRICS
        annee (int, optional): Filtrer par année.
        canal (str, optional): Filtrer par canal.

    Returns:
        dict: Total nouveaux followers et détail par canal.
    """
    try:
        df = data.copy()
        df['date_lancement'] = pd.to_datetime(df['date_lancement'], errors='coerce')

        if annee is not None:
            df = df[df['date_lancement'].dt.year == annee]

        if canal is not None:
            df = df[df['canal'].str.strip().str.lower() == canal.strip().lower()]

        if df.empty:
            return {'total_nouveaux_followers': 0, 'detail_par_canal': {}}

        df['nouveaux_followers'] = df['followers_apres'] - df['followers_avant']

        total = int(df['nouveaux_followers'].sum())

        detail = (
            df.groupby('canal')['nouveaux_followers']
            .sum()
            .astype(int)
            .to_dict()
        )

        return {
            'total_nouveaux_followers': total,
            'detail_par_canal': detail
        }

    except Exception as e:
        print(f"Erreur dans nb_followers_campagnes: {e}")
        return {'total_nouveaux_followers': 0, 'detail_par_canal': {}}


# ─────────────────────────────────────────────
# PARTNERSHIPS
# Colonnes : nom_partenaire, type_partenaire, commercial_responsable,
#            date_premier_contact, statut, origine_contact,
#            objectif_volume, volume_realise
# ─────────────────────────────────────────────

def nb_partenariats_inities(data, annee=None, commercial=None):
    """
    Nombre de nouveaux partenariats initiés.
    Statuts considérés comme "initié" : 'initié', 'en cours', 'contacté'

    Args:
        data (pd.DataFrame): PARTNERSHIPS
        annee (int, optional): Filtrer par année du premier contact.
        commercial (str, optional): Filtrer par commercial responsable.

    Returns:
        int: Nombre de partenariats initiés.
    """
    try:
        df = data.copy()
        df['date_premier_contact'] = pd.to_datetime(df['date_premier_contact'], errors='coerce')

        statuts_inities = ['initié', 'en cours', 'contacté', 'en negociation']
        df_inities = df[
            df['statut'].str.strip().str.lower().isin(statuts_inities)
        ]

        if annee is not None:
            df_inities = df_inities[df_inities['date_premier_contact'].dt.year == annee]

        if commercial is not None:
            df_inities = df_inities[
                df_inities['commercial_responsable'].str.strip().str.lower()
                == commercial.strip().lower()
            ]

        return df_inities.shape[0]

    except Exception as e:
        print(f"Erreur dans nb_partenariats_inities: {e}")
        return 0


def nb_partenariats_conclus(data, annee=None, commercial=None):
    """
    Nombre de nouveaux partenariats conclus.
    Statut considéré comme "conclu" : 'conclu', 'actif', 'signé'

    Args:
        data (pd.DataFrame): PARTNERSHIPS
        annee (int, optional): Filtrer par année du premier contact.
        commercial (str, optional): Filtrer par commercial responsable.

    Returns:
        int: Nombre de partenariats conclus.
    """
    try:
        df = data.copy()
        df['date_premier_contact'] = pd.to_datetime(df['date_premier_contact'], errors='coerce')

        statuts_conclus = ['conclu', 'actif', 'signé', 'signe']
        df_conclus = df[
            df['statut'].str.strip().str.lower().isin(statuts_conclus)
        ]

        if annee is not None:
            df_conclus = df_conclus[df_conclus['date_premier_contact'].dt.year == annee]

        if commercial is not None:
            df_conclus = df_conclus[
                df_conclus['commercial_responsable'].str.strip().str.lower()
                == commercial.strip().lower()
            ]

        return df_conclus.shape[0]

    except Exception as e:
        print(f"Erreur dans nb_partenariats_conclus: {e}")
        return 0


def taux_transformation_partenariat(data, annee=None, commercial=None):
    """
    Taux de transformation des partenariats (conclus / initiés).

    Returns:
        float: Taux entre 0 et 1.
    """
    try:
        inities = nb_partenariats_inities(data, annee, commercial)
        conclus = nb_partenariats_conclus(data, annee, commercial)

        if inities == 0:
            return 0.0

        return round(conclus / inities, 4)

    except Exception as e:
        print(f"Erreur dans taux_transformation_partenariat: {e}")
        return 0.0


def performance_volume_partenariats(data, annee=None):
    """
    Comparaison entre volume objectif et volume réalisé par les partenariats.

    Args:
        data (pd.DataFrame): PARTNERSHIPS
        annee (int, optional): Filtrer par année.

    Returns:
        dict: objectif_total, realise_total, taux_realisation, detail_par_partenaire.
    """
    try:
        df = data.copy()
        df['date_premier_contact'] = pd.to_datetime(df['date_premier_contact'], errors='coerce')

        if annee is not None:
            df = df[df['date_premier_contact'].dt.year == annee]

        if df.empty:
            return {
                'objectif_total': 0, 'realise_total': 0,
                'taux_realisation': 0.0, 'detail_par_partenaire': {}
            }

        objectif_total = df['objectif_volume'].sum()
        realise_total  = df['volume_realise'].sum()

        taux_realisation = (
            realise_total / objectif_total
            if objectif_total > 0 else 0.0
        )

        detail = (
            df.groupby('nom_partenaire')[['objectif_volume', 'volume_realise']]
            .sum()
            .to_dict(orient='index')
        )

        return {
            'objectif_total':      round(float(objectif_total), 2),
            'realise_total':       round(float(realise_total), 2),
            'taux_realisation':    round(float(taux_realisation), 4),
            'detail_par_partenaire': detail
        }

    except Exception as e:
        print(f"Erreur dans performance_volume_partenariats: {e}")
        return {
            'objectif_total': 0, 'realise_total': 0,
            'taux_realisation': 0.0, 'detail_par_partenaire': {}
        }