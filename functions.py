import numpy as np
import os
import copy
import time
# Variables globales
_traces_reinitialisees = set()
_current_proposal = None  # Stocke le numéro de proposition courante

# Ajout d'une variable globale pour le choix d'algorithme
algo = None

def set_current_proposal(num):
    global _current_proposal
    _current_proposal = num

def set_algo(choice):
    global algo
    algo = choice

def get_algo():
    return algo

def lire_matrice_graphe(n):
    nom_fichier = f"proposals/proposal_{n}.txt"
    with open(nom_fichier, 'r') as fichier:
        nbrSommet = int(fichier.readline().strip())
        lignes = [list(map(int, ligne.strip().split())) for ligne in fichier]
        
        if int(n) > 5:
            matrice_capacite = np.array(lignes[:nbrSommet])
            matrice_cout = np.array(lignes[nbrSommet:])
            # Ajustement pour permettre les arêtes de coût 0
            matrice_cout_mod = []
            for i in range(nbrSommet):
                row = []
                for j in range(nbrSommet):
                    cap = matrice_capacite[i][j]
                    cout = matrice_cout[i][j]
                    if cout == 0 and cap == 0:
                        row.append(None)
                    else:
                        row.append(cout)
                matrice_cout_mod.append(row)
            matrice_cout = np.array(matrice_cout_mod, dtype=object)
        else:
            matrice_capacite = np.array(lignes)
            matrice_cout = None
            
    return matrice_capacite, matrice_cout, nbrSommet

def ecrire_trace(numero_proposition, message):
    global _traces_reinitialisees
    
    # Créer le dossier traces s'il n'existe pas
    if not os.path.exists("traces"):
        os.makedirs("traces")
    
    nom_fichier = f"traces/I2-trace{numero_proposition}-{algo}.txt"
    
    # Si c'est la première écriture pour cette proposition dans cette exécution
    if numero_proposition not in _traces_reinitialisees:
        # Ouvrir en mode write (w) pour écraser le contenu
        mode = 'w'
        _traces_reinitialisees.add(numero_proposition)
    else:
        # Ouvrir en mode append (a) pour les écritures suivantes
        mode = 'a'
    
    with open(nom_fichier, mode) as fichier:
        fichier.write(f"{message}\n")

def generer_noms_sommets(n):
    """Génère les noms des sommets: s, a, b, c, ..., t"""
    noms = ['s']  # Premier sommet
    for i in range(1, n-1):
        noms.append(chr(96 + i))  # a, b, c, ...
    noms.append('t')  # Dernier sommet
    return noms

def affichage(matrice, numero_proposition):
    n = len(matrice)
    noms = generer_noms_sommets(n)
    
    # Afficher l'en-tête avec les noms des colonnes
    en_tete = "     " + "  ".join(f"{nom:2}" for nom in noms)
    printt(en_tete)
    
    # Afficher chaque ligne avec le nom du sommet
    for i in range(n):
        ligne = f"{noms[i]:2} |" + "  ".join(
            f"{val:2}" if val is not None else " ." for val in matrice[i]
        )
        printt(ligne)

def printt(message, numero_proposition=None):
    """Affiche le message dans la console et l'écrit dans le fichier de trace"""
    if numero_proposition is None:
        if _current_proposal is None:
            raise ValueError("No current proposal set")
        numero_proposition = _current_proposal
        
    if isinstance(message, np.ndarray):
        affichage(message, numero_proposition)
    else:
        print(message)
        ecrire_trace(numero_proposition, str(message))

def affichage_flot_max(matrice_originale, matrice_residuelle):
    n = len(matrice_originale)
    noms = generer_noms_sommets(n)
    
    # Afficher l'en-tête
    en_tete = "\nAffichage du graphe résiduel :"
    printt(en_tete)
    en_tete = "     " + "  ".join(f"{nom:3}" for nom in noms)
    printt(en_tete)
    
    # Pour chaque ligne
    for i in range(n):
        ligne = [f"{noms[i]:2} |"]
        for j in range(n):
            if matrice_originale[i][j] > 0:
                flot = matrice_originale[i][j] - matrice_residuelle[i][j]
                capacite = matrice_originale[i][j]
                ligne.append(f"{flot}/{capacite}")
            else:
                ligne.append("0")
        printt(" ".join(f"{val:4}" for val in ligne))

def FF(matrice):
    n = len(matrice)
    matrice_residuelle = matrice.copy()  # On travaille sur une copie
    flot_total = 0
    
    while True:  # On continue tant qu'on trouve un chemin
        noms = generer_noms_sommets(n)
        visites = [False] * n
        precedent = [None] * n
        
        file = []
        file.append(0)
        visites[0] = True
        printt("\nS")
        
        while file and not visites[n-1]:
            sommet = file.pop(0)
            sommets_visites = []
            predecesseurs = []
            
            for voisin in range(n):
                if matrice_residuelle[sommet][voisin] > 0 and not visites[voisin]:
                    file.append(voisin)
                    visites[voisin] = True
                    precedent[voisin] = sommet
                    sommets_visites.append(noms[voisin])
                    predecesseurs.append(f"Pre({noms[voisin]})={noms[sommet]}")
            
            if sommets_visites:
                msg = f"{','.join(sommets_visites)}; {'; '.join(predecesseurs)}"
                printt(msg)

        # Si on ne peut plus atteindre t, on arrête
        if not visites[n-1]:
            printt("Aucun chemin trouvé vers t, fin de l'algorithme.")
            break
            
        chemin = []
        sommet = n-1
        while sommet is not None:
            chemin.append(sommet)
            sommet = precedent[sommet]
        chemin = chemin[::-1]

        # Calcul du flot minimal sur le chemin
        flot = float('inf')
        for i in range(len(chemin)-1):
            u = chemin[i]
            v = chemin[i+1]
            if matrice_residuelle[u][v] < flot:
                flot = matrice_residuelle[u][v]
        
        # Mise à jour du graphe résiduel
        for i in range(len(chemin)-1):
            u = chemin[i]
            v = chemin[i+1]
            matrice_residuelle[u][v] -= flot
            matrice_residuelle[v][u] += flot
        
        flot_total += flot
        printt(f"Chemin trouvé : {chemin} de flot {flot}")
        printt(f"Flot total actuel : {flot_total}")

        # Affichage du graphe résiduel à chaque itération
        affichage_flot_max(matrice, matrice_residuelle)

    printt(f"Valeur du flot max = {flot_total}")
    return flot_total

def push_relabel(matrice):
    n = len(matrice)
    residual = matrice.copy()
    height = [0] * n
    height[0] = n
    excess = [0] * n

    noms = generer_noms_sommets(n)
    printt("\n")
    for v in range(n):
        if matrice[0][v] > 0:
            flow = matrice[0][v]
            residual[0][v] -= flow
            residual[v][0] += flow
            excess[v] += flow
            printt(f"Pousser {flow} unités de {noms[0]} vers {noms[v]}")
    affichage_flot_max(matrice, residual)  # Affiche après chaque push du pré-écoulement

    while True:
        u = -1
        for i in range(1, n-1):
            if excess[i] > 0:
                u = i
                break

        if u == -1:
            break

        pushed = False
        for v in range(n):
            if residual[u][v] > 0 and height[u] == height[v] + 1:
                flow = min(excess[u], residual[u][v])
                residual[u][v] -= flow
                residual[v][u] += flow
                excess[u] -= flow
                excess[v] += flow
                pushed = True
                printt(f"\nPousser {flow} unités de {noms[u]} vers {noms[v]}")
                affichage_flot_max(matrice, residual)  # Affiche après chaque push
                break

        if not pushed:
            min_height = float('inf')
            for v in range(n):
                if residual[u][v] > 0:
                    min_height = min(min_height, height[v])
            if min_height != float('inf'):
                height[u] = min_height + 1
                printt(f"\nRéétiqueter {noms[u]} à hauteur {height[u]}")

    max_flow = excess[n-1]
    printt(f"\nValeur du flot max = {max_flow}")
    return max_flow

def bellman_ford(matrice_cout):
    n = len(matrice_cout)
    source = 0  # sommet s

    # Initialisation
    distance = [float('inf')] * n
    predecesseur = [None] * n
    distance[source] = 0

    printt("\nExécution de l'algorithme de Bellman-Ford:")

    noms_sommets = generer_noms_sommets(n)
    en_tete = "k      " + "   ".join(f"{nom:3}" for nom in noms_sommets)
    printt(en_tete)

    ligne = "0 |  "
    for d in distance:
        if d == float('inf'):
            ligne += "inf   "
        else:
            ligne += f"{d:3}   "
    printt(ligne)

    for k in range(n):
        modified = False
        for u in range(n):
            for v in range(n):
                if matrice_cout[u][v] is not None:
                    if distance[u] != float('inf') and distance[v] > distance[u] + matrice_cout[u][v]:
                        modified = True
                        distance[v] = distance[u] + matrice_cout[u][v]
                        predecesseur[v] = u

        ligne = f"{k+1} |  "
        for d in distance:
            if d == float('inf'):
                ligne += "inf   "
            else:
                ligne += f"{d:3}   "
        printt(ligne)

        if not modified:
            printt(f"Aucune modification pendant l'itération {k+1}, fin de Bellman-Ford.")
            break

    chemin = []
    sommet = n-1  # sommet t
    while sommet is not None:
        chemin.append(sommet)
        sommet = predecesseur[sommet]
    chemin = chemin[::-1]
    strChemin = []
    for sommet in chemin:
        strChemin.append(noms_sommets[sommet])

    if distance[n-1] == float('inf'):
        printt(f"Plus court chemin: {strChemin[-1]}")
    else:
        printt(f"Plus court chemin: {' -> '.join(strChemin)} de coût {distance[n-1]}")

    return chemin, distance[n-1]

def flotCoutMin(matriceCout, matriceCapacite, flotRecherche):
    flotRecherche = int(flotRecherche)
        
    flot_total = 0
    cout_total = 0
    n = len(matriceCapacite)
    matriceCap = copy.deepcopy(matriceCapacite)
    matriceCo = copy.deepcopy(matriceCout)
    for i in range(n):
        for j in range(n):
            if matriceCap[i][j] == 0 and matriceCo[i][j] == 0:
                matriceCo[i][j] = None
            
    
    while True:
        chemin, cout = bellman_ford(matriceCo)
        if cout == float('inf'):
            printt("Pas de chemin trouvé, flot demandé inatteignable, fin de l'algorithme.\n")
            break
        flot_chemin = min(matriceCap[chemin[i]][chemin[i+1]] for i in range(len(chemin)-1))
        for i in range(len(chemin)-1):
            u = chemin[i]
            v = chemin[i+1]
            
            matriceCap[u][v] -= flot_chemin
            matriceCap[v][u] += flot_chemin
            if matriceCap[u][v] == 0:
                matriceCo[u][v] = None
            if matriceCap[v][u] == 0:
                matriceCo[v][u] = None
            # Mise à jour de la matrice de coût selon la nouvelle règle
            if matriceCap[v][u] > 0 and matriceCo[u][v] is not None:
                matriceCo[v][u] = -matriceCo[u][v]
        
        cout_flot = cout * flot_chemin
        flot_total += flot_chemin
        cout_total += cout_flot

        printt(f"\nFlot trouvé: {flot_chemin} avec coût {cout_flot}")
        printt(f"Flot total actuel: {flot_total} avec coût total {cout_total}")
        #affichage_flot_max(matriceCapacite, matriceCap)
        printt(matriceCo)
        if flot_total >= flotRecherche:
            printt("Flot recherché atteint ou dépassé, fin de l'algorithme.")
            break


