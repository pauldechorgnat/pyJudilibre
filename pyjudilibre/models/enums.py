from aenum import Enum, EnumMeta, MultiValueEnum

from ..exceptions import JudilibreValueError


class JudilibreEnumMeta(EnumMeta):
    def __call__(cls, value, *args, **kw):
        try:
            new_instance = super().__call__(value, *args, **kw)
            return new_instance
        except ValueError as exc:
            raise JudilibreValueError(f"Value '{value}' is not valid for {cls.__name__}") from exc


class SourceEnum(Enum, metaclass=JudilibreEnumMeta):
    """Data source of a decision.

    Can only take one of 3 values:
    - 'jurinet': Cour de cassation system.
    - 'jurica': Cours d'appel system.
    - 'juritj': Tribunaux judiciaires system.
    - 'dila': Legacy system.
    """

    jurinet = "jurinet"
    jurica = "jurica"
    dila = "dila"
    juritj = "juritj"


class JurisdictionEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    """Jurisdiction level of a decision.

    Can only take one of 2 values:
    - 'cc' for Cour de cassation.
    - 'ca' for Cour d'appel.
    """

    cour_de_cassation = "Cour de cassation", "cc", "cour_de_cassation"
    cours_d_appel = "Cour d'appel", "ca", "cours_d_appel"
    tribunal_judiciaire = "Tribunal judiciaire", "tj", "tribunal_judiciaire"


class SolutionEnum(Enum, metaclass=JudilibreEnumMeta):
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


class ChamberEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    pl = "Assemblée plénière", "pl"
    mi = "Chambre mixte", "mi"
    civ1 = "Première chambre civile", "civ1"
    civ2 = "Deuxième chambre civile", "civ2"
    civ3 = "Troisième chambre civile", "civ3"
    comm = "Chambre commerciale financière et économique", "comm"
    soc = "Chambre sociale", "soc"
    cr = "Chambre criminelle", "cr"
    creun = "Chambres réunies", "creun"
    ordo = "Première présidence (Ordonnance)", "ordo"
    allciv = "Toutes les chambres civiles", "allciv"
    other = "Autre", "other"


class FormationEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    fp = "Formation plénière de chambre", "fp"
    fm = "Formation mixte", "fm"
    fs = "Formation de section", "fs"
    f = "Formation restreinte", "f"
    frh = "Formation restreinte hors RNSM/NA", "frh"
    frr = "Formation restreinte RNSM/NA", "frr"


class PublicationEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    b = "Publié au Bulletin", "b"
    r = "Publié au Rapport", "r"
    l = "Publié aux Lettres de chambre", "l"  # noqa: E741
    c = "Communiqué", "c"
    n = "Non publié", "n"


class LocationCAEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
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


class LocationTJEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    tj_47001 = "Tribunal judiciaire d'Agen", "tj47001"
    tj_13001 = "Tribunal judiciaire d'Aix-en-Provence", "tj13001"
    tj_2a004 = "Tribunal judiciaire d'Ajaccio", "tj2a004"
    tj_73011 = "Tribunal judiciaire d'Albertville", "tj73011"
    tj_81004 = "Tribunal judiciaire d'Albi", "tj81004"
    tj_61001 = "Tribunal judiciaire d'Alençon", "tj61001"
    tj_30007 = "Tribunal judiciaire d'Alès", "tj30007"
    tj_80021 = "Tribunal judiciaire d'Amiens", "tj80021"
    tj_49007 = "Tribunal judiciaire d'Angers", "tj49007"
    tj_16015 = "Tribunal judiciaire d'Angoulême", "tj16015"
    tj_74010 = "Tribunal judiciaire d'Annecy", "tj74010"
    tj_61006 = "Tribunal judiciaire d'Argentan", "tj61006"
    tj_62041 = "Tribunal judiciaire d'Arras", "tj62041"
    tj_32013 = "Tribunal judiciaire d'Auch", "tj32013"
    tj_15014 = "Tribunal judiciaire d'Aurillac", "tj15014"
    tj_89024 = "Tribunal judiciaire d'Auxerre", "tj89024"
    tj_59036 = "Tribunal judiciaire d'Avesnes-sur-Helpe", "tj59036"
    tj_84007 = "Tribunal judiciaire d'Avignon", "tj84007"
    tj_55029 = "Tribunal judiciaire de Bar-le-Duc", "tj55029"
    tj_97105 = "Tribunal judiciaire de Basse-Terre", "tj97105"
    tj_2b033 = "Tribunal judiciaire de Bastia", "tj2b033"
    tj_64102 = "Tribunal judiciaire de Bayonne", "tj64102"
    tj_60057 = "Tribunal judiciaire de Beauvais", "tj60057"
    tj_90010 = "Tribunal judiciaire de Belfort", "tj90010"
    tj_24037 = "Tribunal judiciaire de Bergerac", "tj24037"
    tj_25056 = "Tribunal judiciaire de Besançon", "tj25056"
    tj_62119 = "Tribunal judiciaire de Béthune", "tj62119"
    tj_34032 = "Tribunal judiciaire de Béziers", "tj34032"
    tj_41018 = "Tribunal judiciaire de Blois", "tj41018"
    tj_93008 = "Tribunal judiciaire de Bobigny", "tj93008"
    tj_74042 = "Tribunal judiciaire de Bonneville", "tj74042"
    tj_33063 = "Tribunal judiciaire de Bordeaux", "tj33063"
    tj_62160 = "Tribunal judiciaire de Boulogne-sur-Mer", "tj62160"
    tj_01053 = "Tribunal judiciaire de Bourg-en-Bresse", "tj1053", "tj01053"
    tj_18033 = "Tribunal judiciaire de Bourges", "tj18033"
    tj_38053 = "Tribunal judiciaire de Bourgoin-Jallieu", "tj38053"
    tj_29019 = "Tribunal judiciaire de Brest", "tj29019"
    tj_54099 = "Tribunal judiciaire de Briey", "tj54099"
    tj_19031 = "Tribunal judiciaire de Brive-la-Gaillarde", "tj19031"
    tj_14118 = "Tribunal judiciaire de Caen", "tj14118"
    tj_46042 = "Tribunal judiciaire de Cahors", "tj46042"
    tj_59122 = "Tribunal judiciaire de Cambrai", "tj59122"
    tj_11069 = "Tribunal judiciaire de Carcassonne", "tj11069"
    tj_84031 = "Tribunal judiciaire de Carpentras", "tj84031"
    tj_81065 = "Tribunal judiciaire de Castres", "tj81065"
    tj_97302 = "Tribunal judiciaire de Cayenne", "tj97302"
    tj_71076 = "Tribunal judiciaire de Chalon-sur-Saône", "tj71076"
    tj_51108 = "Tribunal judiciaire de Chalons-en-Champagne", "tj51108"
    tj_73065 = "Tribunal judiciaire de Chambéry", "tj73065"
    tj_08105 = "Tribunal judiciaire de Charleville-Mézières", "tj8105", "tj08105"
    tj_28085 = "Tribunal judiciaire de Chartres", "tj28085"
    tj_36044 = "Tribunal judiciaire de Châteauroux", "tj36044"
    tj_52121 = "Tribunal judiciaire de Chaumont", "tj52121"
    tj_50129 = "Tribunal judiciaire de Cherbourg", "tj50129"
    tj_63113 = "Tribunal judiciaire de Clermont-Ferrand", "tj63113"
    tj_68066 = "Tribunal judiciaire de Colmar", "tj68066"
    tj_60159 = "Tribunal judiciaire de Compiègne", "tj60159"
    tj_50147 = "Tribunal judiciaire de Coutances", "tj50147"
    tj_94028 = "Tribunal judiciaire de Créteil", "tj94028"
    tj_03095 = "Tribunal judiciaire de Cusset", "tj3095", "tj03095"
    tj_40088 = "Tribunal judiciaire de Dax", "tj40088"
    tj_76217 = "Tribunal judiciaire de Dieppe", "tj76217"
    tj_04070 = "Tribunal judiciaire de Digne-les-Bains", "tj4070", "tj04070"
    tj_21231 = "Tribunal judiciaire de Dijon", "tj21231"
    tj_39198 = "Tribunal judiciaire de Dole (chambre détachée)", "tj39198"
    tj_59178 = "Tribunal judiciaire de Douai", "tj59178"
    tj_83050 = "Tribunal judiciaire de Draguignan", "tj83050"
    tj_59183 = "Tribunal judiciaire de Dunkerque", "tj59183"
    tj_88160 = "Tribunal judiciaire d'Epinal", "tj88160"
    tj_27229 = "Tribunal judiciaire d'Evreux", "tj27229"
    tj_91228 = "Tribunal judiciaire d'Evry", "tj91228"
    tj_09122 = "Tribunal judiciaire de Foix", "tj9122", "tj09122"
    tj_77186 = "Tribunal judiciaire de Fontainebleau", "tj77186"
    tj_97209 = "Tribunal judiciaire de Fort-de-France", "tj97209"
    tj_05061 = "Tribunal judiciaire de Gap", "tj5061", "tj05061"
    tj_06069 = "Tribunal judiciaire de Grasse", "tj6069", "tj06069"
    tj_38185 = "Tribunal judiciaire de Grenoble", "tj38185"
    tj_23096 = "Tribunal judiciaire de Guéret", "tj23096"
    tj_22070 = "Tribunal judiciaire de Guingamp (chambre détachée)", "tj22070"
    tj_98811 = "Tribunal judiciaire de Kone", "tj98811"
    tj_85191 = "Tribunal judiciaire de La Roche-sur-Yon", "tj85191"
    tj_17300 = "Tribunal judiciaire de La Rochelle", "tj17300"
    tj_02408 = "Tribunal judiciaire de Laon", "tj2408", "tj02408"
    tj_53130 = "Tribunal judiciaire de Laval", "tj53130"
    tj_76351 = "Tribunal judiciaire du Havre", "tj76351"
    tj_72181 = "Tribunal judiciaire du Mans", "tj72181"
    tj_43157 = "Tribunal judiciaire du Puy-en-Velay", "tj43157"
    tj_85194 = "Tribunal judiciaire des Sables-d'Olonne", "tj85194"
    tj_33243 = "Tribunal judiciaire de Libourne", "tj33243"
    tj_59350 = "Tribunal judiciaire de Lille", "tj59350"
    tj_87085 = "Tribunal judiciaire de Limoges", "tj87085"
    tj_14366 = "Tribunal judiciaire de Lisieux", "tj14366"
    tj_39300 = "Tribunal judiciaire de Lons-le-Saunier", "tj39300"
    tj_56121 = "Tribunal judiciaire de Lorient", "tj56121"
    tj_69123 = "Tribunal judiciaire de Lyon", "tj69123"
    tj_71270 = "Tribunal judiciaire de Mâcon", "tj71270"
    tj_97611 = "Tribunal judiciaire de Mamoudzou", "tj97611"
    tj_47157 = "Tribunal judiciaire de Marmande (chambre détachée)", "tj47157"
    tj_13055 = "Tribunal judiciaire de Marseille", "tj13055"
    tj_98613 = "Tribunal judiciaire de Mata-Utu", "tj98613"
    tj_77284 = "Tribunal judiciaire de Meaux", "tj77284"
    tj_77288 = "Tribunal judiciaire de Melun", "tj77288"
    tj_48095 = "Tribunal judiciaire de Mende", "tj48095"
    tj_57463 = "Tribunal judiciaire de Metz", "tj57463"
    tj_12145 = "Tribunal judiciaire de Millau (chambre détachée)", "tj12145"
    tj_40192 = "Tribunal judiciaire de Mont-de-Marsan", "tj40192"
    tj_45208 = "Tribunal judiciaire de Montargis", "tj45208"
    tj_82121 = "Tribunal judiciaire de Montauban", "tj82121"
    tj_25388 = "Tribunal judiciaire de Montbéliard", "tj25388"
    tj_03185 = "Tribunal judiciaire de Montluçon", "tj3185", "tj03185"
    tj_34172 = "Tribunal judiciaire de Montpellier", "tj34172"
    tj_03190 = "Tribunal judiciaire de Moulins", "tj3190", "tj03190"
    tj_68224 = "Tribunal judiciaire de Mulhouse", "tj68224"
    tj_54395 = "Tribunal judiciaire de Nancy", "tj54395"
    tj_92050 = "Tribunal judiciaire de Nanterre", "tj92050"
    tj_44109 = "Tribunal judiciaire de Nantes", "tj44109"
    tj_11262 = "Tribunal judiciaire de Narbonne", "tj11262"
    tj_58194 = "Tribunal judiciaire de Nevers", "tj58194"
    tj_06088 = "Tribunal judiciaire de Nice", "tj6088", "tj06088"
    tj_30189 = "Tribunal judiciaire de Nîmes", "tj30189"
    tj_79191 = "Tribunal judiciaire de Niort", "tj79191"
    tj_98818 = "Tribunal judiciaire de Nouméa", "tj98818"
    tj_45234 = "Tribunal judiciaire d'Orléans", "tj45234"
    tj_98735 = "Tribunal judiciaire de Papeete", "tj98735"
    tj_75056 = "Tribunal judiciaire de Paris", "tj75056"
    tj_64445 = "Tribunal judiciaire de Pau", "tj64445"
    tj_24322 = "Tribunal judiciaire de Périgueux", "tj24322"
    tj_66136 = "Tribunal judiciaire de Perpignan", "tj66136"
    tj_97120 = "Tribunal judiciaire de Pointe-à-Pitre", "tj97120"
    tj_86194 = "Tribunal judiciaire de Poitiers", "tj86194"
    tj_95500 = "Tribunal judiciaire de Pontoise", "tj95500"
    tj_07186 = "Tribunal judiciaire de Privas", "tj7186", "tj07186"
    tj_29232 = "Tribunal judiciaire de Quimper", "tj29232"
    tj_51454 = "Tribunal judiciaire de Reims", "tj51454"
    tj_35238 = "Tribunal judiciaire de Rennes", "tj35238"
    tj_42187 = "Tribunal judiciaire de Roanne", "tj42187"
    tj_12202 = "Tribunal judiciaire de Rodez", "tj12202"
    tj_76540 = "Tribunal judiciaire de Rouen", "tj76540"
    tj_22278 = "Tribunal judiciaire de Saint-Brieuc", "tj22278"
    tj_97411 = "Tribunal judiciaire de Saint-Denis de La Réunion", "tj97411"
    tj_42218 = "Tribunal judiciaire de Saint-Etienne", "tj42218"
    tj_31483 = "Tribunal judiciaire de Saint-Gaudens", "tj31483"
    tj_35288 = "Tribunal judiciaire de Saint-Malo", "tj35288"
    tj_44184 = "Tribunal judiciaire de Saint-Nazaire", "tj44184"
    tj_62765 = "Tribunal judiciaire de Saint-Omer", "tj62765"
    tj_97416 = "Tribunal judiciaire de Saint-Pierre de La Réunion", "tj97416"
    tj_02691 = "Tribunal judiciaire de Saint-Quentin", "tj2691", "tj02691"
    tj_97311 = (
        "Tribunal judiciaire de Saint-Laurent-Du-Maroni (chambre détachée)",
        "tj97311",
    )
    tj_97801 = "Tribunal judiciaire de Saint-Martin (chambre détachée)", "tj97801"
    tj_49328 = "Tribunal judiciaire de Saumur", "tj49328"
    tj_67437 = "Tribunal judiciaire de Saverne", "tj67437"
    tj_60612 = "Tribunal judiciaire de Senlis", "tj60612"
    tj_89387 = "Tribunal judiciaire de Sens", "tj89387"
    tj_02722 = "Tribunal judiciaire de Soissons", "tj2722", "tj02722"
    tj_67482 = "Tribunal judiciaire de Strasbourg", "tj67482"
    tj_13108 = "Tribunal judiciaire de Tarascon", "tj13108"
    tj_65440 = "Tribunal judiciaire de Tarbes", "tj65440"
    tj_57672 = "Tribunal judiciaire de Thionville", "tj57672"
    tj_74281 = "Tribunal judiciaire de Thonon-les-Bains", "tj74281"
    tj_83137 = "Tribunal judiciaire de Toulon", "tj83137"
    tj_31555 = "Tribunal judiciaire de Toulouse", "tj31555"
    tj_37261 = "Tribunal judiciaire de Tours", "tj37261"
    tj_10387 = "Tribunal judiciaire de Troyes", "tj10387"
    tj_26362 = "Tribunal judiciaire de Valence", "tj26362"
    tj_59606 = "Tribunal judiciaire de Valenciennes", "tj59606"
    tj_56260 = "Tribunal judiciaire de Vannes", "tj56260"
    tj_55545 = "Tribunal judiciaire de Verdun", "tj55545"
    tj_78646 = "Tribunal judiciaire de Versailles", "tj78646"
    tj_70550 = "Tribunal judiciaire de Vesoul", "tj70550"
    tj_38544 = "Tribunal judiciaire de Vienne", "tj38544"
    tj_69264 = "Tribunal judiciaire de Villefranche-sur-Saône", "tj69264"


class SearchOrderFieldEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    score = "Par pertinence", "score"
    scorepub = "Par pertinence et niveau de publication", "scorepub"
    date = "Par date", "date"


class DecisionTypeEnum(MultiValueEnum, metaclass=JudilibreEnumMeta):
    arret = "Arrêt", "arret"
    avis = "Demande d'avis", "avis"
    qpc = "Question prioritaire de constitutionnalité (QPC)", "qpc"
    ordonnance = "Ordonnance", "ordonnance"
    saisie = "Saisie", "saisie"
    other = "Autre", "other"
