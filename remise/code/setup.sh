#!/bin/bash
# IFT3295 - TP1 - Creation du venv et installation des dependances.
#
# Usage :
#   bash setup.sh      -> cree le venv (.venv) et installe les dependances
#   source setup.sh    -> en plus, active le venv dans votre terminal
#
# Apres l'execution, activez le venv avant de rouler le TP :
#   source .venv/bin/activate          (macOS/Linux)
#   source .venv/Scripts/activate      (Windows, Git Bash)
set -eu

cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"

# 1) Python present ?
if ! command -v "$PYTHON" >/dev/null 2>&1; then
	echo "ERREUR: $PYTHON introuvable — installez Python 3.10 ou plus recent"
	echo "(voir README.md, section 2), puis relancez ce script." >&2
	exit 1
fi

# 2) Version >= 3.10 (les annotations de type du TP l'exigent).
if ! "$PYTHON" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)'; then
	echo "ERREUR: Python 3.10+ requis, version trouvee :" "$("$PYTHON" --version 2>&1)" >&2
	echo "Installez une version recente (voir README.md, section 2)." >&2
	exit 1
fi

# 3) Creation du venv (une seule fois).
if [ ! -d .venv ]; then
	"$PYTHON" -m venv .venv
	echo "venv cree : .venv"
else
	echo "venv deja present : .venv"
fi

# 4) Installation des dependances (directement via le python du venv).
if [ -x .venv/bin/python ]; then
	VPY=.venv/bin/python
else
	VPY=.venv/Scripts/python
fi
"$VPY" -m pip install -q -r requirements.txt
echo "dependances installees."

# 5) Activation : efficace seulement si le script est SOURCE.
if [ "${BASH_SOURCE[0]:-$0}" = "$0" ]; then
	echo
	echo "Pour activer le venv dans votre terminal :"
	echo "  source .venv/bin/activate        (macOS/Linux)"
	echo "  source .venv/Scripts/activate    (Windows, Git Bash)"
else
	if [ -f .venv/bin/activate ]; then
		. .venv/bin/activate
	elif [ -f .venv/Scripts/activate ]; then
		. .venv/Scripts/activate
	fi
	echo "venv active dans ce terminal."
fi
