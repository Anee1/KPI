import pandas as pd
import numpy as np


#clients par année 
def clients_Anné(data,Annee):
    """
    clients acquis .

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données des clients.

    Returns:
        int: Le nombre de clients acquis en 2026.
    """
    data['Date_conversion'] = pd.to_datetime(data['Date_conversion'])
    clients_annee= data[
        (data['Statut'] == 'Converti') &
        (data['Date_conversion'].dt.year == Annee)
    ]

    return clients_annee

def filtrer_par_mois(data, mois):
    """
    Filtre les données pour ne conserver que celles des derniers 'mois' mois.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données.
        mois (int): Le nombre de mois à considérer.

    Returns:
        pd.DataFrame: Le DataFrame filtré.
    """


    data['Date_premier_contact'] = pd.to_datetime(data['Date_premier_contact'])
    data['Date_conversion'] = pd.to_datetime(data['Date_conversion'])

    date_ref = pd.Timestamp.today()

    # Fenêtre 3 mois glissants
    date_3_mois = date_ref - pd.DateOffset(months= mois)

    df_3_mois = data[
        (data['Statut'] == 'Converti') &
        (data['Date_conversion'] >= date_3_mois)
    ]

    return df_3_mois


def filtrer_par_Semaine(data, semaine):
    """
    Filtre les données pour ne conserver que celles des dernières 'semaine' semaines.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données.
        semaine (int): Le nombre de semaines à considérer.

    Returns:
        pd.DataFrame: Le DataFrame filtré.
    """
    data['Date_premier_contact'] = pd.to_datetime(data['Date_premier_contact'])
    data['Date_conversion'] = pd.to_datetime(data['Date_conversion'])

    date_ref = pd.Timestamp.today()

    # Fenêtre 3 semaines glissants
    date_3_semaines = date_ref - pd.DateOffset(weeks= semaine)

    df_3_semaines = data[
        (data['Statut'] == 'Converti') &
        (data['Date_conversion'] >= date_3_semaines)
    ]

    return df_3_semaines




def filtrer_par_commercial(data, commercial):
    """
    Filtre les données pour ne conserver que celles d'un commercial spécifique.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données.
        commercial (str): Le nom du commercial à filtrer.

    Returns:
        pd.DataFrame: Le DataFrame filtré.
    """
    df_commercial = data[data['Commercial'] == commercial]
    return df_commercial



def filtrer_par_statut(data, statut):
    """
    Filtre les données pour ne conserver que celles d'un statut spécifique.

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données.
        statut (str): Le statut à filtrer.

    Returns:
        pd.DataFrame: Le DataFrame filtré.
    """
    df_statut = data[data['Statut'] == statut]
    return df_statut


def filtrer_pipeline_actif(data):
    """
    Filtre les données pour ne conserver que les prospects dans le pipeline actif
    (ceux qui n'ont pas encore été convertis).

    Args:
        data (pd.DataFrame): Le DataFrame contenant les données.

    Returns:
        pd.DataFrame: Le DataFrame filtré.
    """
    df_pipeline_actif = data[data['Statut'] != 'Converti']
    return df_pipeline_actif


