import pandas as pd
import numpy as np
from pathlib import Path
from functools import lru_cache


ROLE_GROUP_MAP = {
    "Goalkeeper": "GK",
    "Centre-Back": "DEF",
    "Left-Back": "DEF",
    "Right-Back": "DEF",
    "Defensive Midfield": "MID",
    "Central Midfield": "MID",
    "Attacking Midfield": "MID",
    "Left Midfield": "MID",
    "Right Midfield": "MID",
    "Left Winger": "ATT",
    "Right Winger": "ATT",
    "Centre-Forward": "ATT",
    "Second Striker": "ATT"
}

RADAR_SKILLS = {
    "attacking": [
        "goals", "expectedGoals", "totalShots", "shotsOnTarget",
        "goalConversionPercentage", "bigChancesMissed"
    ],
    "passing": [
        "assists", "expectedAssists", "keyPasses", "accuratePassesPercentage",
        "accurateFinalThirdPasses", "bigChancesCreated"
    ],
    "dribbling": [
        "successfulDribbles", "successfulDribblesPercentage",
        "possessionWonAttThird", "touches"
    ],
    "defending": [
        "tackles", "tacklesWon", "interceptions", "clearances",
        "blockedShots", "ballRecovery"
    ],
    "physical": [
        "groundDuelsWon", "groundDuelsWonPercentage",
        "aerialDuelsWon", "aerialDuelsWonPercentage",
        "totalDuelsWon", "totalDuelsWonPercentage"
    ]
}


class PlayerDataService:
    
    def __init__(self, data_path: str = None):
        if data_path is None:
            data_path = Path(__file__).parent.parent / "data" / "cleaned_player_data.csv"
        self.data_path = Path(data_path)
        self._df = None
        self._load_data()
    
    def _load_data(self):
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        self._df = pd.read_csv(self.data_path)
        
        self._df["positionGroup"] = self._df["position"].map(ROLE_GROUP_MAP).fillna("UNK")
        
        self._calculate_radar_percentiles()
    
    def _calculate_radar_percentiles(self):
        for category, columns in RADAR_SKILLS.items():
            available_cols = [c for c in columns if c in self._df.columns]
            if available_cols:
                means = self._df[available_cols].apply(
                    lambda x: pd.to_numeric(x, errors='coerce')
                ).mean(axis=1, skipna=True)
                
                self._df[f"radar_{category}"] = means.rank(pct=True) * 100
            else:
                self._df[f"radar_{category}"] = 50.0  
        
    
        if "rating" in self._df.columns:
            self._df["radar_rating"] = pd.to_numeric(
                self._df["rating"], errors='coerce'
            ).rank(pct=True) * 100
        else:
            self._df["radar_rating"] = 50.0
    
    def get_players(
        self,
        page: int = 1,
        limit: int = 50,
        search: str = None,
        position_group: str = None,
        team: str = None,
        sort_by: str = "marketValue",
        sort_order: str = "desc"
    ) -> tuple[list[dict], int]:
        df = self._df.copy()
        
        # Apply filters
        if search:
            search_lower = search.lower()
            df = df[
                df["name"].str.lower().str.contains(search_lower, na=False) |
                df["player_name"].str.lower().str.contains(search_lower, na=False)
            ]
        
        if position_group and position_group != "ALL":
            df = df[df["positionGroup"] == position_group]
        
        if team:
            df = df[df["teamName"].str.contains(team, case=False, na=False)]
        
        # Sort
        sort_col_map = {
            "marketValue": "MarketValueCurrent",
            "rating": "rating",
            "name": "name",
            "age": "age",
            "goals": "goals"
        }
        sort_col = sort_col_map.get(sort_by, "MarketValueCurrent")
        if sort_col in df.columns:
            ascending = sort_order.lower() == "asc"
            df = df.sort_values(by=sort_col, ascending=ascending, na_position='last')
        
        total = len(df)
        
        # Paginate
        start = (page - 1) * limit
        end = start + limit
        df_page = df.iloc[start:end]
        
        # Convert to list of dicts
        players = []
        for _, row in df_page.iterrows():
            players.append({
                "playerId": int(row.get("playerId", 0)),
                "name": str(row.get("name", row.get("player_name", "Unknown"))),
                "teamName": str(row.get("teamName", "Unknown")).split(" ~ ")[0],
                "position": str(row.get("position", "Unknown")),
                "positionGroup": str(row.get("positionGroup", "UNK")),
                "age": float(row["age"]) if pd.notna(row.get("age")) else None,
                "marketValue": float(row["MarketValueCurrent"]) if pd.notna(row.get("MarketValueCurrent")) else None,
                "marketValueCurrency": str(row.get("MarketValueCurrency", "EUR")),
                "rating": float(row["rating"]) if pd.notna(row.get("rating")) else None,
                "appearances": int(row["appearances"]) if pd.notna(row.get("appearances")) else None
            })
        
        return players, total
    
    def get_player_by_id(self, player_id: int) -> dict | None:
        """Get detailed player information by ID."""
        df = self._df[self._df["playerId"] == player_id]
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        
        # Determine market value trend
        current = row.get("MarketValueCurrent")
        previous = row.get("MarketValuePrevious")
        if pd.notna(current) and pd.notna(previous):
            if current > previous:
                trend = "up"
            elif current < previous:
                trend = "down"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        return {
            "playerId": int(row.get("playerId", 0)),
            "name": str(row.get("name", row.get("player_name", "Unknown"))),
            "teamName": str(row.get("teamName", "Unknown")).split(" ~ ")[0],
            "position": str(row.get("position", "Unknown")),
            "positionGroup": str(row.get("positionGroup", "UNK")),
            "firstSidePosition": str(row.get("firstSidePosition")) if pd.notna(row.get("firstSidePosition")) else None,
            "secondSidePosition": str(row.get("secondSidePosition")) if pd.notna(row.get("secondSidePosition")) else None,
            
            # Demographics
            "age": float(row["age"]) if pd.notna(row.get("age")) else None,
            "height": float(row["height"]) if pd.notna(row.get("height")) else None,
            "preferredFoot": str(row.get("preferredFoot")) if pd.notna(row.get("preferredFoot")) else None,
            "dateOfBirth": str(row.get("date_of_birth")) if pd.notna(row.get("date_of_birth")) else None,
            "nationalityId": int(row["nationalityId"]) if pd.notna(row.get("nationalityId")) else None,
            
            # Contract & Market
            "contractUntil": str(row.get("contractUntil")) if pd.notna(row.get("contractUntil")) else None,
            "marketValueCurrent": float(row["MarketValueCurrent"]) if pd.notna(row.get("MarketValueCurrent")) else None,
            "marketValuePrevious": float(row["MarketValuePrevious"]) if pd.notna(row.get("MarketValuePrevious")) else None,
            "marketValueCurrency": str(row.get("MarketValueCurrency", "EUR")),
            "marketValueTrend": trend,
            
            # Playing Time
            "appearances": int(row["appearances"]) if pd.notna(row.get("appearances")) else None,
            "minutesPlayed": float(row["minutesPlayed"]) if pd.notna(row.get("minutesPlayed")) else None,
            "matchesStarted": int(row["matchesStarted"]) if pd.notna(row.get("matchesStarted")) else None,
            
            # Rating
            "rating": float(row["rating"]) if pd.notna(row.get("rating")) else None,
            
            # Attacking
            "goals": float(row["goals"]) if pd.notna(row.get("goals")) else None,
            "expectedGoals": float(row["expectedGoals"]) if pd.notna(row.get("expectedGoals")) else None,
            "assists": float(row["assists"]) if pd.notna(row.get("assists")) else None,
            
            # Additional stats
            "totalPasses": float(row["totalPasses"]) if pd.notna(row.get("totalPasses")) else None,
            "accuratePassesPercentage": float(row["accuratePassesPercentage"]) if pd.notna(row.get("accuratePassesPercentage")) else None,
            "successfulDribbles": float(row["successfulDribbles"]) if pd.notna(row.get("successfulDribbles")) else None,
            "tackles": float(row["tackles"]) if pd.notna(row.get("tackles")) else None,
            "interceptions": float(row["interceptions"]) if pd.notna(row.get("interceptions")) else None,
            
            "keyPasses": float(row["keyPasses"]) if pd.notna(row.get("keyPasses")) else None,
            "bigChancesCreated": float(row["bigChancesCreated"]) if pd.notna(row.get("bigChancesCreated")) else None,
            "clearances": float(row["clearances"]) if pd.notna(row.get("clearances")) else None,
            "aerialDuelsWon": float(row["aerialDuelsWon"]) if pd.notna(row.get("aerialDuelsWon")) else None,
            "groundDuelsWon": float(row["groundDuelsWon"]) if pd.notna(row.get("groundDuelsWon")) else None,
            "totalShots": float(row["totalShots"]) if pd.notna(row.get("totalShots")) else None,
            "shotsOnTarget": float(row["shotsOnTarget"]) if pd.notna(row.get("shotsOnTarget")) else None,
            
            "radar": {
                "attacking": float(row.get("radar_attacking", 50)),
                "passing": float(row.get("radar_passing", 50)),
                "dribbling": float(row.get("radar_dribbling", 50)),
                "defending": float(row.get("radar_defending", 50)),
                "physical": float(row.get("radar_physical", 50)),
                "rating": float(row.get("radar_rating", 50))
            },
            
            "detailedStats": {
                "attacking": {
                    "Goals": int(row["goals"]) if pd.notna(row.get("goals")) else 0,
                    "xG": round(float(row["expectedGoals"]), 2) if pd.notna(row.get("expectedGoals")) else 0,
                    "Shots": int(row["totalShots"]) if pd.notna(row.get("totalShots")) else 0,
                    "On Target": int(row["shotsOnTarget"]) if pd.notna(row.get("shotsOnTarget")) else 0
                },
                "passing": {
                    "Assists": int(row["assists"]) if pd.notna(row.get("assists")) else 0,
                    "Key Passes": int(row["keyPasses"]) if pd.notna(row.get("keyPasses")) else 0,
                    "Pass %": round(float(row["accuratePassesPercentage"]), 1) if pd.notna(row.get("accuratePassesPercentage")) else 0,
                    "Chances Created": int(row["bigChancesCreated"]) if pd.notna(row.get("bigChancesCreated")) else 0
                },
                "dribbling": {
                    "Dribbles": int(row["successfulDribbles"]) if pd.notna(row.get("successfulDribbles")) else 0,
                    "Dribble %": round(float(row["successfulDribblesPercentage"]), 1) if pd.notna(row.get("successfulDribblesPercentage")) else 0,
                    "Touches": int(row["touches"]) if pd.notna(row.get("touches")) else 0
                },
                "defending": {
                    "Tackles": int(row["tackles"]) if pd.notna(row.get("tackles")) else 0,
                    "Interceptions": int(row["interceptions"]) if pd.notna(row.get("interceptions")) else 0,
                    "Clearances": int(row["clearances"]) if pd.notna(row.get("clearances")) else 0,
                    "Blocks": int(row["blockedShots"]) if pd.notna(row.get("blockedShots")) else 0
                },
                "physical": {
                    "Ground Duels": int(row["groundDuelsWon"]) if pd.notna(row.get("groundDuelsWon")) else 0,
                    "Aerial Duels": int(row["aerialDuelsWon"]) if pd.notna(row.get("aerialDuelsWon")) else 0,
                    "Duels Won %": round(float(row["totalDuelsWonPercentage"]), 1) if pd.notna(row.get("totalDuelsWonPercentage")) else 0
                }
            }
        }
    
    def get_radar_data(self, player_id: int) -> dict | None:
        """Get radar chart data for a player."""
        df = self._df[self._df["playerId"] == player_id]
        
        if df.empty:
            return None
        
        row = df.iloc[0]
        
        return {
            "attacking": float(row.get("radar_attacking", 50)),
            "passing": float(row.get("radar_passing", 50)),
            "dribbling": float(row.get("radar_dribbling", 50)),
            "defending": float(row.get("radar_defending", 50)),
            "physical": float(row.get("radar_physical", 50)),
            "rating": float(row.get("radar_rating", 50))
        }
    
    def get_positions(self) -> list[dict]:
        """Get all available position groups."""
        return [
            {"id": "ALL", "name": "All Positions"},
            {"id": "GK", "name": "Goalkeeper"},
            {"id": "DEF", "name": "Defenders"},
            {"id": "MID", "name": "Midfielders"},
            {"id": "ATT", "name": "Attackers"}
        ]
    
    def get_teams(self) -> list[str]:
        """Get all unique team names."""
        teams = self._df["teamName"].str.split(" ~ ").str[0].unique()
        return sorted([t for t in teams if pd.notna(t)])


@lru_cache(maxsize=1)
def get_data_service() -> PlayerDataService:
    """Get the singleton data service instance."""
    return PlayerDataService()
