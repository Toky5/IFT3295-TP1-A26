"""Fonctions utilitaires fournies avec le TP — NE PAS MODIFIER CE FICHIER.

Utilisez ces fonctions pour lire les fichiers FASTQ et FASTA. Elles sont
entierement typees: les retours sont sans ambiguite (voir chaque docstring).
"""

from Bio import SeqIO


def read_fastq_records(fastq_file: str) -> list[tuple[str, str]]:
    """Lit un fichier FASTQ et retourne (identifiant, sequence) par lecture.

    Args:
        fastq_file: Chemin vers le fichier FASTQ.

    Returns:
        Liste de couples ``(identifiant, sequence)`` dans l'ordre du fichier.
        L'identifiant est l'en-tete sans le ``@``. Retourne ``[]`` si le
        fichier est vide. C'est LA source de verite pour nommer les reads.
    """
    records: list[tuple[str, str]] = []
    for record in SeqIO.parse(fastq_file, "fastq"):
        records.append((str(record.id), str(record.seq)))
    return records


def read_sequences_from_fastq(fastq_file: str) -> list[str]:
    """Lit un fichier FASTQ et retourne les sequences qu'il contient.

    Args:
        fastq_file: Chemin vers le fichier FASTQ.

    Returns:
        Liste des sequences du fichier, dans l'ordre d'apparition. Retourne
        ``[]`` si le fichier est vide ou sans sequence. (Les identifiants
        sont ignores; utilisez ``read_fastq_records`` pour les conserver.)
    """
    return [sequence for _, sequence in read_fastq_records(fastq_file)]


def read_single_fasta_sequence(file_path: str) -> str:
    """Lit l'unique sequence d'un fichier FASTA (lignes enroulees gerees).

    Args:
        file_path: Chemin vers le fichier FASTA.

    Returns:
        La sequence, concatensee sans les caracteres de retour a la ligne.

    Raises:
        ValueError: Si le fichier est vide, sans en-tete ``>``, ou sans
            sequence.
    """
    sequence: str = ""
    with open(file_path, "r") as file:
        lines: list[str] = file.readlines()
        if not lines:
            raise ValueError("Le fichier FASTA est vide.")
        if not lines[0].startswith(">"):
            raise ValueError("Le fichier FASTA ne commence pas par un en-tete (>).")
        for line in lines[1:]:
            sequence += line.strip()
    if not sequence:
        raise ValueError("Le fichier FASTA ne contient aucune sequence.")
    return sequence


def read_fasta_sequences(file_path: str) -> dict[str, str]:
    """Lit un fichier FASTA et retourne identifiants -> sequences.

    Args:
        file_path: Chemin vers le fichier FASTA.

    Returns:
        Dictionnaire dont chaque cle est l'identifiant (sans le ``>``) et
        chaque valeur la sequence correspondante. Les sequences peuvent etre
        enroulees sur plusieurs lignes. Retourne ``{}`` si le fichier ne
        contient aucun en-tete.
    """
    sequences: dict[str, str] = {}
    current_id: str | None = None
    current_seq: list[str] = []
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith(">"):
                if current_id is not None:
                    sequences[current_id] = "".join(current_seq)
                current_id = line[1:]  # Enlever le '>'
                current_seq = []
            else:
                current_seq.append(line)
        if current_id is not None:
            sequences[current_id] = "".join(current_seq)
    return sequences
