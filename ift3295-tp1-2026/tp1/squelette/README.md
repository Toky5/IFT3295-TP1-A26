# IFT3295 — TP1 : assemblage de séquences (guide de démarrage)

Vous complétez `overlap.py` et `assembly.py` ; tout le reste est fourni.

## 1. Contenu du dossier

| Fichier | Statut | Rôle |
| --- | --- | --- |
| `main.py` | fourni (NE PAS MODIFIER) | orchestration, écriture des sorties |
| `utils.py` | fourni (NE PAS MODIFIER) | lecture des fichiers FASTQ |
| `run.sh` | fourni (NE PAS MODIFIER) | pipeline complet en une commande |
| `overlap.py` | à compléter | Q1.5 et Ex. 2.1 (chevauchements) |
| `assembly.py` | à compléter | Ex. 2.2 et 2.3 (graphe, assemblage) |
| `reads.fq` | données | 20 reads à assembler |
| `requirements.txt` | fourni | dépendances pip |
| `setup.sh` / `setup.ps1` | fourni | crée le venv et installe les dépendances (macOS/Linux / Windows) |

Les 6 fonctions à implémenter (ne changez ni noms, ni signatures) :

- `overlap.py` : `chevauchement_maximal`, `matrice_chevauchements`
- `assembly.py` : `graphe_chevauchements`, `reduction_transitive`, `ordre_assemblage`, `sequence_finale`

## 2. Prérequis

Python **3.10 ou plus récent requis** (les annotations échouent sous 3.10) :

- **macOS** : `xcode-select --install` (fournit `python3`), ou Python depuis [python.org](https://www.python.org/downloads/).
- **Windows** : Python depuis [python.org](https://www.python.org/downloads/) en cochant « Add python.exe to PATH ».
- **Linux** : paquet de votre distribution, p. ex. `sudo apt install python3 python3-venv` (Debian/Ubuntu).

Vérification :

```bash
python3 --version
```

(Windows : utilisez `py` ou `python` partout où ce guide écrit `python3`.)

## 3. Installation

Depuis le dossier du TP, une seule commande crée le venv et installe les
dépendances :

```bash
bash setup.sh
```

- **Windows (PowerShell)** : `.\setup.ps1`
  (si PowerShell bloque les scripts : `powershell -ExecutionPolicy Bypass -File .\setup.ps1`)

Puis activez le venv (**à refaire à chaque nouvelle session de terminal**) :

- macOS/Linux : `source .venv/bin/activate`
- Windows (PowerShell) : `.\.venv\Scripts\Activate.ps1`
- Windows (Git Bash) : `source .venv/Scripts/activate`

Équivalent à la main, si vous préférez :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 4. Exécution

Q1.5 — chevauchement maximal des 2 premières séquences :

```bash
python3 main.py chevauchement reads.fq
```

Sortie attendue (une fois `chevauchement_maximal` implémentée) :

```text
Score: <score>
Alignement X: <ligne alignée>
Alignement Y: <ligne alignée>
Longueur: <longueur du chevauchement>
```

Ex. 2 — assemblage complet (seuil optionnel, défaut 80) :

```bash
python3 main.py assemblage reads.fq [seuil]
```

ou, de façon équivalente (macOS/Linux, venv actif requis) :

```bash
./run.sh [fichier] [seuil]
```

Écrit `overlap_matrix.csv` (20 lignes), `graphe.dot` et `fragment.fasta`, puis affiche :

```text
Ordre: READS_i,READS_j,...
Chevauchements: <longueurs séparées par des virgules>
Longueur fragment: <n>
```

## 5. Ce qui est attendu au départ

Tant que les 6 fonctions ne sont pas complétées, chaque commande s'arrête sur
`NotImplementedError` : état normal du squelette, pas une erreur à corriger.

Les doctests de `overlap.py` servent d'auto-validation :

```bash
python3 -m doctest overlap.py
```

Au départ, ils signalent `NotImplementedError` ; une fois la fonction complète,
le doctest se termine sans aucun message (des messages affichés = échec).

## 6. Dépannage

- `python3: command not found` (macOS) : lancez `xcode-select --install` ou installez Python depuis python.org, puis rouvrez le terminal.
- `pip: command not found` : utilisez `python3 -m pip install -r requirements.txt`.
- pydot / Graphviz : seul le paquet pip `pydot` est requis ; le binaire `dot` de Graphviz n'est **pas** nécessaire.
- « ERREUR: fichier de sortie manquant ou vide » (signalé par `run.sh`) : une des trois sorties (`overlap_matrix.csv`, `graphe.dot`, `fragment.fasta`) n'a pas été produite ; complétez la fonction correspondante.
- `ModuleNotFoundError: No module named 'networkx'` (ou `'Bio'`, `'pydot'`) :
  le venv n'est pas actif — refaites l'activation de l'étape 3 (Windows :
  `.venv\Scripts\activate`), puis relancez la commande.

## 7. Remise

- **Code** : archive zip du dossier, déposée sur Studium.
- **Rédactionnel** : PDF séparé (questions écrites des sections 1 à 4).
