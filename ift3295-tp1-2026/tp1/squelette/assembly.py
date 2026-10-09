"""IFT3295 - TP1 - Assemblage de fragments (Ex. 2.2 et 2.3).

Ce fichier est A COMPLETER. Regles:
* Completez uniquement le corps des fonctions ci-dessous.
* Ne modifiez ni les noms, ni les signatures, ni les types.
* Vous pouvez utiliser NetworkX pour representer et manipuler le graphe.
* Typez tous vos parametres et retours (types simples: int, str, list, ...).
* Le programme principal est ``main.py`` (fourni): il appelle les fonctions
  de ce module, il ne faut donc rien executer ici directement.
"""

import networkx as nx

SEUIL_DEFAUT: int = 80

# Les noeuds du graphe sont les entiers 0..n-1 (indices des reads); chaque
# arete porte l'attribut entier ``poids`` (= score du chevauchement).


def graphe_chevauchements(
    scores: list[list[int]], seuil: int = SEUIL_DEFAUT
) -> nx.DiGraph:
    """Construit le graphe oriente des chevauchements pertinents.

    Args:
        scores (list[list[int]]): Matrice carree des scores de chevauchement.
        seuil (int): Score minimal requis pour conserver une arete.

    Returns:
        nx.DiGraph: Graphe dont les noeuds sont les indices ``0..n-1``.
        Une arete ``(i, j)`` existe si ``scores[i][j] >= seuil``; son attribut
        ``poids`` vaut le score correspondant.
    """
    n: int = len(scores)
    graphe: nx.DiGraph = nx.DiGraph()
    graphe.add_nodes_from(range(n))
    for i in range(n):
        for j in range(n):
            if i != j and scores[i][j] >= seuil:
                graphe.add_edge(i, j, poids=scores[i][j])
    return graphe


def reduction_transitive(graphe: nx.DiGraph) -> nx.DiGraph:
    """Calcule la reduction transitive du graphe de chevauchement.

    Supprime une arete ``(u, v)`` lorsqu'un autre chemin simple de ``u`` a
    ``v`` subsiste. Pour un cycle de deux noeuds, conserve uniquement l'arete
    de plus grand poids.

    Args:
        graphe (nx.DiGraph): Graphe oriente dont les aretes portent un attribut
            entier ``poids``.

    Returns:
        nx.DiGraph: Copie reduite du graphe d'entree. Le graphe d'entree n'est
        pas modifie.
    """
    reduit: nx.DiGraph = graphe.copy()

    # Etape 1: cycles de deux noeuds (u -> v et v -> u): garder l'arete de
    # plus grand poids (en cas d'egalite, celle de plus petit indice source).
    for u, v in list(reduit.edges):
        if reduit.has_edge(u, v) and reduit.has_edge(v, u):
            if reduit[u][v]["poids"] >= reduit[v][u]["poids"]:
                reduit.remove_edge(v, u)
            else:
                reduit.remove_edge(u, v)

    # Etape 2: supprimer (u, v) s'il reste un autre chemin de u a v. On teste
    # les aretes de la plus faible a la plus forte, pour garder en priorite
    # les chevauchements les plus significatifs.
    aretes: list[tuple[int, int]] = sorted(
        reduit.edges, key=lambda arete: reduit[arete[0]][arete[1]]["poids"]
    )

    def chemin_existe(depart: int, arrivee: int) -> bool:
        """Recherche en profondeur: ``arrivee`` est-il atteignable?"""
        a_visiter: list[int] = [depart]
        vus: set[int] = {depart}
        while a_visiter:
            courant: int = a_visiter.pop()
            if courant == arrivee:
                return True
            for voisin in reduit.successors(courant):
                if voisin not in vus:
                    vus.add(voisin)
                    a_visiter.append(voisin)
        return False

    for u, v in aretes:
        poids: int = reduit[u][v]["poids"]
        reduit.remove_edge(u, v)
        if not chemin_existe(u, v):
            reduit.add_edge(u, v, poids=poids)  # arete necessaire: on la remet
    return reduit


def ordre_assemblage(graphe: nx.DiGraph) -> list[int]:
    """Trouve l'ordre d'assemblage des reads dans le graphe reduit.

    Args:
        graphe (nx.DiGraph): Graphe reduit produit par
            ``reduction_transitive``.

    Returns:
        list[int]: Indices des reads dans un chemin du graphe qui visite
        chaque noeud exactement une fois. L'enonce garantit l'existence de
        ce chemin apres reduction.
    """
    n: int = graphe.number_of_nodes()

    def explorer(chemin: list[int], visites: set[int]) -> list[int] | None:
        """Recherche en profondeur d'un chemin visitant tous les noeuds."""
        if len(chemin) == n:
            return chemin
        for voisin in graphe.successors(chemin[-1]):
            if voisin not in visites:
                visites.add(voisin)
                chemin.append(voisin)
                trouve: list[int] | None = explorer(chemin, visites)
                if trouve is not None:
                    return trouve
                chemin.pop()
                visites.remove(voisin)
        return None

    # On part d'abord des noeuds sans arete entrante (debut naturel du chemin).
    departs: list[int] = sorted(graphe.nodes, key=lambda u: graphe.in_degree(u))
    for depart in departs:
        trouve = explorer([depart], {depart})
        if trouve is not None:
            return trouve
    raise ValueError("Aucun chemin ne visite tous les noeuds du graphe")


def sequence_finale(reads: list[str], ordre: list[int]) -> tuple[str, list[int]]:
    """Assemble les reads en une sequence de fragment genomique.

    Args:
        reads (list[str]): Sequences des reads a assembler.
        ordre (list[int]): Indices des reads dans l'ordre d'assemblage.

    Returns:
        tuple[str, list[int]]: Tuple contenant la sequence assemblee et les
        longueurs des chevauchements entre les paires de reads consecutifs,
        dans l'ordre.
    """
    if not ordre:
        return "", []
    fragment: str = reads[ordre[0]]
    longueurs: list[int] = []
    for precedent, suivant in zip(ordre, ordre[1:]):
        x: str = reads[precedent]
        y: str = reads[suivant]
        # Meilleur chevauchement suffixe(x)/prefixe(y) sans trou: les reads
        # consecutifs ne different que par des erreurs de substitution.
        # Memes poids que overlap.py: match +4, mismatch -4.
        meilleure_longueur: int = 0
        meilleur_score: int = 0
        for k in range(1, min(len(x), len(y)) + 1):
            score: int = sum(
                4 if a == b else -4 for a, b in zip(x[len(x) - k :], y[:k])
            )
            if score > meilleur_score:
                meilleur_score = score
                meilleure_longueur = k
        fragment += y[meilleure_longueur:]
        longueurs.append(meilleure_longueur)
    return fragment, longueurs
