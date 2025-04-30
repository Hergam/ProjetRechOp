import numpy as np
from functions import *

while True:
    # Réinitialiser les traces pour chaque nouvelle exécution
    from functions import _traces_reinitialisees
    _traces_reinitialisees.clear()

    numero_proposition = input("Entrez le numéro de la proposition que vous souhaitez exécuter ou q pour quitter le programme : ")
    if numero_proposition.lower() == "q":
        print("Fin du programme.")
        break
    set_current_proposal(numero_proposition)

    algo = input("Choisissez l'algorithme (1: Ford-Fulkerson, 2: Push-Relabel, 3: Flot à coût minimal) : ")
    if algo == "1":
        set_algo("FF")
    elif algo == "2":
        set_algo("PR")
    elif algo == "3":
        set_algo("MIN")

    try:
        matrice_capacite, matrice_cout, nbrSommet = lire_matrice_graphe(numero_proposition)
        printt(f"Matrice de capacité pour la proposition {numero_proposition} :")
        printt(matrice_capacite)
        
        if matrice_cout is not None:
            printt(f"\nMatrice de coût pour la proposition {numero_proposition} :")
            printt(matrice_cout)
    except FileNotFoundError:
        message_erreur = f"Fichier de proposition 'proposal_{numero_proposition}.txt' introuvable."
        printt(f"ERREUR : {message_erreur}")

    if algo == "1":
        matriceFF = FF(matrice_capacite)
    elif algo == "2":
        matricePR = push_relabel(matrice_capacite)
    elif algo == "3" and matrice_cout is not None:
        flot_recherche = input("Entrez le flot recherché : ")
        flotCoutMin(matrice_cout, matrice_capacite, flot_recherche) 
    else:
        printt("Algorithme non valide ou matrice de coût non disponible pour cette proposition")