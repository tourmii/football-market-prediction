import asyncio
from sofascore_scraper import SofaScoreScraper


async def collect_players_workflow():
    """
    Workflow 1: Collect players from a specific league
    """
    scraper = SofaScoreScraper()
    
    try:
        league_id = 170
        season_id = 61243
        output_file = f'players_data_{league_id}.csv'
        
        df = await scraper.collect_players_from_league(
            league_id=league_id,
            season_id=season_id,
            output_file=output_file
        )
        
        print(f"\n{'='*50}")
        print("COLLECTION COMPLETE!")
        print(f"{'='*50}")
        print(df.head(10))
        
        return df
        
    finally:
        await scraper.close()


async def enrich_stats_workflow():
    """
    Workflow 2: Enrich player data with statistics from multiple leagues
    """
    scraper = SofaScoreScraper()
    
    try:
        input_file = 'players_data_170.csv'
        output_file = f'stats_{input_file}'
        
        df = await scraper.enrich_player_stats(
            input_file=input_file,
            output_file=output_file
        )
        
        print(f"\n{'='*50}")
        print("ENRICHMENT COMPLETE!")
        print(f"{'='*50}")
        print(df.head(10))
        
        return df
        
    finally:
        await scraper.close()


async def full_pipeline_workflow(league_id: int = 170, season_id: int = 61243):
    """
    Workflow 3: Complete pipeline - collect players then enrich with stats
    """
    scraper = SofaScoreScraper()
    
    try:
        print("STEP 1: Collecting players...")
        players_file = f'players_data_{league_id}.csv'
        await scraper.collect_players_from_league(
            league_id=league_id,
            season_id=season_id,
            output_file=players_file
        )
        
        print("\n" + "="*50)
        print("STEP 2: Enriching with statistics...")
        print("="*50 + "\n")
        
        stats_file = f'stats_{players_file}'
        df_final = await scraper.enrich_player_stats(
            input_file=players_file,
            output_file=stats_file
        )
        
        print(f"\n{'='*50}")
        print("PIPELINE COMPLETE!")
        print(f"{'='*50}")
        print(f"Players collected: {players_file}")
        print(f"Stats enriched: {stats_file}")
        
        return df_final
        
    finally:
        await scraper.close()


if __name__ == "__main__":
    print("Choose workflow:")
    print("1. Collect players from league")
    print("2. Enrich existing player data with stats")
    print("3. Full pipeline (collect + enrich)")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        asyncio.run(collect_players_workflow())
    elif choice == "2":
        asyncio.run(enrich_stats_workflow())
    elif choice == "3":
        asyncio.run(full_pipeline_workflow())
    else:
        print("Invalid choice!")
        
    print("\nDone!")