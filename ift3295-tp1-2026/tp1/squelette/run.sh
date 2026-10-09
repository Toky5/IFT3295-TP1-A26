#!/bin/bash
# IFT3295 - TP1 - Script d'execution (fourni, NE PAS MODIFIER).
# Usage: ./run.sh [fichier_reads.fastq] [seuil]
set -uo pipefail

cd "$(dirname "$0")"
PY="${PYTHON:-python3}"
READS="${1:-reads.fq}"
SEUIL="${2:-80}"

echo "=== Q1.5: chevauchement maximal (2 premieres sequences) ==="
"$PY" main.py chevauchement "$READS" || exit 1

echo "=== Ex. 2: assemblage des reads ==="
"$PY" main.py assemblage "$READS" "$SEUIL" || exit 1

# Contrat de correction: les trois fichiers de sortie doivent exister.
for f in overlap_matrix.csv graphe.dot fragment.fasta; do
	if [ ! -s "$f" ]; then
		echo "ERREUR: fichier de sortie manquant ou vide: $f" >&2
		exit 1
	fi
done
echo "=== OK: tous les fichiers de sortie sont presents ==="
