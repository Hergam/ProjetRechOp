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
    en_tete = "    " + "  ".join(f"{nom:2}" for nom in noms)
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

def FF(matrice):
    n = len(matrice)
    t_atteignable = True
    while t_atteignable:
        noms = generer_noms_sommets(n)
        visites = [False] * n
        precedent = [None] * n
        
        file = []
        
        file.append(0)
        visites[0] = True
        printt("S")
        
        while file and not visites[n-1]:
            sommet = file.pop(0)
            sommets_visites = []
            predecesseurs = []
            
            for voisin in range(n):
                if matrice[sommet][voisin] > 0 and not visites[voisin]:
                    file.append(voisin)
                    visites[voisin] = True
                    precedent[voisin] = sommet
                    sommets_visites.append(noms[voisin])
                    predecesseurs.append(f"Pre({noms[voisin]})={noms[sommet]}")
            
            if sommets_visites:
                msg = f"{','.join(sommets_visites)}; {'; '.join(predecesseurs)}"
                printt(msg)

        # Reconstruction du chemin
        if not visites[n-1]:
            t_atteignable = False
            
        chemin = []
        sommet = n-1
        while sommet is not None:
            chemin.append(sommet)
            sommet = precedent[sommet]
        

        flot = 0

        for i,sommet in enumerate(chemin[:-1][::-1]):
            flot += matrice[sommet][chemin[i+1]]
        printt(f"Chemin trouvé : {chemin[::-1]} de flot {flot}")

    return chemin[::-1]


