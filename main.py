import numpy as np
from functions import *

# Demande à l'utilisateur le numéro de la proposition
numero_proposition = input("Entrez le numéro de la proposition que vous souhaitez exécuter : ")
set_current_proposal(numero_proposition)

# Exécute la proposition sélectionnée avec la fonction
try:
    matrice_graphe, nbrSommet = lire_matrice_graphe(numero_proposition)
    printt(f"Matrice du graphe pour la proposition {numero_proposition} :")
    printt(matrice_graphe)
except FileNotFoundError:
    message_erreur = f"Fichier de proposition 'proposal_{numero_proposition}.txt' introuvable."
    printt(f"ERREUR : {message_erreur}")

chemin = FF(matrice_graphe)
printt(chemin)