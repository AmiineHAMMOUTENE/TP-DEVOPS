import pandas as pd

from pipeline import agreger_par_categorie, agreger_par_ville, transformer


def donnees_exemple():
    return pd.DataFrame({
        "quantite": [2, 2, None, -1, 3],
        "prix_unitaire": [10.0, 10.0, 5.0, 5.0, 20.0],
        "ville": ["paris", "paris", "Lyon", "Lyon", " lyon"],
    })


def test_supprime_les_doublons_et_lignes_invalides():
    resultat = transformer(donnees_exemple())
    assert len(resultat) == 2


def test_normalise_les_villes():
    resultat = transformer(donnees_exemple())
    assert sorted(resultat["ville"]) == ["Lyon", "Paris"]


def test_calcule_le_montant():
    resultat = transformer(donnees_exemple())
    assert resultat["montant"].sum() == 80.0


def test_agregation_par_ville():
    resultat = agreger_par_ville(transformer(donnees_exemple()))
    assert resultat.iloc[0]["ville"] == "Lyon"
    assert resultat.iloc[0]["montant"] == 60.0


def test_agregation_par_categorie():
    df = pd.DataFrame({
        "categorie": ["Informatique", "Mobilier", "Informatique"],
        "ville": ["Paris", "Lyon", "Lyon"],
        "quantite": [2, 1, 3],
        "prix_unitaire": [10.0, 50.0, 20.0],
    })
    resultat = agreger_par_categorie(transformer(df))
    # Informatique : 2*10 + 3*20 = 80 ; Mobilier : 1*50 = 50
    assert list(resultat["categorie"]) == ["Informatique", "Mobilier"]
    assert list(resultat["montant"]) == [80.0, 50.0]
