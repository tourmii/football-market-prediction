import asyncio
from transfermakt_scraper import TransfermarktScraper


async def main():
    scraper = TransfermarktScraper()
    await scraper.scrape_and_save()


if __name__ == "__main__":
    asyncio.run(main())