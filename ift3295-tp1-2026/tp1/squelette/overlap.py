"""IFT3295 - TP1 - Algorithme de chevauchement de sequences (Q1.5, Ex. 2.1).

Ce fichier est A COMPLETER. Regles:
* Completez uniquement le corps des fonctions ci-dessous.
* Ne modifiez ni les noms, ni les signatures, ni les types, ni les constantes.
* Typez tous vos parametres et retours (types simples: int, str, list, ...).
* Le programme principal est ``main.py`` (fourni): il appelle les fonctions
  de ce module, il ne faut donc rien executer ici directement.
"""

MATCH: int = 4
MISMATCH: int = -4
INDEL: int = -8


def chevauchement_maximal(x: str, y: str) -> tuple[int, str, str, int]:
    """Calcule le meilleur chevauchement ordonne entre deux sequences.

    Un chevauchement aligne un suffixe de ``x`` avec un prefixe de ``y``.
    Programmation dynamique en O(|x| * |y|), avec ``V[i][j]`` = meilleur score
    d'un alignement entre un suffixe de ``x[:i]`` et ``y[:j]``:

    * ``V[i][0] = 0``: le debut de ``x`` peut etre ignore sans penalite;
    * ``V[0][j] = j * INDEL``: ``y`` doit etre aligne depuis son premier
      caractere;
    * le score optimal est ``max_j V[n][j]``: on termine a la fin de ``x``,
      mais la fin du chevauchement dans ``y`` est libre.

    Args:
        x (str): Premiere sequence a aligner.
        y (str): Deuxieme sequence a aligner.

    Returns:
        tuple[int, str, str, int]: Score maximal, deux lignes alignees et
        longueur du chevauchement.

    Examples:
        >>> chevauchement_maximal("ACCA", "CACGC")
        (8, 'CA', 'CA', 2)
        >>> chevauchement_maximal("CACGC", "ACCA")
        (4, 'ACGC', 'AC-C', 4)
    """
    n: int = len(x)
    m: int = len(y)

    # Remplissage de la table.
    table: list[list[int]] = [[0] * (m + 1) for _ in range(n + 1)]
    for j in range(1, m + 1):
        table[0][j] = j * INDEL
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score_diag: int = table[i - 1][j - 1] + (
                MATCH if x[i - 1] == y[j - 1] else MISMATCH
            )
            table[i][j] = max(
                score_diag,
                table[i - 1][j] + INDEL,  # x[i-1] contre un trou
                table[i][j - 1] + INDEL,  # trou contre y[j-1]
            )

    # Meilleure fin: derniere ligne; en cas d'egalite, on garde le
    # chevauchement le plus court (j minimal), donc le premier maximum.
    fin_j: int = max(range(m + 1), key=lambda j: (table[n][j], -j))
    score: int = table[n][fin_j]
    if score <= 0:
        return 0, "", "", 0  # aucun chevauchement utile

    # Retour arriere depuis (n, fin_j) jusqu'a ce que y soit epuise (j == 0).
    ligne_x: list[str] = []
    ligne_y: list[str] = []
    i: int = n
    j: int = fin_j
    while j > 0:
        if (
            i > 0
            and table[i][j]
            == table[i - 1][j - 1] + (MATCH if x[i - 1] == y[j - 1] else MISMATCH)
        ):
            ligne_x.append(x[i - 1])
            ligne_y.append(y[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and table[i][j] == table[i - 1][j] + INDEL:
            ligne_x.append(x[i - 1])
            ligne_y.append("-")
            i -= 1
        else:
            ligne_x.append("-")
            ligne_y.append(y[j - 1])
            j -= 1

    aligne_x: str = "".join(reversed(ligne_x))
    aligne_y: str = "".join(reversed(ligne_y))
    return score, aligne_x, aligne_y, len(aligne_x)


def matrice_chevauchements(reads: list[str]) -> list[list[int]]:
    """Construit la matrice des scores de chevauchement de toutes les paires.

    Args:
        reads (list[str]): Sequences a comparer, par exemple les 20 reads de
            ``reads.fq``.

    Returns:
        list[list[int]]: Matrice carree dont l'element ``[i][j]`` est le score
        maximal de la paire ordonnee ``(reads[i], reads[j])``. La diagonale
        contient des zeros.
    """
    n: int = len(reads)
    matrice: list[list[int]] = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                matrice[i][j] = chevauchement_maximal(reads[i], reads[j])[0]
    return matrice
