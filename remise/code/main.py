"""IFT3295 - TP1 - Programme principal (fourni, NE PAS MODIFIER).

Orchestration du TP: lecture des donnees, appels aux fonctions a completer
dans ``overlap.py`` et ``assembly.py``, ecriture des fichiers de sortie et
affichage des resultats. Les formats de sortie ci-dessous constituent le
contrat de correction: ils sont identiques pour toutes les copies.

La seule identite d'un read est son identifiant (en-tete du FASTQ, ex.
``READS_3``). L'index i (position dans le fichier) n'est qu'un detail interne
des algorithmes: ``main.py`` traduit toujours vers les identifiants dans les
sorties. Les figures et l'ordre affichent donc ``READS_i``, jamais des
numeros nus.

Commandes:
    python3 main.py chevauchement fichier.fastq
        Affiche le chevauchement maximal des 2 sequences du fichier (Q1.5):
            Score: <score>
            Alignement X: <x alignee>
            Alignement Y: <y alignee>
            Longueur: <longueur du chevauchement>

    python3 main.py assemblage fichier.fastq [seuil]
        Assemble les reads du fichier (Ex. 2) :
        1. ecrit ``overlap_matrix.csv`` (n lignes, n entiers separes par des
           virgules, sans entete; la ligne i correspond au read i du fichier);
        2. ecrit ``graphe.dot`` (graphe filtre par le seuil, noeuds nommes
           ``READS_1..READS_n``);
        3. affiche l'ordre d'assemblage (par identifiants) et les
           chevauchements consecutifs:
               Ordre: <identifiants READS_i separes par des virgules>
               Chevauchements: <longueurs separees par des virgules>
        4. ecrit ``fragment.fasta`` et affiche:
               Longueur fragment: <longueur>
"""

import argparse

import networkx as nx

from assembly import (
    SEUIL_DEFAUT,
    graphe_chevauchements,
    ordre_assemblage,
    reduction_transitive,
    sequence_finale,
)
from overlap import chevauchement_maximal, matrice_chevauchements
from utils import read_fastq_records

CHEVAUCHEMENT: str = "chevauchement"
ASSEMBLAGE: str = "assemblage"


def _lire_fastq(fichier: str) -> tuple[list[str], list[str]]:
    """Lit un FASTQ et retourne (identifiants, sequences), ou termine sinon."""
    enregistrements: list[tuple[str, str]] = read_fastq_records(fichier)
    if not enregistrements:
        raise SystemExit(f"Erreur: le fichier {fichier} ne contient aucune sequence")
    identifiants: list[str] = [identifiant for identifiant, _ in enregistrements]
    sequences: list[str] = [sequence for _, sequence in enregistrements]
    return identifiants, sequences


def _commande_chevauchement(args: argparse.Namespace) -> None:
    """Affiche le chevauchement maximal des deux premieres sequences."""
    _, sequences = _lire_fastq(args.fichier)
    if len(sequences) < 2:
        raise SystemExit(f"Erreur: {args.fichier} doit contenir au moins 2 sequences")
    score, alignement_x, alignement_y, longueur = chevauchement_maximal(
        sequences[0], sequences[1]
    )
    print(f"Score: {score}")
    print(f"Alignement X: {alignement_x}")
    print(f"Alignement Y: {alignement_y}")
    print(f"Longueur: {longueur}")


def _ecrire_matrice(scores: list[list[int]]) -> None:
    """Ecrit la matrice n x n dans ``overlap_matrix.csv`` (sans entete)."""
    with open("overlap_matrix.csv", "w") as fichier_csv:
        for ligne in scores:
            fichier_csv.write(",".join(str(valeur) for valeur in ligne) + "\n")


def _ecrire_fragment(fragment: str) -> None:
    """Ecrit la sequence assemblee dans ``fragment.fasta``."""
    with open("fragment.fasta", "w") as fichier_fasta:
        fichier_fasta.write(f">fragment\n{fragment}\n")


def _commande_assemblage(args: argparse.Namespace) -> None:
    """Pipeline complet d'assemblage: matrice, graphe, ordre, fragment."""
    identifiants, sequences = _lire_fastq(args.fichier)

    scores: list[list[int]] = matrice_chevauchements(sequences)
    _ecrire_matrice(scores)

    graphe: nx.DiGraph = graphe_chevauchements(scores, args.seuil)
    nx.drawing.nx_pydot.write_dot(
        nx.relabel_nodes(graphe, dict(enumerate(identifiants))), "graphe.dot"
    )

    reduit: nx.DiGraph = reduction_transitive(graphe)
    ordre: list[int] = ordre_assemblage(reduit)
    sequence, longueurs = sequence_finale(sequences, ordre)

    print("Ordre: " + ",".join(identifiants[index] for index in ordre))
    print("Chevauchements: " + ",".join(str(longueur) for longueur in longueurs))
    _ecrire_fragment(sequence)
    print(f"Longueur fragment: {len(sequence)}")


def _construire_parseur() -> argparse.ArgumentParser:
    """Construit le parseur de ligne de commande (sous-commandes)."""
    parseur: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="IFT3295-TP1",
        description="Assemblage de sequences (voir docstring du module).",
    )
    sous_commandes = parseur.add_subparsers(dest="commande", required=True)

    chevauchement: argparse.ArgumentParser = sous_commandes.add_parser(
        CHEVAUCHEMENT, help="chevauchement de 2 sequences"
    )
    chevauchement.add_argument("fichier", help="fichier FASTQ contenant les sequences")
    chevauchement.set_defaults(action=_commande_chevauchement)

    assemblage: argparse.ArgumentParser = sous_commandes.add_parser(
        ASSEMBLAGE, help="assemblage des reads"
    )
    assemblage.add_argument("fichier", help="fichier FASTQ contenant les reads")
    assemblage.add_argument(
        "seuil",
        nargs="?",
        type=int,
        default=SEUIL_DEFAUT,
        help="score minimum (defaut: 80)",
    )
    assemblage.set_defaults(action=_commande_assemblage)

    return parseur


def main() -> None:
    parseur: argparse.ArgumentParser = _construire_parseur()
    args: argparse.Namespace = parseur.parse_args()
    args.action(args)


if __name__ == "__main__":
    main()
