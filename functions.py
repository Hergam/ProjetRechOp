import numpy as np
import os

# Variables globales
_traces_reinitialisees = set()
_current_proposal = None  # Stocke le numéro de proposition courante

def set_current_proposal(num):
    global _current_proposal
    _current_proposal = num

def lire_matrice_graphe(n):
    nom_fichier = f"proposals/proposal_{n}.txt"
    with open(nom_fichier, 'r') as fichier:
        nbrSommet = int(fichier.readline().strip())  # Lit la première ligne dans nbrSommet
        matrice = [list(map(int, ligne.strip().split())) for ligne in fichier]
    return np.array(matrice), nbrSommet

def ecrire_trace(numero_proposition, message):
    global _traces_reinitialisees
    
    # Créer le dossier traces s'il n'existe pas
    if not os.path.exists("traces"):
        os.makedirs("traces")
    
    nom_fichier = f"traces/I1-trace{numero_proposition}-FF.txt"
    
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
        ligne = f"{noms[i]:2} |" + "  ".join(f"{val:2}" for val in matrice[i])
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
    en_tete = "\nAffichage du flot max :"
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

    
    affichage_flot_max(matrice, matrice_residuelle)
    printt(f"Valeur du flot max = {flot_total}")
    return flot_total

def push_relabel(matrice):
    n = len(matrice)
    # Créer une copie de la matrice pour le graphe résiduel
    residual = matrice.copy()
    # Initialiser les hauteurs: source à n, autres à 0
    height = [0] * n
    height[0] = n
    # Initialiser les excès à 0
    excess = [0] * n
    
    # Pré-écoulement depuis la source
    for v in range(n):
        if matrice[0][v] > 0:
            flow = matrice[0][v]
            residual[0][v] -= flow
            residual[v][0] += flow
            excess[v] += flow
    
    while True:
        # Trouver un sommet avec excès positif
        u = -1
        for i in range(1, n-1):  # Skip source (0) and sink (n-1)
            if excess[i] > 0:
                u = i
                break
        
        if u == -1:  # Aucun sommet avec excès
            break
            
        # Essayer de push, sinon relabel
        pushed = False
        for v in range(n):
            if residual[u][v] > 0 and height[u] == height[v] + 1:
                # Push operation
                flow = min(excess[u], residual[u][v])
                residual[u][v] -= flow
                residual[v][u] += flow
                excess[u] -= flow
                excess[v] += flow
                pushed = True
                printt(f"Pousser {flow} unités de {generer_noms_sommets(n)[u]} vers {generer_noms_sommets(n)[v]}")
                if excess[u] == 0:
                    break
        
        if not pushed:
            # Relabel operation
            min_height = float('inf')
            for v in range(n):
                if residual[u][v] > 0:
                    min_height = min(min_height, height[v])
            if min_height != float('inf'):
                height[u] = min_height + 1
                printt(f"\nRéétiqueter {generer_noms_sommets(n)[u]} à hauteur {height[u]}")
    
    # Calculer le flot maximal (somme des excès au puits)
    max_flow = excess[n-1]
    printt(f"\nValeur du flot max = {max_flow}")
    
    # Afficher la matrice de flot final
    flow_matrix = np.zeros_like(matrice)
    for i in range(n):
        for j in range(n):
            if matrice[i][j] > 0:
                flow_matrix[i][j] = matrice[i][j] - residual[i][j]
    
    affichage_flot_max(matrice, residual)
    return max_flow


