import pandas as pd
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from sofascore_wrapper.api import SofascoreAPI
from sofascore_wrapper.league import League
from sofascore_wrapper.team import Team
from sofascore_wrapper.player import Player
from sofascore_config import SEARCH_PAIRS, PRIORITY_COLUMNS


class SofaScoreScraper:
    def __init__(self):
        self.api = SofascoreAPI()

    async def close(self):
        await self.api.close()

    @staticmethod
    def timestamp_to_date(ts: Optional[int]) -> Optional[str]:
        if ts:
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        return None

    @staticmethod
    def get_team_mapping(standings_data: Dict[str, Any]) -> Dict[int, str]:
        team_dict = {}
        
        if standings_data and 'standings' in standings_data and len(standings_data['standings']) > 0:
            standings_total = standings_data['standings'][0]
            rows = standings_total.get('rows', [])

            for row in rows:
                team_info = row.get('team', {})
                t_id = team_info.get('id')
                t_name = team_info.get('name')

                if t_id and t_name:
                    team_dict[t_id] = t_name

        return team_dict

    async def collect_players_from_league(
        self, 
        league_id: int, 
        season_id: int,
        output_file: Optional[str] = None
    ) -> pd.DataFrame:
        print(f"--- Collecting players from League ID: {league_id} ---")
        
        league = League(self.api, league_id=league_id)
        standings_obj = await league.standings(season=season_id)

        all_players_data = []

        if standings_obj and 'standings' in standings_obj:
            rows = standings_obj['standings'][0].get('rows', [])
            print(f"Found {len(rows)} teams. Starting player collection...\n")

            for row in rows:
                team_info = row.get('team', {})
                club_id = team_info.get('id')
                club_name = team_info.get('name')

                if club_id:
                    print(f"Processing: {club_name} (ID: {club_id})...")

                    try:
                        team_instance = Team(self.api, team_id=club_id)
                        squad_data = await team_instance.squad()

                        players = squad_data.get('players', [])
                        for item in players:
                            player = item.get('player', {})
                            p_id = player.get('id')
                            p_name = player.get('name')

                            if p_id and p_name:
                                all_players_data.append({
                                    "player_name": p_name,
                                    "player_id": p_id,
                                    "league_id": league_id,
                                    "club_name": club_name,
                                    "club_id": club_id
                                })

                        await asyncio.sleep(0.5)

                    except Exception as e:
                        print(f" -> Error fetching squad for {club_name}: {e}")

        df = pd.DataFrame(all_players_data)
        
        if output_file:
            df.to_csv(output_file, index=False)
            print(f"\nData saved to: {output_file}")
        
        print(f"Total players collected: {len(df)}")
        return df

    async def enrich_player_stats(
        self, 
        input_file: str, 
        output_file: Optional[str] = None
    ) -> pd.DataFrame:
        try:
            df_input = pd.read_csv(input_file)
            print(f"Loaded {len(df_input)} players. Starting multi-league scan...")
        except FileNotFoundError:
            print(f"Input file not found: {input_file}")
            return pd.DataFrame()

        processed_data = []

        for index, row in df_input.iterrows():
            p_id = row['player_id']
            p_name = row['player_name']
            current_club = row.get('club_name', 'Unknown')

            print(f"[{index + 1}/{len(df_input)}] {p_name} (ID: {p_id}) - Searching stats...")

            player_dict = await self._fetch_player_info(p_id, p_name, current_club)
            stats_found = await self._fetch_player_stats(p_id, player_dict)

            if stats_found:
                processed_data.append(player_dict)
            else:
                print(f"No stats found in any league.")
                player_dict['data_source_league_id'] = "Not Found"
                processed_data.append(player_dict)

            await asyncio.sleep(0.2)

        if processed_data:
            df_result = self._create_result_dataframe(processed_data)
            
            if output_file:
                df_result.to_csv(output_file, index=False, encoding='utf-8-sig')
                print(f"\nCompleted! File saved at: {output_file}")
            
            return df_result
        else:
            print("No data to process.")
            return pd.DataFrame()

    async def _fetch_player_info(
        self, 
        player_id: int, 
        player_name: str, 
        current_club: str
    ) -> Dict[str, Any]:
        player_dict = {
            'player_name': player_name,
            'player_id': player_id,
            'current_club': current_club
        }

        try:
            player_obj = Player(self.api, player_id=player_id)
            info_data = await player_obj.get_player()

            if 'player' in info_data:
                p_data = info_data['player']
                player_dict.update({
                    'date_of_birth': self.timestamp_to_date(p_data.get('dateOfBirthTimestamp')),
                    'height': p_data.get('height'),
                    'preferred_foot': p_data.get('preferredFoot'),
                    'position': p_data.get('position'),
                    'market_value_eur': p_data.get('proposedMarketValue'),
                    'nationality': p_data.get('country', {}).get('name')
                })
        except Exception as e:
            print(f"  -> Info Error: {e}")

        return player_dict

    async def _fetch_player_stats(
        self, 
        player_id: int, 
        player_dict: Dict[str, Any]
    ) -> bool:
        player_obj = Player(self.api, player_id=player_id)

        for search_league_id, search_season_id in SEARCH_PAIRS:
            try:
                player_stats = await player_obj.league_stats(
                    league_id=search_league_id, 
                    season=search_season_id
                )

                if player_stats and 'statistics' in player_stats:
                    stats = player_stats['statistics']
                    print(f"Found data at League ID: {search_league_id}")

                    player_dict['data_source_league_id'] = search_league_id
                    player_dict['data_source_season_id'] = search_season_id

                    try:
                        player_dict['season_team_name'] = player_stats['team']['name']
                        player_dict['season_team_id'] = player_stats['team']['id']
                    except:
                        player_dict['season_team_name'] = None

                    player_dict.update(stats)
                    if 'statisticsType' in player_dict:
                        del player_dict['statisticsType']

                    return True

            except Exception:
                continue

        return False

    @staticmethod
    def _create_result_dataframe(processed_data: List[Dict[str, Any]]) -> pd.DataFrame:
        df_result = pd.DataFrame(processed_data)

        cols = df_result.columns.tolist()
        sorted_cols = [c for c in PRIORITY_COLUMNS if c in cols] + \
                      [c for c in cols if c not in PRIORITY_COLUMNS]

        return df_result[sorted_cols]