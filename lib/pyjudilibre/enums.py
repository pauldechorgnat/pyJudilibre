from enum import Enum


class JudilibreMultiValueEnum(Enum):
    def __new__(cls, *values):
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values  # type: ignore
        return obj


def replace_enum(obj):
    if isinstance(obj, JudilibreMultiValueEnum):
        return obj._all_values[-1]  # type: ignore
    else:
        return obj


def replace_enums_in_dictionary(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            obj[k] = replace_enums_in_dictionary(v)
    elif isinstance(obj, list):
        return [replace_enums_in_dictionary(i) for i in obj]
    else:
        return replace_enum(obj)
    return obj


class SourceEnum(JudilibreMultiValueEnum):
    jurinet = "jurinet"
    jurica = "jurica"
    dila = "dila"
    juritj = "juritj"
    juritcom = "juritcom"


class JurisdictionEnum(JudilibreMultiValueEnum):
    """Enum class for the different type of jurisdiction"""

    cour_de_cassation = "Cour de cassation", "cc"
    cours_d_appel = "Cour d'appel", "ca"
    tribunal_judiciaire = "Tribunal judiciaire", "tj"
    tribunal_de_commerce = "Tribunal de commerce", "tcom"


class SolutionCCEnum(JudilibreMultiValueEnum):
    cassation = "Cassation", "cassation"
    rejet = "Rejet", "rejet"
    annulation = "Annulation", "annulation"
    avis = "Avis", "avis"
    decheance = "Déchéance", "decheance"
    designation = "Désignation de juridiction", "designation"
    irrecevabilite = "Irrecevabilité", "irrecevabilite"
    nonlieu = "Non-lieu à statuer", "nonlieu"
    qpc = "QPC renvoi", "qpc"
    qpcother = "QPC autres", "qpcother"
    rabat = "Rabat", "rabat"
    reglement = "Règlement des juges", "reglement"
    renvoi = "Renvoi", "renvoi"
    other = "Autre", "other"


class ChamberCCEnum(JudilibreMultiValueEnum):
    assemblee_pleniere = "Assemblée plénière", "pl"
    chamber_mixte = "Chambre mixte", "mi"
    premiere_chambre_civile = "Première chambre civile", "civ1"
    deuxieme_chambre_civile = "Deuxième chambre civile", "civ2"
    troisieme_chambre_civile = "Troisième chambre civile", "civ3"
    chambre_commerciale = "Chambre commerciale financière et économique", "comm"
    chambre_sociale = "Chambre sociale", "soc"
    chambre_criminelle = "Chambre criminelle", "cr"
    chambres_reunies = "Chambres réunies", "creun"
    ordonnance = "Première présidence (Ordonnance)", "ordo"
    chambres_civiles = "Toutes les chambres civiles", "allciv"
    autres = "Autre", "other"


class FormationCCEnum(JudilibreMultiValueEnum):
    formation_pleniere_chambre = "Formation plénière de chambre", "fp"
    formation_mixte = "Formation mixte", "fm"
    formation_section = "Formation de section", "fs"
    formation_restreinte = "Formation restreinte", "f"
    formation_restreinte_hors_rnsm_na = "Formation restreinte hors RNSM/NA", "frh"
    formation_restreinte_rnsm_na = "Formation restreinte RNSM/NA", "frr"


class PublicationCCEnum(JudilibreMultiValueEnum):
    bulletin = "Publié au Bulletin", "b"
    rapport = "Publié au Rapport", "r"
    lettre_de_chambre = "Publié aux Lettres de chambre", "l"
    communique = "Communiqué", "c"
    non_publie = "Non publié", "n"


class DecisionTypeCCEnum(JudilibreMultiValueEnum):
    arret = "Arrêt", "arret"
    demande_avis = "Demande d'avis", "avis"
    qpc = "Question prioritaire de constitutionnalité (QPC)", "qpc"
    ordonnance = "Ordonnance", "ordonnance"
    saisie = "Saisie", "saisie"
    other = "Autre", "other"


class DecisionTypeCAEnum(JudilibreMultiValueEnum):
    arret = "Arrêt", "arret"
    ordonnance = "Ordonnance", "ordonnance"
    other = "Autre", "other"


class JudilibreStatsAggregationKeysEnum(JudilibreMultiValueEnum):
    jurisdiction = "jurisdiction"
    source = "source"
    location = "location"
    year = "year"
    month = "month"
    chamber = "chamber"
    formation = "formation"
    solution = "solution"
    type = "type"
    nac = "nac"
    themes = "themes"
    publication = "publication"


class JudilibreOrderEnum(JudilibreMultiValueEnum):
    par_score = "Par pertinence", "score"
    par_score_et_publication = "Par pertinence et niveau de publication", "scorepub"
    par_date = "Par date", "date"


class JudilibreSortEnum(JudilibreMultiValueEnum):
    asc = "Croissant", "asc"
    desc = "Décroissant", "desc"


class JudilibreFieldEnum(JudilibreMultiValueEnum):
    themes = "Titre", "themes"
    text = "Texte entier", "text"
    introduction = "Entête", "introduction"
    expose = "Exposé du litige", "expose"
    moyens = "Moyens", "moyens"
    motivations = "Motivation", "motivations"
    dispositif = "Dispositif", "dispositif"
    annexes = "Moyens annexés", "annexes"
    visa = "Textes appliqués", "visa"
    summary = "Sommaire", "summary"


class JudilibreFileTypeEnum(JudilibreMultiValueEnum):
    prep_rapp = "Rapport du conseiller", "prep_rapp"
    prep_raco = "Rapport complémentaire du conseiller", "prep_raco"
    prep_avpg = "Avis du procureur général", "prep_avpg"
    prep_avis = "Avis de l’avocat général", "prep_avis"
    prep_oral = "Avis oral de l’avocat général", "prep_oral"
    comm_comm = "Communiqué", "comm_comm"
    comm_note = "Note explicative", "comm_note"
    comm_nora = "Notice au rapport annuel", "comm_nora"
    comm_lett = "Lettre de chambre", "comm_lett"
    comm_trad = "Arrêt traduit", "comm_trad"


class JudilibreTaxonEnum(JudilibreMultiValueEnum):
    jurisdiction = "jurisdiction"

    # cour de cassation specific taxons
    chamber = "chamber"
    formation = "formation"
    publication = "publication"
    solution = "solution"
    decision_type = "type"

    # other court specific taxons
    location = "location"
    theme = "theme"

    # technical taxons
    text_query_field = "field"
    file_type = "filetype"
    date_type = "date_type"
    sort_order = "sort"
    query_operator = "operator"
    sort_variable = "order"


class JudilibreTransactionActionEnum(JudilibreMultiValueEnum):
    created = "created"
    updated = "updated"
    deleted = "deleted"


class JudilibreDateTypeEnum(JudilibreMultiValueEnum):
    creation = "Date de création", "creation"
    update = "Date de mise à jour", "update"


class JudilibreOperatorEnum(JudilibreMultiValueEnum):
    or_operator = "Ou", "or"
    and_operator = "Et", "and"
    exact_operator = "Expression exacte", "exact"


class LocationCAEnum(JudilibreMultiValueEnum):
    """Enum class for the different cours d'appel"""

    ca_agen = "Cour d'appel d'Agen", "ca_agen"
    ca_aix_provence = "Cour d'appel d'Aix-en-Provence", "ca_aix_provence"
    ca_amiens = "Cour d'appel d'Amiens", "ca_amiens"
    ca_angers = "Cour d'appel d'Angers", "ca_angers"
    ca_basse_terre = "Cour d'appel de Basse-Terre", "ca_basse_terre"
    ca_bastia = "Cour d'appel de Bastia", "ca_bastia"
    ca_besancon = "Cour d'appel de Besançon", "ca_besancon"
    ca_bordeaux = "Cour d'appel de Bordeaux", "ca_bordeaux"
    ca_bourges = "Cour d'appel de Bourges", "ca_bourges"
    ca_caen = "Cour d'appel de Caen", "ca_caen"
    ca_cayenne = "Cour d'appel de Cayenne", "ca_cayenne"
    ca_chambery = "Cour d'appel de Chambéry", "ca_chambery"
    ca_colmar = "Cour d'appel de Colmar", "ca_colmar"
    ca_dijon = "Cour d'appel de Dijon", "ca_dijon"
    ca_douai = "Cour d'appel de Douai", "ca_douai"
    ca_fort_de_france = "Cour d'appel de Fort-de-France", "ca_fort_de_france"
    ca_grenoble = "Cour d'appel de Grenoble", "ca_grenoble"
    ca_limoges = "Cour d'appel de Limoges", "ca_limoges"
    ca_lyon = "Cour d'appel de Lyon", "ca_lyon"
    ca_metz = "Cour d'appel de Metz", "ca_metz"
    ca_montpellier = "Cour d'appel de Montpellier", "ca_montpellier"
    ca_nancy = "Cour d'appel de Nancy", "ca_nancy"
    ca_nimes = "Cour d'appel de Nîmes", "ca_nimes"
    ca_noumea = "Cour d'appel de Nouméa", "ca_noumea"
    ca_orleans = "Cour d'appel d'Orléans", "ca_orleans"
    ca_papeete = "Cour d'appel de Papeete", "ca_papeete"
    ca_paris = "Cour d'appel de Paris", "ca_paris"
    ca_pau = "Cour d'appel de Pau", "ca_pau"
    ca_poitiers = "Cour d'appel de Poitiers", "ca_poitiers"
    ca_reims = "Cour d'appel de Reims", "ca_reims"
    ca_rennes = "Cour d'appel de Rennes", "ca_rennes"
    ca_riom = "Cour d'appel de Riom", "ca_riom"
    ca_rouen = "Cour d'appel de Rouen", "ca_rouen"
    ca_st_denis_reunion = (
        "Cour d'appel de Saint-Denis de la Réunion",
        "ca_st_denis_reunion",
    )
    ca_toulouse = "Cour d'appel de Toulouse", "ca_toulouse"
    ca_versailles = "Cour d'appel de Versailles", "ca_versailles"

    @property
    def city(self) -> str:
        string = self.value
        replacements = [
            ("Cour d'appel de ", ""),
            ("Cour d'appel d'", ""),
            ("Cour d'appel du", "Le"),
            ("Cour d'appel des", "Les"),
        ]

        for pattern, replacement in replacements:
            string = string.replace(pattern, replacement)

        string = string.split("(")[0]
        return string.strip()


class LocationTJEnum(JudilibreMultiValueEnum):
    """Enum class for the different tribunaux judiciaire"""

    tj_agen = "Tribunal judiciaire d'Agen", "tj47001"
    tj_aix_en_provence = "Tribunal judiciaire d'Aix-en-Provence", "tj13001"
    tj_ajaccio = "Tribunal judiciaire d'Ajaccio", "tj2a004"
    tj_albertville = "Tribunal judiciaire d'Albertville", "tj73011"
    tj_albi = "Tribunal judiciaire d'Albi", "tj81004"
    tj_alencon = "Tribunal judiciaire d'Alençon", "tj61001"
    tj_ales = "Tribunal judiciaire d'Alès", "tj30007"
    tj_amiens = "Tribunal judiciaire d'Amiens", "tj80021"
    tj_angers = "Tribunal judiciaire d'Angers", "tj49007"
    tj_angouleme = "Tribunal judiciaire d'Angoulême", "tj16015"
    tj_annecy = "Tribunal judiciaire d'Annecy", "tj74010"
    tj_argentan = "Tribunal judiciaire d'Argentan", "tj61006"
    tj_arras = "Tribunal judiciaire d'Arras", "tj62041"
    tj_auch = "Tribunal judiciaire d'Auch", "tj32013"
    tj_aurillac = "Tribunal judiciaire d'Aurillac", "tj15014"
    tj_auxerre = "Tribunal judiciaire d'Auxerre", "tj89024"
    tj_avesnes_sur_helpe = "Tribunal judiciaire d'Avesnes-sur-Helpe", "tj59036"
    tj_avignon = "Tribunal judiciaire d'Avignon", "tj84007"
    tj_bar_le_duc = "Tribunal judiciaire de Bar-le-Duc", "tj55029"
    tj_basse_terre = "Tribunal judiciaire de Basse-Terre", "tj97105"
    tj_bastia = "Tribunal judiciaire de Bastia", "tj2b033"
    tj_bayonne = "Tribunal judiciaire de Bayonne", "tj64102"
    tj_beauvais = "Tribunal judiciaire de Beauvais", "tj60057"
    tj_belfort = "Tribunal judiciaire de Belfort", "tj90010"
    tj_bergerac = "Tribunal judiciaire de Bergerac", "tj24037"
    tj_besancon = "Tribunal judiciaire de Besançon", "tj25056"
    tj_bethune = "Tribunal judiciaire de Béthune", "tj62119"
    tj_beziers = "Tribunal judiciaire de Béziers", "tj34032"
    tj_blois = "Tribunal judiciaire de Blois", "tj41018"
    tj_bobigny = "Tribunal judiciaire de Bobigny", "tj93008"
    tj_bonneville = "Tribunal judiciaire de Bonneville", "tj74042"
    tj_bordeaux = "Tribunal judiciaire de Bordeaux", "tj33063"
    tj_boulogne_sur_mer = "Tribunal judiciaire de Boulogne-sur-Mer", "tj62160"
    tj_bourg_en_bresse = "Tribunal judiciaire de Bourg-en-Bresse", "tj01053"
    tj_bourges = "Tribunal judiciaire de Bourges", "tj18033"
    tj_bourgoin_jallieu = "Tribunal judiciaire de Bourgoin-Jallieu", "tj38053"
    tj_brest = "Tribunal judiciaire de Brest", "tj29019"
    tj_brive_la_gaillarde = "Tribunal judiciaire de Brive-la-Gaillarde", "tj19031"
    tj_caen = "Tribunal judiciaire de Caen", "tj14118"
    tj_cahors = "Tribunal judiciaire de Cahors", "tj46042"
    tj_cambrai = "Tribunal judiciaire de Cambrai", "tj59122"
    tj_carcassonne = "Tribunal judiciaire de Carcassonne", "tj11069"
    tj_carpentras = "Tribunal judiciaire de Carpentras", "tj84031"
    tj_castres = "Tribunal judiciaire de Castres", "tj81065"
    tj_cayenne = "Tribunal judiciaire de Cayenne", "tj97302"
    tj_chalon_sur_saone = "Tribunal judiciaire de Chalon-sur-Saône", "tj71076"
    tj_chalons_en_champagne = "Tribunal judiciaire de Chalons-en-Champagne", "tj51108"
    tj_chambery = "Tribunal judiciaire de Chambéry", "tj73065"
    tj_charleville_mezieres = "Tribunal judiciaire de Charleville-Mézières", "tj08105"
    tj_chartres = "Tribunal judiciaire de Chartres", "tj28085"
    tj_chateauroux = "Tribunal judiciaire de Châteauroux", "tj36044"
    tj_chaumont = "Tribunal judiciaire de Chaumont", "tj52121"
    tj_cherbourg_en_cotentin = "Tribunal judiciaire de Cherbourg-en-Cotentin", "tj50129"
    tj_clermont_ferrand = "Tribunal judiciaire de Clermont-Ferrand", "tj63113"
    tj_colmar = "Tribunal judiciaire de Colmar", "tj68066"
    tj_compiegne = "Tribunal judiciaire de Compiègne", "tj60159"
    tj_coutances = "Tribunal judiciaire de Coutances", "tj50147"
    tj_creteil = "Tribunal judiciaire de Créteil", "tj94028"
    tj_cusset = "Tribunal judiciaire de Cusset", "tj03095"
    tj_dax = "Tribunal judiciaire de Dax", "tj40088"
    tj_dieppe = "Tribunal judiciaire de Dieppe", "tj76217"
    tj_digne_les_bains = "Tribunal judiciaire de Digne-les-Bains", "tj04070"
    tj_dijon = "Tribunal judiciaire de Dijon", "tj21231"
    tj_dole = "Tribunal judiciaire de Dole (chambre détachée)", "tj39198"
    tj_douai = "Tribunal judiciaire de Douai", "tj59178"
    tj_draguignan = "Tribunal judiciaire de Draguignan", "tj83050"
    tj_dunkerque = "Tribunal judiciaire de Dunkerque", "tj59183"
    tj_epinal = "Tribunal judiciaire d'Épinal", "tj88160"
    tj_evreux = "Tribunal judiciaire d'Évreux", "tj27229"
    tj_evry = "Tribunal judiciaire d'Évry", "tj91228"
    tj_foix = "Tribunal judiciaire de Foix", "tj09122"
    tj_fontainebleau = "Tribunal judiciaire de Fontainebleau", "tj77186"
    tj_fort_de_france = "Tribunal judiciaire de Fort-de-France", "tj97209"
    tj_gap = "Tribunal judiciaire de Gap", "tj05061"
    tj_grasse = "Tribunal judiciaire de Grasse", "tj06069"
    tj_grenoble = "Tribunal judiciaire de Grenoble", "tj38185"
    tj_gueret = "Tribunal judiciaire de Guéret", "tj23096"
    tj_guingamp = "Tribunal judiciaire de Guingamp (chambre détachée)", "tj22070"
    tj_kone = "Tribunal judiciaire de Kone (section détachée)", "tj98811"
    tj_la_roche_sur_yon = "Tribunal judiciaire de La Roche-sur-Yon", "tj85191"
    tj_la_rochelle = "Tribunal judiciaire de La Rochelle", "tj17300"
    tj_laon = "Tribunal judiciaire de Laon", "tj02408"
    tj_laval = "Tribunal judiciaire de Laval", "tj53130"
    tj_havre = "Tribunal judiciaire du Havre", "tj76351"
    tj_mans = "Tribunal judiciaire du Mans", "tj72181"
    tj_puy_en_velay = "Tribunal judiciaire du Puy-en-Velay", "tj43157"
    tj_sables_d_olonne = "Tribunal judiciaire des Sables-d'Olonne", "tj85194"
    tj_libourne = "Tribunal judiciaire de Libourne", "tj33243"
    tj_lille = "Tribunal judiciaire de Lille", "tj59350"
    tj_limoges = "Tribunal judiciaire de Limoges", "tj87085"
    tj_lisieux = "Tribunal judiciaire de Lisieux", "tj14366"
    tj_lons_le_saunier = "Tribunal judiciaire de Lons-le-Saunier", "tj39300"
    tj_lorient = "Tribunal judiciaire de Lorient", "tj56121"
    tj_lyon = "Tribunal judiciaire de Lyon", "tj69123"
    tj_macon = "Tribunal judiciaire de Mâcon", "tj71270"
    tj_mamoudzou = "Tribunal judiciaire de Mamoudzou", "tj97611"
    tj_marmande = "Tribunal judiciaire de Marmande (chambre détachée)", "tj47157"
    tj_marseille = "Tribunal judiciaire de Marseille", "tj13055"
    tj_mata_utu = "Tribunal judiciaire de Mata-Utu", "tj98613"
    tj_meaux = "Tribunal judiciaire de Meaux", "tj77284"
    tj_melun = "Tribunal judiciaire de Melun", "tj77288"
    tj_mende = "Tribunal judiciaire de Mende", "tj48095"
    tj_metz = "Tribunal judiciaire de Metz", "tj57463"
    tj_millau = "Tribunal judiciaire de Millau (chambre détachée)", "tj12145"
    tj_mont_de_marsan = "Tribunal judiciaire de Mont-de-Marsan", "tj40192"
    tj_montargis = "Tribunal judiciaire de Montargis", "tj45208"
    tj_montauban = "Tribunal judiciaire de Montauban", "tj82121"
    tj_montbeliard = "Tribunal judiciaire de Montbéliard", "tj25388"
    tj_montlucon = "Tribunal judiciaire de Montluçon", "tj03185"
    tj_montpellier = "Tribunal judiciaire de Montpellier", "tj34172"
    tj_moulins = "Tribunal judiciaire de Moulins", "tj03190"
    tj_mulhouse = "Tribunal judiciaire de Mulhouse", "tj68224"
    tj_nancy = "Tribunal judiciaire de Nancy", "tj54395"
    tj_nanterre = "Tribunal judiciaire de Nanterre", "tj92050"
    tj_nantes = "Tribunal judiciaire de Nantes", "tj44109"
    tj_narbonne = "Tribunal judiciaire de Narbonne", "tj11262"
    tj_nevers = "Tribunal judiciaire de Nevers", "tj58194"
    tj_nice = "Tribunal judiciaire de Nice", "tj06088"
    tj_nimes = "Tribunal judiciaire de Nîmes", "tj30189"
    tj_niort = "Tribunal judiciaire de Niort", "tj79191"
    tj_noumea = "Tribunal judiciaire de Nouméa", "tj98818"
    tj_orleans = "Tribunal judiciaire d'Orléans", "tj45234"
    tj_papeete = "Tribunal judiciaire de Papeete", "tj98735"
    tj_paris = "Tribunal judiciaire de Paris", "tj75056"
    tj_pau = "Tribunal judiciaire de Pau", "tj64445"
    tj_perigueux = "Tribunal judiciaire de Périgueux", "tj24322"
    tj_perpignan = "Tribunal judiciaire de Perpignan", "tj66136"
    tj_pointe_a_pitre = "Tribunal judiciaire de Pointe-à-Pitre", "tj97120"
    tj_poitiers = "Tribunal judiciaire de Poitiers", "tj86194"
    tj_pontoise = "Tribunal judiciaire de Pontoise", "tj95500"
    tj_privas = "Tribunal judiciaire de Privas", "tj07186"
    tj_quimper = "Tribunal judiciaire de Quimper", "tj29232"
    tj_reims = "Tribunal judiciaire de Reims", "tj51454"
    tj_rennes = "Tribunal judiciaire de Rennes", "tj35238"
    tj_roanne = "Tribunal judiciaire de Roanne", "tj42187"
    tj_rodez = "Tribunal judiciaire de Rodez", "tj12202"
    tj_rouen = "Tribunal judiciaire de Rouen", "tj76540"
    tj_saint_brieuc = "Tribunal judiciaire de Saint-Brieuc", "tj22278"
    tj_saint_denis_de_la_reunion = "Tribunal judiciaire de Saint-Denis de La Réunion", "tj97411"
    tj_saint_etienne = "Tribunal judiciaire de Saint-Etienne", "tj42218"
    tj_saint_gaudens = "Tribunal judiciaire de Saint-Gaudens", "tj31483"
    tj_saint_malo = "Tribunal judiciaire de Saint-Malo", "tj35288"
    tj_saint_nazaire = "Tribunal judiciaire de Saint-Nazaire", "tj44184"
    tj_saint_omer = "Tribunal judiciaire de Saint-Omer", "tj62765"
    tj_saint_pierre_de_la_reunion = "Tribunal judiciaire de Saint-Pierre de La Réunion", "tj97416"
    tj_saint_quentin = "Tribunal judiciaire de Saint-Quentin", "tj02691"
    tj_saint_laurent_du_maroni = "Tribunal judiciaire de Saint-Laurent-Du-Maroni (chambre détachée)", "tj97311"
    tj_saint_martin = "Tribunal judiciaire de Saint-Martin (chambre détachée)", "tj97801"
    tj_sarreguemines = "Tribunal judiciaire de Sarreguemines", "tj57631"
    tj_saumur = "Tribunal judiciaire de Saumur", "tj49328"
    tj_saverne = "Tribunal judiciaire de Saverne", "tj67437"
    tj_senlis = "Tribunal judiciaire de Senlis", "tj60612"
    tj_sens = "Tribunal judiciaire de Sens", "tj89387"
    tj_soissons = "Tribunal judiciaire de Soissons", "tj02722"
    tj_strasbourg = "Tribunal judiciaire de Strasbourg", "tj67482"
    tj_tarascon = "Tribunal judiciaire de Tarascon", "tj13108"
    tj_tarbes = "Tribunal judiciaire de Tarbes", "tj65440"
    tj_thionville = "Tribunal judiciaire de Thionville", "tj57672"
    tj_thonon_les_bains = "Tribunal judiciaire de Thonon-les-Bains", "tj74281"
    tj_toulon = "Tribunal judiciaire de Toulon", "tj83137"
    tj_toulouse = "Tribunal judiciaire de Toulouse", "tj31555"
    tj_tours = "Tribunal judiciaire de Tours", "tj37261"
    tj_troyes = "Tribunal judiciaire de Troyes", "tj10387"
    tj_tulle = "Tribunal judiciaire de Tulle", "tj19272"
    tj_val_de_briey = "Tribunal judiciaire de Val de Briey", "tj54099"
    tj_valence = "Tribunal judiciaire de Valence", "tj26362"
    tj_valenciennes = "Tribunal judiciaire de Valenciennes", "tj59606"
    tj_vannes = "Tribunal judiciaire de Vannes", "tj56260"
    tj_verdun = "Tribunal judiciaire de Verdun", "tj55545"
    tj_versailles = "Tribunal judiciaire de Versailles", "tj78646"
    tj_vesoul = "Tribunal judiciaire de Vesoul", "tj70550"
    tj_vienne = "Tribunal judiciaire de Vienne", "tj38544"
    tj_villefranche_sur_saone = "Tribunal judiciaire de Villefranche-sur-Saône", "tj69264"

    @property
    def city(self) -> str:
        string = self.value
        replacements = [
            ("Tribunal judiciaire de ", ""),
            ("Tribunal judiciaire d'", ""),
            ("Tribunal judiciaire du", "Le"),
            ("Tribunal judiciaire des", "Les"),
        ]

        for pattern, replacement in replacements:
            string = string.replace(pattern, replacement)

        string = string.split("(")[0]
        return string.strip()


class LocationTCOMEnum(JudilibreMultiValueEnum):
    """Enum class for the different tribunaux de commerce"""

    tcom_agen = "Tribunal de commerce d'Agen", "4701"
    tcom_aix_en_provence = "Tribunal de commerce d'Aix-en-Provence", "1301"
    tcom_ajaccio = "Tribunal de commerce d'Ajaccio", "2001"
    tcom_albi = "Tribunal de commerce d'Albi", "8101"
    tcom_alencon = "Tribunal de commerce d'Alençon", "6101"
    tcom_amiens = "Tribunal de commerce d'Amiens", "8002"
    tcom_angers = "Tribunal de commerce d'Angers", "4901"
    tcom_angouleme = "Tribunal de commerce d'Angoulême", "1601"
    tcom_annecy = "Tribunal de commerce d'Annecy", "7401"
    tcom_antibes = "Tribunal de commerce d'Antibes", "0601"
    tcom_arras = "Tribunal de commerce d'Arras", "6201"
    tcom_aubenas = "Tribunal de commerce d'Aubenas", "0702"
    tcom_auch = "Tribunal de commerce d'Auch", "3201"
    tcom_aurillac = "Tribunal de commerce d'Aurillac", "1501"
    tae_d_auxerre = "Tribunal des activités économiques d'Auxerre", "8901"
    tae_d_avignon = "Tribunal des activités économiques d'Avignon", "8401"
    tcom_bar_le_duc = "Tribunal de commerce de Bar-le-Duc", "5501"
    tcom_basse_terre = "Tribunal de commerce de Basse-Terre", "9711"
    tcom_bastia = "Tribunal de commerce de Bastia", "2002"
    tcom_bayonne = "Tribunal de commerce de Bayonne", "6401"
    tcom_beauvais = "Tribunal de commerce de Beauvais", "6001"
    tcom_belfort = "Tribunal de commerce de Belfort", "9001"
    tcom_bergerac = "Tribunal de commerce de Bergerac", "2401"
    tcom_bernay = "Tribunal de commerce de Bernay", "2701"
    tcom_besancon = "Tribunal de commerce de Besançon", "2501"
    tcom_beziers = "Tribunal de commerce de Béziers", "3402"
    tcom_blois = "Tribunal de commerce de Blois", "4101"
    tcom_bobigny = "Tribunal de commerce de Bobigny", "9301"
    tcom_bordeaux = "Tribunal de commerce de Bordeaux", "3302"
    tcom_boulogne_sur_mer = "Tribunal de commerce de Boulogne-sur-Mer", "6202"
    tcom_bourg_en_bresse = "Tribunal de commerce de Bourg-en-Bresse", "0101"
    tcom_bourges = "Tribunal de commerce de Bourges", "1801"
    tcom_brest = "Tribunal de commerce de Brest", "2901"
    tcom_briey = "Tribunal de commerce de Briey", "5401"
    tcom_brive_la_gaillarde = "Tribunal de commerce de Brive-la-Gaillarde", "1901"
    tcom_caen = "Tribunal de commerce de Caen", "1402"
    tcom_cahors = "Tribunal de commerce de Cahors", "4601"
    tcom_cannes = "Tribunal de commerce de Cannes", "0602"
    tcom_carcassonne = "Tribunal de commerce de Carcassonne", "1101"
    tcom_castres = "Tribunal de commerce de Castres", "8102"
    tcom_cayenne = "Tribunal de commerce de Cayenne", "9731"
    tcom_chalon_sur_saone = "Tribunal de commerce de Chalon-sur-Saône", "7102"
    tcom_chalons_en_champagne = "Tribunal de commerce de Chalons-en-Champagne", "5101"
    tcom_chambery = "Tribunal de commerce de Chambéry", "7301"
    tcom_chartres = "Tribunal de commerce de Chartres", "2801"
    tcom_chateauroux = "Tribunal de commerce de Châteauroux", "3601"
    tcom_chaumont = "Tribunal de commerce de Chaumont", "5201"
    tcom_cherbourg = "Tribunal de commerce de Cherbourg", "5001"
    tcom_clermont_ferrand = "Tribunal de commerce de Clermont-Ferrand", "6303"
    tcom_compiegne = "Tribunal de commerce de Compiègne", "6002"
    tcom_coutances = "Tribunal de commerce de Coutances", "5002"
    tcom_creteil = "Tribunal de commerce de Créteil", "9401"
    tcom_cusset = "Tribunal de commerce de Cusset", "0301"
    tcom_dax = "Tribunal de commerce de Dax", "4001"
    tcom_dieppe = "Tribunal de commerce de Dieppe", "7601"
    tcom_dijon = "Tribunal de commerce de Dijon", "2104"
    tcom_douai = "Tribunal de commerce de Douai", "5952"
    tcom_draguignan = "Tribunal de commerce de Draguignan", "8302"
    tcom_dunkerque = "Tribunal de commerce de Dunkerque", "5902"
    tcom_epinal = "Tribunal de commerce d'Épinal", "8801"
    tcom_evreux = "Tribunal de commerce d'Évreux", "2702"
    tcom_evry = "Tribunal de commerce d'Évry", "7801"
    tcom_foix = "Tribunal de commerce de Foix", "0901"
    tcom_fort_de_france = "Tribunal de commerce de Fort-de-France", "9721"
    tcom_frejus = "Tribunal de commerce de Fréjus", "8303"
    tcom_gap = "Tribunal de commerce de Gap", "0501"
    tcom_grasse = "Tribunal de commerce de Grasse", "0603"
    tcom_grenoble = "Tribunal de commerce de Grenoble", "3801"
    tcom_gueret = "Tribunal de commerce de Guéret", "2301"
    tcom_la_roche_sur_yon = "Tribunal de commerce de La Roche-sur-Yon", "8501"
    tcom_la_rochelle = "Tribunal de commerce de La Rochelle", "1704"
    tcom_laval = "Tribunal de commerce de Laval", "5301"
    tae_du_havre = "Tribunal des activités économiques du Havre", "7606"
    tae_du_mans = "Tribunal des activités économiques du Mans", "7202"
    tcom_puy_en_velay = "Tribunal de commerce du Puy-en-Velay", "4302"
    tcom_libourne = "Tribunal de commerce de Libourne", "3303"
    tcom_lille_metropole = "Tribunal de commerce de Lille Métropole", "5910"
    tae_de_limoges = "Tribunal des activités économiques de Limoges", "8701"
    tcom_lisieux = "Tribunal de commerce de Lisieux", "1407"
    tcom_lons_le_saunier = "Tribunal de commerce de Lons-le-Saunier", "3902"
    tcom_lorient = "Tribunal de commerce de Lorient", "5601"
    tae_de_lyon = "Tribunal des activités économiques de Lyon", "6901"
    tcom_macon = "Tribunal de commerce de Mâcon", "7106"
    tcom_mamoudzou = "Tribunal de commerce de Mamoudzou", "9761"
    tcom_manosque = "Tribunal de commerce de Manosque", "0401"
    tae_de_marseille = "Tribunal des activités économiques de Marseille", "1303"
    tcom_meaux = "Tribunal de commerce de Meaux", "7701"
    tcom_melun = "Tribunal de commerce de Melun", "7702"
    tcom_mende = "Tribunal de commerce de Mende", "4801"
    tcom_mont_de_marsan = "Tribunal de commerce de Mont-de-Marsan", "4002"
    tcom_montauban = "Tribunal de commerce de Montauban", "8201"
    tcom_montlucon = "Tribunal de commerce de Montluçon", "0303"
    tcom_montpellier = "Tribunal de commerce de Montpellier", "3405"
    tae_de_nancy = "Tribunal des activités économiques de Nancy", "5402"
    tae_de_nanterre = "Tribunal des activités économiques de Nanterre", "9201"
    tcom_nantes = "Tribunal de commerce de Nantes", "4401"
    tcom_narbonne = "Tribunal de commerce de Narbonne", "1104"
    tcom_nevers = "Tribunal de commerce de Nevers", "5802"
    tcom_nice = "Tribunal de commerce de Nice", "0605"
    tcom_nimes = "Tribunal de commerce de Nîmes", "3003"
    tcom_niort = "Tribunal de commerce de Niort", "7901"
    tcom_orleans = "Tribunal de commerce d'Orléans", "4502"
    tae_de_paris = "Tribunal des activités économiques de Paris", "7501"
    tcom_pau = "Tribunal de commerce de Pau", "6403"
    tcom_perigueux = "Tribunal de commerce de Périgueux", "2402"
    tcom_perpignan = "Tribunal de commerce de Perpignan", "6601"
    tcom_pointe_a_pitre = "Tribunal de commerce de Pointe-à-Pitre", "9712"
    tcom_poitiers = "Tribunal de commerce de Poitiers", "8602"
    tcom_pontoise = "Tribunal de commerce de Pontoise", "7802"
    tcom_quimper = "Tribunal de commerce de Quimper", "2903"
    tcom_reims = "Tribunal de commerce de Reims", "5103"
    tcom_rennes = "Tribunal de commerce de Rennes", "3501"
    tcom_roanne = "Tribunal de commerce de Roanne", "4201"
    tcom_rodez = "Tribunal de commerce de Rodez", "1203"
    tcom_romans = "Tribunal de commerce de Romans", "2602"
    tcom_rouen = "Tribunal de commerce de Rouen", "7608"
    tae_de_saint_brieuc = "Tribunal des activités économiques de Saint-Brieuc", "2202"
    tcom_saint_denis_de_la_reunion = "Tribunal de commerce de Saint-Denis de La Réunion", "9741"
    tcom_saint_etienne = "Tribunal de commerce de Saint-Etienne", "4202"
    tcom_saint_malo = "Tribunal de commerce de Saint-Malo", "3502"
    tcom_saint_nazaire = "Tribunal de commerce de Saint-Nazaire", "4402"
    tcom_saint_pierre_de_la_reunion = "Tribunal de commerce de Saint-Pierre de La Réunion", "9742"
    tcom_saint_quentin = "Tribunal de commerce de Saint-Quentin", "0202"
    tcom_saintes = "Tribunal de commerce de Saintes", "1708"
    tcom_salon_de_provence = "Tribunal de commerce de Salon-de-Provence", "1304"
    tcom_sedan = "Tribunal de commerce de Sedan", "0802"
    tcom_sens = "Tribunal de commerce de Sens", "8903"
    tcom_soissons = "Tribunal de commerce de Soissons", "0203"
    tcom_tarascon = "Tribunal de commerce de Tarascon", "1305"
    tcom_tarbes = "Tribunal de commerce de Tarbes", "6502"
    tcom_thonon_les_bains = "Tribunal de commerce de Thonon-les-Bains", "7402"
    tcom_toulon = "Tribunal de commerce de Toulon", "8305"
    tcom_toulouse = "Tribunal de commerce de Toulouse", "3102"
    tcom_tours = "Tribunal de commerce de Tours", "3701"
    tcom_troyes = "Tribunal de commerce de Troyes", "1001"
    tcom_valenciennes = "Tribunal de commerce de Valenciennes", "5906"
    tcom_vannes = "Tribunal de commerce de Vannes", "5602"
    tcom_vesoul___gray = "Tribunal de commerce de Vesoul - Gray", "7001"
    tae_de_versailles = "Tribunal des activités économiques de Versailles", "7803"
    tcom_vienne = "Tribunal de commerce de Vienne", "3802"
    tcom_villefranche_sur_saone___tarare = "Tribunal de commerce de Villefranche-sur-Saône - Tarare", "6903"

    @property
    def city(self) -> str:
        string = self.value
        replacements = [
            ("Tribunal de commerce de ", ""),
            ("Tribunal de commerce d'", ""),
            ("Tribunal de commerce du", "Le"),
            ("Tribunal de commerce des", "Les"),
            ("Tribunal des activités économiques de ", ""),
            ("Tribunal des activités économiques d'", ""),
            ("Tribunal des activités économiques du", "Le"),
            ("Tribunal des activités économiques des", "Les"),
        ]

        for pattern, replacement in replacements:
            string = string.replace(pattern, replacement)

        string = string.split("(")[0]
        return string.strip()
