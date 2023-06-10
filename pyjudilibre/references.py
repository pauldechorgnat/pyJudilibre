import json

JURISDICTIONS = {"ca": "Cour d'appel", "cc": "Cour de cassation"}

CA_DECISION_TYPES = {"arret": "Arrêt", "ordonnance": "Ordonnance", "other": "Autre"}

CC_DECISION_TYPES = {
    "arret": "Arrêt",
    "avis": "Demande d'avis",
    "ordonnance": "Ordonnance",
    "other": "Autre",
    "qpc": "Question prioritaire de constitutionnalité (QPC)",
    "saisie": "Saisie",
}
with open("ca_themes.json", "r", encoding="utf-8") as ca_theme_file:
    CA_THEMES = json.load(ca_theme_file)


with open("cc_themes.json", "r", encoding="utf-8") as cc_theme_file:
    CC_THEMES = json.load(cc_theme_file)


CC_CHAMBERS = {
    "allciv": "Toutes les chambres civiles",
    "civ1": "Première chambre civile",
    "civ2": "Deuxième chambre civile",
    "civ3": "Troisième chambre civile",
    "comm": "Chambre commerciale financière et économique",
    "cr": "Chambre criminelle",
    "creun": "Chambres réunies",
    "mi": "Chambre mixte",
    "ordo": "Première présidence (Ordonnance)",
    "other": "Autre",
    "pl": "Assemblée plénière",
    "soc": "Chambre sociale",
}


CC_PUBLICATIONS = {
    "b": "Publié au Bulletin",
    "c": "Communiqué",
    "l": "Publié aux Lettres de chambre",
    "n": "Non publié",
    "r": "Publié au Rapport",
}

CC_SOLUTIONS = {
    "annulation": "Annulation",
    "avis": "Avis",
    "cassation": "Cassation",
    "decheance": "Déchéance",
    "designation": "Désignation de juridiction",
    "irrecevabilite": "Irrecevabilité",
    "nonlieu": "Non-lieu à statuer",
    "other": "Autre",
    "qpc": "QPC renvoi",
    "qpcother": "QPC autres",
    "rabat": "Rabat",
    "reglement": "Règlement des juges",
    "rejet": "Rejet",
    "renvoi": "Renvoi",
}


CC_FORMATIONS = {
    "f": "Formation restreinte",
    "fm": "Formation mixte",
    "fp": "Formation plénière de chambre",
    "frh": "Formation restreinte hors RNSM/NA",
    "frr": "Formation restreinte RNSM/NA",
    "fs": "Formation de section",
}

CA_LOCATIONS = {
    "ca_agen": "Cour d'appel d'Agen",
    "ca_aix_provence": "Cour d'appel d'Aix-en-Provence",
    "ca_amiens": "Cour d'appel d'Amiens",
    "ca_angers": "Cour d'appel d'Angers",
    "ca_basse_terre": "Cour d'appel de Basse-Terre",
    "ca_bastia": "Cour d'appel de Bastia",
    "ca_besancon": "Cour d'appel de Besançon",
    "ca_bordeaux": "Cour d'appel de Bordeaux",
    "ca_bourges": "Cour d'appel de Bourges",
    "ca_caen": "Cour d'appel de Caen",
    "ca_cayenne": "Cour d'appel de Cayenne",
    "ca_chambery": "Cour d'appel de Chambéry",
    "ca_colmar": "Cour d'appel de Colmar",
    "ca_dijon": "Cour d'appel de Dijon",
    "ca_douai": "Cour d'appel de Douai",
    "ca_fort_de_france": "Cour d'appel de Fort-de-France",
    "ca_grenoble": "Cour d'appel de Grenoble",
    "ca_limoges": "Cour d'appel de Limoges",
    "ca_lyon": "Cour d'appel de Lyon",
    "ca_metz": "Cour d'appel de Metz",
    "ca_montpellier": "Cour d'appel de Montpellier",
    "ca_nancy": "Cour d'appel de Nancy",
    "ca_nimes": "Cour d'appel de Nîmes",
    "ca_noumea": "Cour d'appel de Nouméa",
    "ca_orleans": "Cour d'appel d'Orléans",
    "ca_papeete": "Cour d'appel de Papeete",
    "ca_paris": "Cour d'appel de Paris",
    "ca_pau": "Cour d'appel de Pau",
    "ca_poitiers": "Cour d'appel de Poitiers",
    "ca_reims": "Cour d'appel de Reims",
    "ca_rennes": "Cour d'appel de Rennes",
    "ca_riom": "Cour d'appel de Riom",
    "ca_rouen": "Cour d'appel de Rouen",
    "ca_st_denis_reunion": "Cour d'appel de Saint-Denis de la Réunion",
    "ca_toulouse": "Cour d'appel de Toulouse",
    "ca_versailles": "Cour d'appel de Versailles",
}
