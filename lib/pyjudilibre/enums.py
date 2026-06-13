from enum import Enum


class JudilibreMultiValueEnum(Enum):
    """General class for Judilibre Enums"""

    def __new__(cls, *values):
        """Instantiation function"""
        obj = object.__new__(cls)
        # first value is canonical value
        obj._value_ = values[0]
        for other_value in values[1:]:
            cls._value2member_map_[other_value] = obj
        obj._all_values = values  # type: ignore
        return obj

    @classmethod
    def replace_enum(cls, obj):
        if isinstance(obj, cls):
            return obj._all_values[-1]  # type: ignore
        else:
            return obj


class SourceEnum(JudilibreMultiValueEnum):
    """Enumeration for the `SOURCE` attribute"""

    jurinet = "jurinet"
    jurica = "jurica"
    dila = "dila"
    juritj = "juritj"
    juritcom = "juritcom"
    portalis = "portalis"


class JurisdictionEnum(JudilibreMultiValueEnum):
    """Enumeration for the `JURISDICTION` attribute"""

    cour_de_cassation = "Cour de cassation", "cc"
    cours_d_appel = "Cour d'appel", "ca"
    tribunaux_judiciaires = "Tribunal judiciaire", "tj"
    tribunaux_de_commerce = "Tribunal de commerce", "tcom"
    conseils_de_prud_hommes = "Conseil de Prud'hommes", "cph"


class SolutionCCEnum(JudilibreMultiValueEnum):
    """Enumeration for the `SOLUTION` attribute for the Cour de cassation"""

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
    """Enumeration for the `CHAMBER` attribute for the Cour de cassation"""

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
    """Enumeration for the `FORMATION` attribute for the Cour de cassation"""

    formation_pleniere_chambre = "Formation plénière de chambre", "fp"
    formation_mixte = "Formation mixte", "fm"
    formation_section = "Formation de section", "fs"
    formation_restreinte = "Formation restreinte", "f"
    formation_restreinte_hors_rnsm_na = "Formation restreinte hors RNSM/NA", "frh"
    formation_restreinte_rnsm_na = "Formation restreinte RNSM/NA", "frr"


class PublicationCCEnum(JudilibreMultiValueEnum):
    """Enumeration for the `PUBLICATION` attribute for the Cour de cassation"""

    bulletin = "Publié au Bulletin", "b"
    rapport = "Publié au Rapport", "r"
    lettre_de_chambre = "Publié aux Lettres de chambre", "l"
    communique = "Communiqué", "c"
    non_publie = "Non publié", "n"


class DecisionTypeCCEnum(JudilibreMultiValueEnum):
    """Enumeration for the `TYPE` attribute for the Cour de cassation"""

    arret = "Arrêt", "arret"
    demande_avis = "Demande d'avis", "avis"
    qpc = "Question prioritaire de constitutionnalité (QPC)", "qpc"
    ordonnance = "Ordonnance", "ordonnance"
    saisie = "Saisie", "saisie"
    other = "Autre", "other"


class DecisionTypeCAEnum(JudilibreMultiValueEnum):
    """Enumeration for the `TYPE` attribute for the Cours d'appel"""

    arret = "Arrêt", "arret"
    ordonnance = "Ordonnance", "ordonnance"
    other = "Autre", "other"


class JudilibreStatsAggregationKeysEnum(JudilibreMultiValueEnum):
    """Enumeration for the `KEY` attribute to aggregate data"""

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
    # themes = "themes"
    publication = "publication"
    filetype = "filetype"


class JudilibreOrderEnum(JudilibreMultiValueEnum):
    """Enumeration for the `ORDER` attribute to return data"""

    par_score = "Par pertinence", "score"
    par_score_et_publication = "Par pertinence et niveau de publication", "scorepub"
    par_date = "Par date", "date"


class JudilibreSortEnum(JudilibreMultiValueEnum):
    """Enumeration for the `SORT` attribute to return data"""

    ascending = "Croissant", "asc"
    descending = "Décroissant", "desc"


class JudilibreFieldEnum(JudilibreMultiValueEnum):
    """Enumeration for the `FIELD` attribute to return data"""

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
    """Enumeration for the `FILETYPE` attribute to search data"""

    rapport_du_conseiller = "Rapport du conseiller", "1", "prep_rapp"
    rapport_complementaire_du_conseiller = "Rapport complémentaire du conseiller", "9", "prep_raco"
    avis_du_procureur_general = "Avis du procureur général", "10", "prep_avpg"
    avis_de_l_avocat_general = "Avis de l’avocat général", "2", "prep_avis"
    avis_oral_de_l_avocat_general = "Avis oral de l’avocat général", "3", "prep_oral"
    prep_avco = "Avis complémentaire de l’avocat général", "11", "prep_avco"
    communique = "Communiqué", "4", "comm_comm"
    note_explicative = "Note explicative", "5", "comm_note"
    notice_au_rapport_annuel = "Notice au rapport annuel", "8", "comm_nora"
    lettre_de_chambre = "Lettre de chambre", "6", "comm_lett"
    arret_traduit = "Arrêt traduit", "7", "comm_trad"
    datt_deci = "Décision avec graphiques", "13", "datt_deci"
    datt_grph = "Graphique", "12", "datt_grph"


class JudilibreTaxonEnum(JudilibreMultiValueEnum):
    """Enumeration for the `TAXON` attribute"""

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
    """Enumeration for the `ACTION` attribute of the transactions"""

    created = "created"
    updated = "updated"
    deleted = "deleted"


class JudilibreDateTypeEnum(JudilibreMultiValueEnum):
    """Enumeration for the `DATETYPE` attribute to look for data"""

    creation = "Date de création", "creation"
    update = "Date de mise à jour", "update"


class JudilibreOperatorEnum(JudilibreMultiValueEnum):
    """Enumeration for the `OPERATOR` attribute to look for data"""

    or_operator = "Ou", "or"
    and_operator = "Et", "and"
    exact_operator = "Expression exacte", "exact"


class LocationCAEnum(JudilibreMultiValueEnum):
    """Enumeration for the `LOCATION` attribute for Cours d'appel"""

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
    ca_pau = "Cour d'appelconseils_de_prud_hommes de Pau", "ca_pau"
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
        """Name of the city in which the court is located"""
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


class ZoneTypeEnum(JudilibreMultiValueEnum):
    introduction = "introduction"
    expose_du_litige = "exposé du litige"
    moyen = "moyen"
    motivation = "motivation"
    dispositif = "dispositif"
    moyen_annexe = "moyen annexe"


class LocationTJEnum(JudilibreMultiValueEnum):
    """Enumeration for the `LOCATION` attribute for tribunaux judiciaires"""

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
    tj_meaux = "Tribunal judiciaire de Meaux", "tj77291", "tj77284"
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
    tj_saintes = "Tribunal judiciaire de Saintes", "tj17415"
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
        """Name of the city in which the court is located"""
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
    """Enumeration for the `LOCATION` attribute for tribunaux de commerce"""

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
        """Name of the city in which the court is located"""
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


class LocationCPHEnum(JudilibreMultiValueEnum):
    """Enumeration for the `LOCATION` attribute for Conseils de prud'hommes"""

    # cph_abbeville = "Conseil de prud'hommes d'Abbeville", "cph_abbeville", "1234"
    # cph_agen = "Conseil de prud'hommes d'Agen", "cph_agen", "1234"
    # cph_aix_provence = "Conseil de prud'hommes d'Aix-en-Provence", "cph_aix_provence", "1234"
    # cph_aix_les_bains = "Conseil de prud'hommes d'Aix-les-Bains", "cph_aix_les_bains", "1234"
    # cph_ajaccio = "Conseil de prud'hommes d'Ajaccio", "cph_ajaccio", "1234"
    # cph_albertville = "Conseil de prud'hommes d'Albertville", "cph_albertville", "1234"
    # cph_albi = "Conseil de prud'hommes d'Albi", "cph_albi", "1234"
    # cph_alencon = "Conseil de prud'hommes d'Alençon", "cph_alencon", "1234"
    # cph_ales = "Conseil de prud'hommes d'Alès", "cph_ales", "1234"
    # cph_amiens = "Conseil de prud'hommes d'Amiens", "cph_amiens", "1234"
    # cph_angers = "Conseil de prud'hommes d'Angers", "cph_angers", "1234"
    # cph_angouleme = "Conseil de prud'hommes d'Angoulême", "cph_angouleme", "1234"
    # cph_annecy = "Conseil de prud'hommes d'Annecy", "cph_annecy", "1234"
    cph_annemasse = "Conseil de prud'hommes d'Annemasse", "cph_annemasse", "101152"
    # cph_annonay = "Conseil de prud'hommes d'Annonay", "cph_annonay", "1234"
    # cph_argentan = "Conseil de prud'hommes d'Argentan", "cph_argentan", "1234"
    # cph_argenteuil = "Conseil de prud'hommes d'Argenteuil", "cph_argenteuil", "1234"
    cph_arles = "Conseil de prud'hommes d'Arles", "cph_arles", "100971"
    # cph_arras = "Conseil de prud'hommes d'Arras", "cph_arras", "1234"
    # cph_aubenas = "Conseil de prud'hommes d'Aubenas", "cph_aubenas", "1234"
    # cph_auch = "Conseil de prud'hommes d'Auch", "cph_auch", "1234"
    # cph_aurillac = "Conseil de prud'hommes d'Aurillac", "cph_aurillac", "1234"
    # cph_auxerre = "Conseil de prud'hommes d'Auxerre", "cph_auxerre", "1234"
    # cph_avesnes_sur_helpe = "Conseil de prud'hommes d'Avesnes-sur-Helpe", "cph_avesnes_sur_helpe", "1234"
    cph_avignon = "Conseil de prud'hommes d'Avignon", "cph_avignon", "101184"
    # cph_avranches = "Conseil de prud'hommes d'Avranches", "cph_avranches", "1234"
    # cph_bar_le_duc = "Conseil de prud'hommes de Bar-le-Duc", "cph_bar_le_duc", "1234"
    # cph_basse_terre = "Conseil de prud'hommes de Basse-Terre", "cph_basse_terre", "1234"
    # cph_bastia = "Conseil de prud'hommes de Bastia", "cph_bastia", "1234"
    # cph_bayonne = "Conseil de prud'hommes de Bayonne", "cph_bayonne", "1234"
    # cph_beauvais = "Conseil de prud'hommes de Beauvais", "cph_beauvais", "1234"
    # cph_belfort = "Conseil de prud'hommes de Belfort", "cph_belfort", "1234"
    # cph_belley = "Conseil de prud'hommes de Belley", "cph_belley", "1234"
    cph_bergerac = "Conseil de prud'hommes de Bergerac", "cph_bergerac", "100998"
    cph_bernay = "Conseil de prud'hommes de Bernay", "cph_bernay", "101005"
    # cph_besancon = "Conseil de prud'hommes de Besançon", "cph_besancon", "1234"
    cph_blois = "Conseil de prud'hommes de Blois", "cph_blois", "101046"
    # cph_bobigny = "Conseil de prud'hommes de Bobigny", "cph_bobigny", "1234"
    # cph_bonneville = "Conseil de prud'hommes de Bonneville", "cph_bonneville", "1234"
    # cph_bordeaux = "Conseil de prud'hommes de Bordeaux", "cph_bordeaux", "1234"
    # cph_boulogne_billancourt = "Conseil de prud'hommes de Boulogne-Billancourt", "cph_boulogne_billancourt", "1234"
    # cph_boulogne_sur_mer = "Conseil de prud'hommes de Boulogne-sur-Mer", "cph_boulogne_sur_mer", "1234"
    # cph_bourg_en_bresse = "Conseil de prud'hommes de Bourg-en-Bresse", "cph_bourg_en_bresse", "1234"
    cph_bourges = "Conseil de prud'hommes de Bourges", "cph_bourges", "100986"
    # cph_bourgoin_jallieu = "Conseil de prud'hommes de Bourgoin-Jallieu", "cph_bourgoin_jallieu", "1234"
    # cph_brest = "Conseil de prud'hommes de Brest", "cph_brest", "1234"
    # cph_brive_la_gaillarde = "Conseil de prud'hommes de Brive-la-Gaillarde", "cph_brive_la_gaillarde", "1234"
    # cph_bethune = "Conseil de prud'hommes de Béthune", "cph_bethune", "1234"
    # cph_beziers = "Conseil de prud'hommes de Béziers", "cph_beziers", "1234"
    # cph_caen = "Conseil de prud'hommes de Caen", "cph_caen", "1234"
    # cph_cahors = "Conseil de prud'hommes de Cahors", "cph_cahors", "1234"
    # cph_calais = "Conseil de prud'hommes de Calais", "cph_calais", "1234"
    # cph_cambrai = "Conseil de prud'hommes de Cambrai", "cph_cambrai", "1234"
    cph_cannes = "Conseil de prud'hommes de Cannes", "cph_cannes", "100952"
    # cph_carcassonne = "Conseil de prud'hommes de Carcassonne", "cph_carcassonne", "1234"
    # cph_castres = "Conseil de prud'hommes de Castres", "cph_castres", "1234"
    # cph_cayenne = "Conseil de prud'hommes de Cayenne", "cph_cayenne", "1234"
    # cph_cergy_pontoise = "Conseil de prud'hommes de Cergy-Pontoise", "cph_cergy_pontoise", "1234"
    # cph_chalon_sur_saone = "Conseil de prud'hommes de Chalon-sur-Saône", "cph_chalon_sur_saone", "1234"
    # cph_chambery = "Conseil de prud'hommes de Chambéry", "cph_chambery", "1234"
    cph_charleville_mezieres = "Conseil de prud'hommes de Charleville-Mézières", "cph_charleville_mezieres", "100958"
    # cph_chartres = "Conseil de prud'hommes de Chartres", "cph_chartres", "1234"
    # cph_chaumont = "Conseil de prud'hommes de Chaumont", "cph_chaumont", "1234"
    # cph_cherbourg_en_cotentin = "Conseil de prud'hommes de Cherbourg-en-Cotentin", "cph_cherbourg_en_cotentin", "1234"
    # cph_chalons_en_champagne = "Conseil de prud'hommes de Châlons-en-Champagne", "cph_chalons_en_champagne", "1234"
    # cph_chateaudun = "Conseil de prud'hommes de Châteaudun", "cph_chateaudun", "1234"
    # cph_chateauroux = "Conseil de prud'hommes de Châteauroux", "cph_chateauroux", "1234"
    cph_clermont_ferrand = "Conseil de prud'hommes de Clermont-Ferrand", "cph_clermont_ferrand", "101119"
    cph_colmar = "Conseil de prud'hommes de Colmar", "cph_colmar", "101134"
    # cph_compiegne = "Conseil de prud'hommes de Compiègne", "cph_compiegne", "1234"
    # cph_coutances = "Conseil de prud'hommes de Coutances", "cph_coutances", "1234"
    cph_creil = "Conseil de prud'hommes de Creil", "cph_creil", "101108"
    # cph_creteil = "Conseil de prud'hommes de Créteil", "cph_creteil", "1234"
    cph_dax = "Conseil de prud'hommes de Dax", "cph_dax", "101044"
    cph_dieppe = "Conseil de prud'hommes de Dieppe", "cph_dieppe", "101157"
    # cph_digne_les_bains = "Conseil de prud'hommes de Digne-les-Bains", "cph_digne_les_bains", "1234"
    # cph_dijon = "Conseil de prud'hommes de Dijon", "cph_dijon", "1234"
    # cph_dinan = "Conseil de prud'hommes de Dinan", "cph_dinan", "1234"
    # cph_dole = "Conseil de prud'hommes de Dole", "cph_dole", "1234"
    # cph_douai = "Conseil de prud'hommes de Douai", "cph_douai", "1234"
    cph_draguignan = "Conseil de prud'hommes de Draguignan", "cph_draguignan", "101181"
    # cph_dreux = "Conseil de prud'hommes de Dreux", "cph_dreux", "1234"
    # cph_dunkerque = "Conseil de prud'hommes de Dunkerque", "cph_dunkerque", "1234"
    # cph_epernay = "Conseil de prud'hommes d'Épernay", "cph_epernay", "1234"
    # cph_epinal = "Conseil de prud'hommes d'Épinal", "cph_epinal", "1234"
    cph_evreux = "Conseil de prud'hommes d'Évreux", "cph_evreux", "101006"
    # cph_foix = "Conseil de prud'hommes de Foix", "cph_foix", "1234"
    # cph_fontainebleau = "Conseil de prud'hommes de Fontainebleau", "cph_fontainebleau", "1234"
    # cph_forbach = "Conseil de prud'hommes de Forbach", "cph_forbach", "1234"
    # cph_fort_de_france = "Conseil de prud'hommes de Fort-de-France", "cph_fort_de_france", "1234"
    # cph_frejus = "Conseil de prud'hommes de Fréjus", "cph_frejus", "1234"
    # cph_gap = "Conseil de prud'hommes de Gap", "cph_gap", "1234"
    # cph_grasse = "Conseil de prud'hommes de Grasse", "cph_grasse", "1234"
    # cph_grenoble = "Conseil de prud'hommes de Grenoble", "cph_grenoble", "1234"
    # cph_guingamp = "Conseil de prud'hommes de Guingamp", "cph_guingamp", "1234"
    # cph_gueret = "Conseil de prud'hommes de Guéret", "cph_gueret", "1234"
    # cph_haguenau = "Conseil de prud'hommes d'Haguenau", "cph_haguenau", "1234"
    # cph_le_havre = "Conseil de prud'hommes du Havre", "cph_le_havre", "1234"
    # cph_hazebrouck = "Conseil de prud'hommes d'Hazebrouck", "cph_hazebrouck", "1234"
    # cph_laon = "Conseil de prud'hommes de Laon", "cph_laon", "1234"
    # cph_laval = "Conseil de prud'hommes de Laval", "cph_laval", "1234"
    # cph_lens = "Conseil de prud'hommes de Lens", "cph_lens", "1234"
    cph_libourne = "Conseil de prud'hommes de Libourne", "cph_libourne", "101022"
    # cph_lille = "Conseil de prud'hommes de Lille", "cph_lille", "1234"
    # cph_limoges = "Conseil de prud'hommes de Limoges", "cph_limoges", "1234"
    # cph_lisieux = "Conseil de prud'hommes de Lisieux", "cph_lisieux", "1234"
    # cph_longjumeau = "Conseil de prud'hommes de Longjumeau", "cph_longjumeau", "1234"
    # cph_longwy = "Conseil de prud'hommes de Longwy", "cph_longwy", "1234"
    # cph_lons_le_saunier = "Conseil de prud'hommes de Lons-le-Saunier", "cph_lons_le_saunier", "1234"
    # cph_lorient = "Conseil de prud'hommes de Lorient", "cph_lorient", "1234"
    # cph_louviers = "Conseil de prud'hommes de Louviers", "cph_louviers", "1234"
    # cph_lure = "Conseil de prud'hommes de Lure", "cph_lure", "1234"
    # cph_lyon = "Conseil de prud'hommes de Lyon", "cph_lyon", "1234"
    # cph_lys_lez_lannoy = "Conseil de prud'hommes de Lys-Lez-Lannoy", "cph_lys_lez_lannoy", "1234"
    # cph_mamoudzou = "Conseil de prud'hommes de Mamoudzou", "cph_mamoudzou", "1234"
    # cph_le_mans = "Conseil de prud'hommes du Mans", "cph_le_mans", "1234"
    cph_mantes_la_jolie = "Conseil de prud'hommes de Mantes-la-Jolie", "cph_mantes_la_jolie", "101165"
    # cph_marmande = "Conseil de prud'hommes de Marmande", "cph_marmande", "1234"
    # cph_marseille = "Conseil de prud'hommes de Marseille", "cph_marseille", "1234"
    # cph_martigues = "Conseil de prud'hommes de Martigues", "cph_martigues", "1234"
    # cph_meaux = "Conseil de prud'hommes de Meaux", "cph_meaux", "1234"
    # cph_melun = "Conseil de prud'hommes de Melun", "cph_melun", "1234"
    # cph_mende = "Conseil de prud'hommes de Mende", "cph_mende", "1234"
    # cph_metz = "Conseil de prud'hommes de Metz", "cph_metz", "1234"
    # cph_millau = "Conseil de prud'hommes de Millau", "cph_millau", "1234"
    # cph_montargis = "Conseil de prud'hommes de Montargis", "cph_montargis", "1234"
    # cph_montauban = "Conseil de prud'hommes de Montauban", "cph_montauban", "1234"
    # cph_montbrison = "Conseil de prud'hommes de Montbrison", "cph_montbrison", "1234"
    cph_montbeliard = "Conseil de prud'hommes de Montbéliard", "cph_montbeliard", "101001"
    cph_mont_de_marsan = "Conseil de prud'hommes de Mont-de-Marsan", "cph_mont_de_marsan", "101045"
    # cph_montlucon = "Conseil de prud'hommes de Montluçon", "cph_montlucon", "1234"
    # cph_montmorency = "Conseil de prud'hommes de Montmorency", "cph_montmorency", "1234"
    # cph_montpellier = "Conseil de prud'hommes de Montpellier", "cph_montpellier", "1234"
    # cph_montelimar = "Conseil de prud'hommes de Montélimar", "cph_montelimar", "1234"
    # cph_morlaix = "Conseil de prud'hommes de Morlaix", "cph_morlaix", "1234"
    cph_moulins = "Conseil de prud'hommes de Moulins", "cph_moulins", "100946"
    # cph_mulhouse = "Conseil de prud'hommes de Mulhouse", "cph_mulhouse", "1234"
    # cph_macon = "Conseil de prud'hommes de Mâcon", "cph_macon", "1234"
    cph_nancy = "Conseil de prud'hommes de Nancy", "cph_nancy", "101079"
    # cph_nanterre = "Conseil de prud'hommes de Nanterre", "cph_nanterre", "1234"
    # cph_nantes = "Conseil de prud'hommes de Nantes", "cph_nantes", "1234"
    # cph_narbonne = "Conseil de prud'hommes de Narbonne", "cph_narbonne", "1234"
    cph_nevers = "Conseil de prud'hommes de Nevers", "cph_nevers", "101089"
    # cph_nice = "Conseil de prud'hommes de Nice", "cph_nice", "1234"
    # cph_niort = "Conseil de prud'hommes de Niort", "cph_niort", "1234"
    # cph_nimes = "Conseil de prud'hommes de Nîmes", "cph_nimes", "1234"
    cph_orange = "Conseil de prud'hommes d'Orange", "cph_orange", "101186"
    # cph_orleans = "Conseil de prud'hommes d'Orléans", "cph_orleans", "1234"
    # cph_oyonnax = "Conseil de prud'hommes d'Oyonnax", "cph_oyonnax", "1234"
    # cph_paris = "Conseil de prud'hommes de Paris", "cph_paris", "1234"
    # cph_pau = "Conseil de prud'hommes de Pau", "cph_pau", "1234"
    # cph_perpignan = "Conseil de prud'hommes de Perpignan", "cph_perpignan", "1234"
    # cph_pointe_a_pitre = "Conseil de prud'hommes de Pointe-à-Pitre", "cph_pointe_a_pitre", "1234"
    # cph_poissy = "Conseil de prud'hommes de Poissy", "cph_poissy", "1234"
    # cph_poitiers = "Conseil de prud'hommes de Poitiers", "cph_poitiers", "1234"
    # cph_le_puy_en_velay = "Conseil de prud'hommes du Puy-en-Velay", "cph_le_puy_en_velay", "1234"
    # cph_perigueux = "Conseil de prud'hommes de Périgueux", "cph_perigueux", "1234"
    cph_peronne = "Conseil de prud'hommes de Péronne", "cph_peronne", "101175"
    # cph_quimper = "Conseil de prud'hommes de Quimper", "cph_quimper", "1234"
    cph_rambouillet = "Conseil de prud'hommes de Rambouillet", "cph_rambouillet", "101167"
    cph_reims = "Conseil de prud'hommes de Reims", "cph_reims", "101072"
    # cph_rennes = "Conseil de prud'hommes de Rennes", "cph_rennes", "1234"
    # cph_riom = "Conseil de prud'hommes de Riom", "cph_riom", "1234"
    # cph_roanne = "Conseil de prud'hommes de Roanne", "cph_roanne", "1234"
    # cph_rochefort = "Conseil de prud'hommes de Rochefort", "cph_rochefort", "1234"
    # cph_la_rochelle = "Conseil de prud'hommes de La Rochelle", "cph_la_rochelle", "1234"
    # cph_la_roche_sur_yon = "Conseil de prud'hommes de La Roche-sur-Yon", "cph_la_roche_sur_yon", "1234"
    # cph_rodez = "Conseil de prud'hommes de Rodez", "cph_rodez", "1234"
    cph_roubaix = "Conseil de prud'hommes de Roubaix", "cph_roubaix", "101103"
    # cph_rouen = "Conseil de prud'hommes de Rouen", "cph_rouen", "1234"
    # cph_les_sables_dolonne = "Conseil de prud'hommes des Sables d'Olonne", "cph_les_sables_dolonne", "1234"
    # cph_saint_brieuc = "Conseil de prud'hommes de Saint-Brieuc", "cph_saint_brieuc", "1234"
    cph_saint_denis = "Conseil de prud'hommes de Saint-Denis", "cph_saint_denis", "101215"
    # cph_saint_die_des_vosges = "Conseil de prud'hommes de Saint-Dié-des-Vosges", "cph_saint_die_des_vosges", "1234"
    cph_saintes = "Conseil de prud'hommes de Saintes", "cph_saintes", "100985"
    # cph_saint_etienne = "Conseil de prud'hommes de Saint-Étienne", "cph_saint_etienne", "1234"
    # cph_saint_gaudens = "Conseil de prud'hommes de Saint-Gaudens", "cph_saint_gaudens", "1234"
    # cph_saint_germain_en_laye = "Conseil de prud'hommes de Saint-Germain-en-Laye", "cph_saint_germain_en_laye", "1234"
    # cph_saint_malo = "Conseil de prud'hommes de Saint-Malo", "cph_saint_malo", "1234"
    # cph_saint_nazaire = "Conseil de prud'hommes de Saint-Nazaire", "cph_saint_nazaire", "1234"
    # cph_saint_omer = "Conseil de prud'hommes de Saint-Omer", "cph_saint_omer", "1234"
    cph_saint_pierre = "Conseil de prud'hommes de Saint-Pierre", "cph_saint_pierre", "101216"
    # cph_saint_quentin = "Conseil de prud'hommes de Saint-Quentin", "cph_saint_quentin", "1234"
    # cph_saumur = "Conseil de prud'hommes de Saumur", "cph_saumur", "1234"
    # cph_saverne = "Conseil de prud'hommes de Saverne", "cph_saverne", "1234"
    # cph_schiltigheim = "Conseil de prud'hommes de Schiltigheim", "cph_schiltigheim", "1234"
    # cph_sens = "Conseil de prud'hommes de Sens", "cph_sens", "1234"
    # cph_soissons = "Conseil de prud'hommes de Soissons", "cph_soissons", "1234"
    # cph_st_pierre_et_miquelon = "Conseil de prud'hommes de St-Pierre-et-Miquelon", "cph_st_pierre_et_miquelon", "1234"
    # cph_strasbourg = "Conseil de prud'hommes de Strasbourg", "cph_strasbourg", "1234"
    # cph_sete = "Conseil de prud'hommes de Sète", "cph_sete", "1234"
    cph_tarbes = "Conseil de prud'hommes de Tarbes", "cph_tarbes", "101125"
    # cph_thionville = "Conseil de prud'hommes de Thionville", "cph_thionville", "1234"
    # cph_thouars = "Conseil de prud'hommes de Thouars", "cph_thouars", "1234"
    # cph_toulon = "Conseil de prud'hommes de Toulon", "cph_toulon", "1234"
    cph_toulouse = "Conseil de prud'hommes de Toulouse", "cph_toulouse", "101019"
    # cph_tourcoing = "Conseil de prud'hommes de Tourcoing", "cph_tourcoing", "1234"
    # cph_tours = "Conseil de prud'hommes de Tours", "cph_tours", "1234"
    cph_troyes = "Conseil de prud'hommes de Troyes", "cph_troyes", "100964"
    # cph_tulle = "Conseil de prud'hommes de Tulle", "cph_tulle", "1234"
    # cph_valence = "Conseil de prud'hommes de Valence", "cph_valence", "1234"
    cph_valenciennes = "Conseil de prud'hommes de Valenciennes", "cph_valenciennes", "101105"
    # cph_vannes = "Conseil de prud'hommes de Vannes", "cph_vannes", "1234"
    # cph_verdun = "Conseil de prud'hommes de Verdun", "cph_verdun", "1234"
    # cph_versailles = "Conseil de prud'hommes de Versailles", "cph_versailles", "1234"
    # cph_vesoul = "Conseil de prud'hommes de Vesoul", "cph_vesoul", "1234"
    # cph_vichy = "Conseil de prud'hommes de Vichy", "cph_vichy", "1234"
    # cph_vienne = "Conseil de prud'hommes de Vienne", "cph_vienne", "1234"
    # cph_villefranche_sur_saone = "Conseil de prud'hommes de Villefranche-sur-Saône", "cph_villefranche_sur_saone", "1234"
    # cph_villeneuve_saint_georges = "Conseil de prud'hommes de Villeneuve-Saint-Georges", "cph_villeneuve_saint_georges", "1234"
    # cph_evry_courcouronnes = "Conseil de prud'hommes d'Évry-Courcouronnes", "cph_evry_courcouronnes", "1234"
    # dt_mata_utu = "Tribunal du travail de Mata-Utu", "dt_mata_utu", "1234"
    # dt_noumea = "Tribunal du travail de Nouméa", "dt_noumea", "1234"
    # dt_nuku_hiva = "Tribunal du travail de Nuku-Hiva", "dt_nuku_hiva", "1234"
    # dt_papeete = "Tribunal du travail de Papeete", "dt_papeete", "1234"
    # dt_raiatea = "Tribunal du travail de Raïatéa", "dt_raiatea", "1234"

    @property
    def city(self) -> str:
        """Name of the city in which the court is located"""
        string = self.value[0] if isinstance(self.value, tuple) else self.value
        replacements = [
            ("Conseil de prud'hommes de ", ""),
            ("Conseil de prud'hommes d'", ""),
            ("Conseil de prud'hommes du ", "Le "),
            ("Conseil de prud'hommes des ", "Les "),
            ("Tribunal du travail de ", ""),
            ("Tribunal du travail d'", ""),
        ]

        for pattern, replacement in replacements:
            string = string.replace(pattern, replacement)

        string = string.split("(")[0]
        return string.strip()
