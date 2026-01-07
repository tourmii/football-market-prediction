from tmkt import TMKT
import pandas as pd
from typing import List, Dict, Any
from leagues_config import LEAGUES


class TransfermarktScraper:
    def __init__(self):
        self.leagues = LEAGUES
        self.club_mapping: Dict[str, str] = {}
        self.club_squads: Dict[str, List[str]] = {}

    async def fetch_club_ids(self, tmkt: TMKT) -> List[List[str]]:
        all_club_ids = []
        
        for league_name, clubs in self.leagues.items():
            league_ids = []
            for club_name in clubs:
                club_search_result = await tmkt.team_search(club_name)
                club_id = club_search_result[0]['id']
                club_official_name = club_search_result[0]['name']
                
                league_ids.append(club_id)
                self.club_mapping[club_id] = club_official_name
                print(club_official_name)
            
            all_club_ids.append(league_ids)
        
        return all_club_ids

    async def fetch_squad_data(self, tmkt: TMKT, club_ids: List[List[str]]) -> None:
        for league_clubs in club_ids:
            for club_id in league_clubs:
                squad_data = await tmkt.get_club_squad(club_id)
                self.club_squads[club_id] = squad_data['data']['playerIds']

    def create_player_dict(self, player_id: str, player_data: Dict[str, Any], club_id: str) -> Dict[str, Any]:
        data = player_data['data']
        
        return {
            'playerId': player_id,
            'name': data.get('name'),
            'contractUntil': self._safe_extract(data, 'attributes', 'contractUntil'),
            'teamId': club_id,
            'teamName': self.club_mapping[club_id],
            'date_of_birth': self._safe_extract(data, 'lifeDates', 'dateOfBirth'),
            'age': self._safe_extract(data, 'lifeDates', 'age'),
            'height': self._safe_extract(data, 'attributes', 'height'),
            'preferredFoot': self._safe_extract(data, 'attributes', 'preferredFoot', 'name'),
            'preferredFootId': self._safe_extract(data, 'attributes', 'preferredFootId'),
            'position': self._safe_extract(data, 'attributes', 'position', 'name'),
            'positionId': self._safe_extract(data, 'attributes', 'position', 'id'),
            'firstSidePosition': self._safe_extract(data, 'attributes', 'firstSidePosition', 'name'),
            'firstSidePositionId': self._safe_extract(data, 'attributes', 'firstSidePosition', 'id'),
            'secondSidePosition': self._safe_extract(data, 'attributes', 'secondSidePosition', 'name'),
            'secondSidePositionId': self._safe_extract(data, 'attributes', 'secondSidePosition', 'id'),
            'nationalityId': self._safe_extract(data, 'nationalityDetails', 'nationalities', 'nationalityId'),
            'MarketValueCurrent': self._safe_extract(data, 'marketValueDetails', 'current', 'value'),
            'MarketValuePrevious': self._safe_extract(data, 'marketValueDetails', 'previous', 'value'),
            'MarketValueCurrency': self._safe_extract(data, 'marketValueDetails', 'current', 'currency')
        }

    @staticmethod
    def _safe_extract(data: Dict, *keys) -> Any:
        for key in keys:
            if isinstance(data, dict):
                data = data.get(key)
            else:
                return None
        return data

    async def fetch_player_data(self, tmkt: TMKT) -> List[Dict[str, Any]]:
        rows = []
        
        for club_id, player_ids in self.club_squads.items():
            for player_id in player_ids:
                try:
                    player_data = await tmkt.get_player(player_id)
                    print(player_data['data']['name'])
                    
                    player_dict = self.create_player_dict(player_id, player_data, club_id)
                    rows.append(player_dict)
                    
                except Exception as e:
                    print(f'Error fetching player {player_id}: {str(e)}')
                    continue
        
        return rows

    async def scrape_and_save(self, output_file: str = "data_transfermarkt.csv") -> None:
        async with TMKT() as tmkt:
            print("Fetching club IDs...")
            club_ids = await self.fetch_club_ids(tmkt)
            
            print("Fetching squad data...")
            await self.fetch_squad_data(tmkt, club_ids)
            
            print("Fetching player data...")
            player_data = await self.fetch_player_data(tmkt)
            
            print(f"Saving data to {output_file}...")
            df = pd.DataFrame(player_data)
            df.to_csv(output_file, index=False)
            print(f"Data saved successfully. Total players: {len(player_data)}")