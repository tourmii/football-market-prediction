LEAGUE_CONFIGS = [
    {"league_id": 170, "season_id": 61243, "name": "Premier League"},
    {"league_id": 17, "season_id": 61627, "name": "La Liga"},
    {"league_id": 8, "season_id": 61643, "name": "Bundesliga"},
    {"league_id": 35, "season_id": 63516, "name": "Serie A"},
    {"league_id": 34, "season_id": 61736, "name": "Ligue 1"},
    {"league_id": 23, "season_id": 63515, "name": "Belgian Pro League"},
    {"league_id": 38, "season_id": 61459, "name": "Liga Portugal"},
    {"league_id": 325, "season_id": 58766, "name": "MLS"},
    {"league_id": 242, "season_id": 70158, "name": "Championship"},
    {"league_id": 18, "season_id": 61961, "name": "Eredivisie"},
    {"league_id": 238, "season_id": 63670, "name": "Brazilian Serie A"},
    {"league_id": 37, "season_id": 61666, "name": "Argentine Primera"},
    {"league_id": 155, "season_id": 57478, "name": "Polish Ekstraklasa"},
    {"league_id": 202, "season_id": 61236, "name": "Croatian HNL"},
    {"league_id": 39, "season_id": 61326, "name": "Danish Superliga"},
    {"league_id": 519, "season_id": 65808, "name": "Turkish Super Lig"}
]

PREDEFINED_LEAGUES = [config["league_id"] for config in LEAGUE_CONFIGS]
PREDEFINED_SEASONS = [config["season_id"] for config in LEAGUE_CONFIGS]
SEARCH_PAIRS = list(zip(PREDEFINED_LEAGUES, PREDEFINED_SEASONS))

PRIORITY_COLUMNS = [
    'player_name', 
    'current_club', 
    'data_source_league_id', 
    'season_team_name', 
    'rating', 
    'goals', 
    'assists', 
    'market_value_eur'
]
