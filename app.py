import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import os
from flask import Flask, request, jsonify, flash
import torch
import Loc
import Admin
import Home

# Configurer la page
st.set_page_config(page_title="Lutte contre les dépôts sauvages", layout="wide")

def go_home():
    if st.button("Retour à l'accueil"):
        st.session_state.current_tab = 'Accueil'
        st.experimental_rerun()

def admin_login():
    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tstrête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()
    go_home()  # Bouton pour retourner à l'accueil
    st.title("Page de connexion Admin")
    username = st.text_input("Nom d'utilisateur", "Admin")
    password = st.text_input("Mot de passe", type="password")
    
    # Ici, vous pouvez améliorer la sécurité et la gestion des utilisateurs.
    if st.button("Se connecter"):
        if username == "Admin" and password == "Admin":
            st.session_state.current_tab = 'Admin'
            st.experimental_rerun()
        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")

# Ajout de la fonction Admin qui est supposée être définie dans Admin.py
def admin_page():
    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()
    go_home()  # Bouton pour retourner à l'accueil
    Admin.main()  

# Fonction pour l'onglet à propos :
def propos():

    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()
    go_home()  # Bouton pour retourner à l'accueil
    st.title("Bienvenue dans notre application de lutte contre les dépôts sauvages")

    with st.expander("Notre équipe"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.image("images/icon1.png", caption="Membre 1")
        with col2:
            st.image("images/icon2.png", caption="Membre 2")
        with col3:
            st.image("images/icon3.png", caption="Membre 3")
        with col4:
            st.image("images/icon4.jpeg", caption="Membre 4")

    with st.expander("Nos sponsors"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.image("images/sponsor1.jpeg", caption="Sponsor 1")
        with col2:
            st.image("images/sponsor2.png", caption="Sponsor 2")
        with col3:
            st.image("images/sponsor3.png", caption="Sponsor 3")

    with st.expander("Contact"):
            st.markdown("""
            <div style="background-color: #003366; padding: 10px; border-radius: 10px; margin-top: 25px;">
                <h2 style="color: white; text-align: center;">SERVICE PROPRETÉ</h2>
                <p style="color: white; text-align: center;">Centre technique municipal, route de l'Ancienne digue<br>
                92700 Colombes</p>
                <p style="color: white; text-align: center;">📞 0 800 892 700</p>
                <p style="text-align: center;"><a href="https://www.colombes.fr/environnement/proprete-1022.html" target="_blank" style="color: #FFD700; font-weight: bold;">CONTACTER PAR INTERNET</a></p>
            </div>
        """, unsafe_allow_html=True)
    

app = Flask(_name_)

load_model()

UPLOAD_FOLDER = "/tmp"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/predict', methods=['POST'])
def predict_duration():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        predictions = predict(filepath)
        os.remove(filepath)
        return jsonify(predictions if predictions else []), 200
    else:
        return jsonify({"error": "Invalid file extension"}), 400
# Fonction pour l'onglet Photographier
def photographier():
    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()
    go_home()  # Bouton pour retourner à l'accueil

    # Code CSS et bouton de retour comme avant...
    # Code JavaScript pour obtenir la géolocalisation
    js_code = """
    <script>
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const coords = [position.coords.latitude, position.coords.longitude];
            // Utiliser Streamlit pour envoyer les coordonnées au serveur
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: coords}, '*');
        },
        (error) => console.error(error)
    );
    </script>
    """
    
    # Bouton pour déclencher l'obtention de la géolocalisation
    if st.button('Obtenir ma localisation'):
        # Exécuter le script JavaScript pour obtenir la géolocalisation
        st.components.v1.html(js_code, height=0)

    # Récupérer les coordonnées mises à jour
    if 'coords' in st.session_state:
        latitude, longitude = st.session_state.coords
        st.write(f"Latitude: {latitude}, Longitude: {longitude}")
    
    st.title("Photographier ou charger une image")

    option_photo = st.radio("Souhaitez-vous prendre une photo ou charger une image existante ?", ('Prendre une photo', 'Charger une image'))

    photo = None
    if option_photo == 'Prendre une photo':
        photo = st.camera_input("Prenez une photo du déchet")
    else:
        uploaded_file = st.file_uploader("Choisissez une photo depuis votre galerie", type=["png", "jpg", "jpeg"])
        if uploaded_file:
            photo = uploaded_file

    if photo:
        # Convertir la photo Streamlit en une image PIL pour le traitement
        image = Image.open(photo)
        st.image(image, caption="Photo traitée")

        # Convertir l'image PIL en un format compatible avec votre modèle YOLO
        image_np = np.array(image.convert('RGB'))

        # Exécuter l'inférence du modèle sur l'image

        model_inference = torch.hub.load('Notebooks/yolov5', 'custom', path='Data/weights.pt', source='local')
        # Remarque : Assurez-vous que votre modèle est chargé (voir les étapes précédentes)
        results = model_inference(image_np)
        
        #Créer une API pour ne pas que sa plante lors de la mise en ligne
        #@route('/predict', methods=['POST'])


        # Créer une figure pour afficher l'image et les boîtes englobantes
        fig, ax = plt.subplots()
        ax.imshow(image_np)
        for *xyxy, conf, cls in results.xyxy[0]:
            x1, y1, x2, y2 = map(int, xyxy)
            rect = patches.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=2, edgecolor='r', facecolor='none')
            ax.add_patch(rect)
        plt.axis('off')

        # Utiliser Streamlit pour afficher la figure Matplotlib
        st.pyplot(fig)

def points_de_tri():
    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()
    go_home()  # Bouton pour retourner à l'accueil
    st.title("Points de tri à proximité")
    Loc.main()

def data_visualisation():
    # Ici, vous intégrez la fonctionnalité de visualisation des données.
    # Par exemple, vous pouvez avoir une fonction Home.main() qui contient tout le code de visualisation
    Home.main()

# Fonction pour l'onglet Accueil avec ajout du bouton Admin
def accueil():


    # Utiliser du CSS personnalisé pour cacher le titre et la marge par défaut et simuler un en-tête personnalisé
    hide_streamlit_style = """
                <style>
                /* Supprimer le titre et le logo Streamlit pour simuler un en-tête personnalisé */
                header {visibility: hidden;}
                /* Supprimer les espaces autour du contenu principal */
                .block-container {padding-top: 0;}
                /* Supprimer la marge du haut de la première div qui contient le contenu */
                .element-container:first-child {padding-top: 0px;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Utiliser st.empty pour conserver un emplacement en haut de la page pour vos boutons
    header_space = st.empty()

    # Placer les boutons dans le conteneur réservé
    with header_space.container():
        col1, col2, col3, col4, col5 = st.columns([1, 2, 2, 2, 2], gap="small")
        col1.markdown("**Click & Collect**")  # Remplacer par une icône si nécessaire
        if col2.button("Photographier"):
            st.session_state.current_tab = 'Photographier'
            st.experimental_rerun()
        if col3.button("Points de tri à proximité"):
            st.session_state.current_tab = 'Points de tri à proximité'
            st.experimental_rerun()
        if col4.button("À propos"):
            st.session_state.current_tab = 'À propos'
            st.experimental_rerun()
        if col5.button("Admin"):
            st.session_state.current_tab = 'Login Admin'
            st.experimental_rerun()


# Ajout de la page de connexion Admin et de la page Admin aux onglets
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'Accueil'

if st.session_state.current_tab == 'Accueil':
    accueil()
    data_visualisation()
elif st.session_state.current_tab == 'À propos':
    propos()
elif st.session_state.current_tab == 'Photographier':
    photographier()
elif st.session_state.current_tab == 'Points de tri à proximité':
    points_de_tri()
elif st.session_state.current_tab == 'Login Admin':
    admin_login()
elif st.session_state.current_tab == 'Admin':
    admin_page()