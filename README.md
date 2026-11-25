# Pipeline de données Bureau&Co

Auteur : Amine Hammoutene

Ce projet nettoie le fichier des ventes et calcule le chiffre d'affaires par ville et par catégorie. Le tout est versionné avec Git, testé, vérifié par une intégration continue (GitHub Actions) et emballé dans Docker.

## Lancer le projet

```bash
pip install -r requirements.txt   # installer les dépendances
python pipeline.py                # lancer le pipeline
pytest -v                         # lancer les tests
ruff check .                      # vérifier la qualité du code
```

Avec Docker :

```bash
docker build -t pipeline-data .
docker run --rm -v "$(pwd)/output:/app/output" pipeline-data
```

Les résultats arrivent dans `output/` : ventes nettoyées, chiffre d'affaires par ville et par catégorie. Sur le fichier fourni : 12 lignes lues, 9 gardées, Paris en tête avec 525.

## Ce que j'ai fait

1. **Git** : création du dépôt et premiers commits avec des messages clairs.
2. **Pipeline** : `pipeline.py` lit `data/ventes.csv`, supprime les doublons, les lignes sans quantité ou à quantité négative, uniformise les villes (« paris », « LILLE », « Lyon » avec un espace), calcule les montants et écrit les résultats. J'ai ajouté l'agrégation par catégorie.
3. **Tests** : 5 tests `pytest` sur un petit jeu de données inventé, dont je connais le résultat à l'avance.
4. **Intégration continue** : à chaque push, GitHub lance les tests, exécute le pipeline et publie les résultats. J'ai cassé le build exprès (suppression des doublons désactivée) : la CI est passée au rouge, 3 tests sur 5 échouaient, rien n'a été publié. Après correction, elle est repassée au vert.
5. **Docker** : un `Dockerfile` pour exécuter le pipeline à l'identique partout, construit aussi par la CI.
6. **Pull request** : sur une branche, j'ai ajouté le linter `ruff` à la CI, ouvert une PR, relu mon code puis fusionné.

## Ce que j'en retiens

- Un **message de commit clair** permet de comprendre un changement des mois plus tard.
- Les **tests** détectent une erreur tout de suite, sans attendre qu'un rapport faux parte à la direction.
- La **CI** les lance à chaque modification, sur une machine neuve, donc personne ne peut l'oublier.
- **Docker** garantit que le pipeline tourne pareil sur toutes les machines.
