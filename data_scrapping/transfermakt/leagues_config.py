LEAGUES = {
    'laliga': [
        "Barcelona", "Real Madrid", "Villarreal", "Atlético Madrid",
        "Real Betis", "Espanyol", "Getafe", "Athletic Club", "Sevilla",
        "Real Sociedad", "Celta Vigo", "Rayo Vallecano", "Elche",
        "Alavés", "Valencia", "Mallorca", "Osasuna", "Girona",
        "Levante", "Oviedo"
    ],
    'premier_league': [
        "Arsenal", "Chelsea", "Manchester City", "Crystal Palace",
        "Brighton", "Sunderland", "Bournemouth", "Tottenham",
        "Aston Villa", "Manchester United", "Liverpool", "Brentford",
        "Everton", "Newcastle", "Fulham", "Leeds", "Nottingham Forest",
        "West Ham", "Burnley", "Wolves"
    ],
    'ligue1': [
        "PSG", "Marseille", "RC Lens", "LOSC", "Strasbourg", "Rennes",
        "Lyon", "AS Monaco", "Nice", "Toulouse", "Angers SCO",
        "Paris FC", "Le Havre", "Brest", "Nantes", "Lorient", "Metz",
        "Auxerre"
    ],
    'serie_a': [
        "Roma", "Milan", "Napoli", "Inter", "Bologna", "Juventus",
        "Lazio", "Como", "Sassuolo", "Udinese", "Cremonese", "Torino",
        "Atalanta", "Cagliari", "Parma", "Lecce", "Pisa", "Genoa",
        "Fiorentina", "Verona"
    ],
    'bundesliga': [
        "Bayern", "RB Leipzig", "Leverkusen", "Dortmund",
        "VfB Stuttgart", "Eintracht Frankfurt", "Hoffenheim",
        "Union Berlin", "Werder", "Köln", "SC Freiburg",
        "Mönchengladbach", "Augsburg", "Hamburger SV", "Wolfsburg",
        "FC St. Pauli", "Mainz", "Heidenheim"
    ],
    'belgian': [
        "Club Brugge KV", "KRC Genk", "RSC Anderlecht",
        "Union Saint-Gilloise", "KAA Gent", "Royal Antwerp FC",
        "KVC Westerlo", "Standard Liège", "KV Mechelen",
        "Cercle Brugge", "Royal Charleroi SC", "Sint-Truidense VV",
        "Oud-Heverlee Leuven", "Zulte Waregem", "FCV Dender EH",
        "RAAL La Louvière"
    ],
    'championship': [
        "Coventry", "Middlesbrough", "Millwall", "Preston",
        "Ipswich Town", "QPR", "Stoke City", "Southampton",
        "Bristol City", "Birmingham", "Watford", "Hull City",
        "Wrexham", "Leicester City", "Derby County", "West Brom",
        "Sheffield United", "Swansea", "Charlton", "Blackburn Rovers",
        "Oxford Utd", "Portsmouth", "Norwich City", "Sheffield Wednesday"
    ],
    'liga_portugal': [
        "Sporting CP", "FC Porto", "SL Benfica", "SC Braga",
        "FC Famalicão", "Rio Ave FC", "CD Santa Clara",
        "GD Estoril Praia", "FC Alverca", "Gil Vicente FC",
        "Casa Pia AC", "Moreirense FC", "Vitória Guimarães SC",
        "FC Arouca", "CD Tondela", "CD Nacional", "Avs Futebol",
        "CF Estrela Amadora"
    ],
    'brazil_serie_a': [
        "Sociedade Esportiva Palmeiras", "CR Flamengo",
        "Cruzeiro Esporte Clube", "Botafogo de Futebol e Regatas",
        "Clube de Regatas Vasco da Gama",
        "Sport Club Corinthians Paulista", "Esporte Clube Bahia",
        "Fluminense Football Club", "Red Bull Bragantino",
        "Clube Atlético Mineiro", "Santos FC",
        "Grêmio Foot-Ball Porto Alegrense", "São Paulo Futebol Clube",
        "Sport Club Internacional", "Fortaleza Esporte Clube",
        "Sport Club do Recife", "Ceará Sporting Club",
        "Esporte Clube Vitória", "Mirassol Futebol Clube",
        "Esporte Clube Juventude"
    ],
    'mls': [
        "Inter Miami CF", "Los Angeles FC", "FC Cincinnati",
        "Atlanta United FC", "Los Angeles Galaxy", "Portland Timbers",
        "Seattle Sounders FC", "Vancouver Whitecaps FC",
        "Columbus Crew", "New York City FC", "Chicago Fire FC",
        "Charlotte FC", "San Diego FC", "Austin FC",
        "Minnesota United FC", "Colorado Rapids", "Orlando City SC",
        "Nashville SC", "Real Salt Lake City", "Philadelphia Union",
        "New York Red Bulls", "New England Revolution",
        "St. Louis CITY SC", "Houston Dynamo FC",
        "San Jose Earthquakes", "Sporting Kansas City", "FC Dallas",
        "CF Montréal", "Toronto FC", "D.C. United"
    ],
    'eredivisie': [
        "PSV Eindhoven", "Feyenoord Rotterdam", "Ajax Amsterdam",
        "AZ Alkmaar", "FC Utrecht", "Twente Enschede FC",
        "SC Heerenveen", "NEC Nijmegen", "FC Groningen",
        "Go Ahead Eagles", "Sparta Rotterdam", "PEC Zwolle",
        "Fortuna Sittard", "Excelsior Rotterdam", "NAC Breda",
        "Heracles Almelo", "FC Volendam", "SC Telstar"
    ],
    'argentina': [
        "CA River Plate", "CA Boca Juniors", "Racing Club",
        "CA Independiente", "CA Vélez Sarsfield",
        "Club Estudiantes de La Plata", "CA Talleres",
        "CA Rosario Central", "AA Argentinos Juniors",
        "CA San Lorenzo de Almagro", "CA Lanús",
        "Club Atlético Belgrano", "CD Godoy Cruz Antonio Tomba",
        "CA Huracán", "Club Atlético Tigre", "Defensa y Justicia",
        "Club Atlético Platense", "Instituto ACC", "Club Atlético Unión",
        "CS Independiente Rivadavia", "CA Barracas Central",
        "CA Newell's Old Boys", "CA Central Córdoba", "CA Banfield",
        "Club de Gimnasia y Esgrima La Plata", "Club Atlético Tucumán",
        "CA Sarmiento", "CA Aldosivi", "CA San Martín",
        "Club Deportivo Riestra"
    ],
    'poland': [
        "Jagiellonia Bialystok", "Lech Poznan", "Raków Częstochowa",
        "Legia Warszawa", "Widzew Lodz", "Cracovia",
        "Pogon Szczecin", "Lechia Gdansk", "Górnik Zabrze",
        "Zaglebie Lubin", "Radomiak Radom", "Korona Kielce",
        "Motor Lublin", "Wisla Plock", "GKS Katowice",
        "Piast Gliwice", "Arka Gdynia", "Bruk-Bet Termalica Nieciecza"
    ],
    'hnl': [
        "GNK Dinamo Zagreb", "HNK Hajduk Split", "HNK Rijeka",
        "NK Osijek", "NK Istra 1961", "NK Lokomotiva Zagreb",
        "NK Varazdin", "Slaven Belupo Koprivnica", "HNK Gorica",
        "HNK Vukovar 1991"
    ],
    'superliga_denmark': [
        "FC Midtjylland", "FC Copenhagen", "Bröndby IF", "Aarhus GF",
        "FC Nordsjaelland", "Viborg FF", "Silkeborg IF",
        "Vejle Boldklub", "Randers FC", "Sönderjyske Fodbold",
        "Odense Boldklub", "FC Fredericia"
    ],
    'turkish_super_lig': [
        "Galatasaray", "Fenerbahce", "Besiktas JK", "Trabzonspor",
        "Basaksehir FK", "Samsunspor", "Caykur Rizespor", "Göztepe",
        "Antalyaspor", "Gaziantep FK", "Eyüpspor", "Kocaelispor",
        "Alanyaspor", "Konyaspor", "Genclerbirligi Ankara",
        "Kayserispor", "Fatih Karagümrük", "Kasimpasa"
    ]
}