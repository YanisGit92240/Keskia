# Home.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurer le thème de Seaborn pour de belles visualisations
sns.set_theme(style="whitegrid")

# Fonction pour charger les données d'un fichier Excel spécifique
def load_data(year):
    file_path = f'Bilan_{year}.xlsx'
    data = pd.read_excel(file_path)
    return data

# Fonction pour créer un graphique linéaire
def plot_line_chart(data, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    for col in data.columns[1:-1]:  # Ignorer la première et dernière colonne ('ENCOMBRANTS' et 'TOTAL')
        ax.plot(data['ENCOMBRANTS'], data[col], marker='o', label=col)
    ax.set_ylabel('Valeur')
    ax.set_xlabel('Catégorie')
    ax.legend()
    ax.set_title(title)
    return fig

# Fonction pour créer un histogramme
def plot_histogram(data, title):
    fig, ax = plt.subplots()
    data.iloc[:, 1:-1].sum().plot(kind='bar', ax=ax)  # Somme pour chaque mois, ignorer 'ENCOMBRANTS' et 'TOTAL'
    ax.set_title(title)
    return fig

# Fonction pour créer un diagramme en camembert
def plot_pie_chart(data, title):
    total = data.iloc[:, 1:-1].sum(axis=1)  # Somme pour chaque catégorie
    fig, ax = plt.subplots()
    ax.pie(total, labels=data['ENCOMBRANTS'], autopct='%1.1f%%')
    ax.set_title(title)
    return fig

# Fonction pour créer une matrice de corrélation
def plot_correlation_matrix(data, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = data.iloc[:, 1:-1].corr()  # Exclure 'ENCOMBRANTS' et 'TOTAL'
    sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm', ax=ax)
    ax.set_title(title)
    return fig

# La fonction principale qui sera appelée par app.py
def main():
    st.title('Visualisation des données de propreté')

    # Choix de l'année pour la visualisation des données
    year = st.selectbox('Choisir une année pour la visualisation', ['19', '20', '21', '23'])

    # Chargement des données
    data = load_data(year)

    # Affichage des graphiques
    st.pyplot(plot_line_chart(data, f'Évolution mensuelle pour {year}'))
    st.pyplot(plot_histogram(data, f'Distribution mensuelle pour {year}'))
    st.pyplot(plot_pie_chart(data, f'Répartition par catégorie pour {year}'))
    st.pyplot(plot_correlation_matrix(data, f'Matrice de corrélation pour {year}'))

