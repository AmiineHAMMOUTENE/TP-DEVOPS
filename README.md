# Pipeline de données Bureau&Co

Auteur : Amine Hammoutene

Ce projet nettoie le fichier des ventes de Bureau&Co et calcule le chiffre d'affaires par ville et par catégorie de produit. Tout est automatisé : le code est versionné avec Git, vérifié par des tests, exécuté par une intégration continue (GitHub Actions) et emballé dans une image Docker.

Ce README raconte ce que j'ai fait, étape par étape, et ce que j'en retiens.

## Comment lancer le projet

```bash
pip install -r requirements.txt   # installer les dépendances
python pipeline.py                # exécuter le pipeline
pytest -v                         # lancer les tests
ruff check .                      # vérifier la qualité du code
```

Avec Docker :

```bash
docker build -t pipeline-data .
docker run --rm -v "$(pwd)/output:/app/output" pipeline-data
```

Les résultats sont écrits dans le dossier `output/` : `ventes_propres.csv`, `ca_par_ville.csv` et `ca_par_categorie.csv`.

## Ce que fait le pipeline

Le pipeline suit les trois temps d'un ETL.

| Temps | Fonction | Ce qu'elle fait |
|---|---|---|
| Extraire | `extraire` | lit `data/ventes.csv` |
| Transformer | `transformer` | supprime les doublons, enlève les lignes sans quantité ou sans prix, garde les quantités positives, uniformise les villes, calcule le montant |
| Charger | `charger` | écrit les résultats en CSV dans `output/` |

Sur le fichier fourni, le pipeline lit 12 lignes et en garde 9. Le chiffre d'affaires par ville donne Paris (525), Lyon (450), Bordeaux (330), Marseille (250) et Lille (240). Par catégorie : Informatique 945, Mobilier 850.

## Étape par étape

### Étape 1 : le dépôt et le premier commit

J'ai créé le dépôt GitHub, écrit une première version de ce README et fait mon premier commit (« Présentation du projet »).

À retenir : le message d'un commit sert à comprendre, dans six mois, pourquoi un changement a été fait. « Correction : rétablit la suppression des doublons » dit beaucoup plus que « maj ».

### Étape 2 : le pipeline

J'ai ajouté les données brutes (`data/ventes.csv`), la liste des dépendances (`requirements.txt`) et le pipeline (`pipeline.py`).

Les anomalies du fichier, de quatre types :
- des **doublons** (la ligne du clavier à Paris apparaît deux fois) ;
- une **valeur manquante** (la quantité de la lampe à Lille) ;
- une **valeur aberrante** (une quantité de -1 pour la souris à Marseille) ;
- des **villes écrites de plusieurs façons** (« paris », « LILLE », « Lyon » avec un espace devant).

Ensuite, j'ai ajouté la fonction `agreger_par_categorie` pour calculer le chiffre d'affaires par catégorie, écrit dans `output/ca_par_categorie.csv`.

Comparé au tableur : le pipeline refait toujours la même chose, se relit et se versionne, mais il est moins souple pour un cas particulier qu'on voudrait corriger à la main.

### Étape 3 : les tests

J'ai écrit 5 tests dans `tests/test_pipeline.py` avec `pytest`. Ils utilisent un petit jeu de données inventé dont je connais le bon résultat à l'avance. Avec le vrai fichier, un test cassé pourrait venir des données et non du code, et le résultat attendu serait plus dur à calculer à la main.

Les tests vérifient : les doublons et lignes invalides, la normalisation des villes, le calcul du montant, l'agrégation par ville et l'agrégation par catégorie.

J'ai aussi ajouté un `.gitignore` pour ne pas versionner `output/` et les fichiers temporaires de Python, puisque le code les recrée.

### Étape 4 : l'intégration continue

J'ai créé le workflow `.github/workflows/ci.yml`. À chaque push et à chaque pull request, GitHub installe Python, installe les dépendances, lance les tests, exécute le pipeline et publie les résultats dans un artefact `resultats`.

J'ai ensuite cassé le build volontairement : j'ai mis en commentaire la ligne `df = df.drop_duplicates()` (commit « Test : désactive la suppression des doublons »). La CI est passée au rouge à l'étape « Lancer les tests » : 3 tests sur 5 échouaient (doublons, villes, montant). Les étapes suivantes (pipeline, artefact) n'ont pas été lancées, donc aucun résultat faux n'a été publié. J'ai rétabli la ligne et la CI est repassée au vert.

Sans CI, ce code aurait pu produire le rapport envoyé à la direction avec un chiffre d'affaires faux, sans que personne s'en aperçoive. Le serveur repart d'une machine neuve à chaque exécution pour que le résultat ne dépende pas de ce qui est installé par hasard : si ça marche là, ça marche pour tout le monde.

### Étape 5 : Docker

J'ai écrit un `Dockerfile` (image Python 3.12, installation des dépendances puis copie du code) et un `.dockerignore`. J'ai aussi ajouté une étape à la CI qui construit l'image à chaque push.

`requirements.txt` liste les bibliothèques à installer. Le `Dockerfile` va plus loin : il fixe aussi le système et la version de Python. Docker garantit donc que le pipeline tourne à l'identique partout.

### Étape 6 : branche, pull request et linter

J'ai travaillé sur une branche `ajout-linter` pour ne pas toucher directement `main`. J'y ai ajouté `ruff` (un linter qui vérifie le style et les erreurs du code) dans `requirements.txt` et une étape « Vérifier la qualité du code » dans la CI, avant les tests.

J'ai ouvert une pull request (#1), laissé un commentaire de relecture sur la ligne ajoutée dans `ci.yml`, attendu que la CI soit verte, puis fusionné. La CI de `main` est restée verte après la fusion, avec toutes les étapes, y compris le linter et la construction de l'image Docker.

## Structure du dépôt

```
.github/workflows/ci.yml   la chaîne d'intégration continue
data/ventes.csv            les données brutes
tests/test_pipeline.py     les tests automatiques
.dockerignore
.gitignore
Dockerfile                 la recette de l'image Docker
pipeline.py                le pipeline de données
pytest.ini
README.md
requirements.txt           les bibliothèques nécessaires
```
