# Importation des bibliothèques nécessaires
import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import googlemaps
from datetime import datetime

# Chemin vers le fichier Excel contenant les données
EXCEL_FILE = 'Data/BDD_Test.xlsx'

def charger_donnees(filename):
    """
    Charge les données depuis un fichier Excel spécifié et retourne un DataFrame Pandas.
    Seules les colonnes 'ID_Photo', 'Latitude', 'Longitude', 'Etat' sont conservées.
    """
    return pd.read_excel(filename, usecols=['ID_Photo', 'Latitude', 'Longitude', 'Etat'])

def sauvegarder_donnees(df, filename):
    """
    Sauvegarde le DataFrame donné dans un fichier Excel spécifié, en écrasant la feuille si elle existe déjà.
    """
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False)

def afficher_carte(df, etat_selectionne, chemin_optimise=False):
    """
    Affiche une carte avec des marqueurs pour les points d'intérêt basés sur l'état sélectionné.
    Si 'chemin_optimise' est True, calcule et affiche également un chemin optimisé.
    """
    # Créer une carte centrée sur Colombes, Île-de-France
    m = folium.Map(location=[48.9172, 2.2444], zoom_start=12)

    # Filtrer le DataFrame pour les points à afficher selon l'état sélectionné
    points_a_afficher = df[df['Etat'] == etat_selectionne]

    # Ajouter les points à la carte
    for _, point in points_a_afficher.iterrows():
        folium.Marker(
            location=[point['Latitude'], point['Longitude']],
            popup=str(point['ID_Photo']),
            tooltip=str(point['ID_Photo'])
        ).add_to(m)
    
    # Si chemin optimisé est demandé, appelle la fonction pour l'ajouter à la carte
    if chemin_optimise:
        itineraire_optimise(df, m)

    # Afficher la carte dans l'interface Streamlit
    folium_static(m)

def itineraire_optimise(df, carte_folium):
    """
    Calcule un itinéraire optimisé pour les points d'intérêt "à faire" et l'affiche sur la carte.
    Utilise l'API Google Maps pour le calcul de l'itinéraire.
    """
    # Initialiser le client Google Maps avec votre clé API
    gmaps = googlemaps.Client(key='AIzaSyATRus15DLa8CcQPqXbZdMgsUro5EoRpYM')

    # Filtrer les points "à faire"
    points_a_faire = df[df['Etat'] == 'à faire']

    # Définir le point de départ et d'arrivée et les waypoints
    depart_arrivee = 'Centre Technique Municipal, Colombes, 92'
    waypoints = points_a_faire[['Latitude', 'Longitude']].apply(lambda x: f'{x[0]},{x[1]}', axis=1).tolist()
    
    # Calculer l'itinéraire optimisé
    now = datetime.now()
    directions_result = gmaps.directions(depart_arrivee,
                                          depart_arrivee,
                                          waypoints=waypoints,
                                          mode="driving",
                                          departure_time=now)

    # Extraire et tracer l'itinéraire sur la carte
    if directions_result:
        steps = directions_result[0]['legs'][0]['steps']
        for step in steps:
            start_loc = [step['start_location']['lat'], step['start_location']['lng']]
            end_loc = [step['end_location']['lat'], step['end_location']['lng']]
            folium.PolyLine([start_loc, end_loc], color="blue", weight=2.5, opacity=1).add_to(carte_folium)

def afficher_interface(df):
    """
    Affiche l'interface utilisateur de l'application avec Streamlit.
    Permet de sélectionner un état, afficher la carte, rafraîchir les données, et mettre à jour un point d'intéret
    """

    # Titre de l'application
    st.title('Visualisation et Mise à jour des États')

    # Sélection d'un état pour filtrer les points d'intérêt sur la carte
    etat_selectionne = st.selectbox("Sélectionner un état pour visualiser les points correspondants", df['Etat'].unique())

    # Bouton pour générer un chemin optimisé sur la carte, basé sur l'état sélectionné
    if st.button('Générer chemin optimisé'):
        afficher_carte(df, etat_selectionne, chemin_optimise=True)
    else:
        afficher_carte(df, etat_selectionne)

    # Bouton pour rafraîchir les données à partir du fichier Excel
    if st.button('Rafraîchir les données'):
        df = charger_donnees(EXCEL_FILE)
        st.write(df)

    # Interface pour mettre à jour l'état d'un point d'intérêt spécifique
    selected_id = st.selectbox("Choisir l'ID de la photo à mettre à jour", df['ID_Photo'].unique())
    new_etat = st.selectbox("Nouvel État", ['fait', 'rejeté', 'à faire', 'en cours'])

    # Bouton pour appliquer la mise à jour de l'état dans le DataFrame et sauvegarder dans le fichier Excel
    if st.button('Mettre à jour l\'état'):
        index = df[df['ID_Photo'] == selected_id].index[0]  # Trouver l'index du point d'intérêt
        df.at[index, 'Etat'] = new_etat  # Mettre à jour l'état
        sauvegarder_donnees(df, EXCEL_FILE)  # Sauvegarder les modifications
        st.success('État mis à jour avec succès!')

def main():
    """
    Fonction principale qui charge les données, puis affiche l'interface utilisateur.
    """
    df = charger_donnees(EXCEL_FILE) # Charger les données à partir du fichier Excel
    afficher_interface(df) # Afficher l'interface utilisateur

if __name__ == "__main__":
    main()
