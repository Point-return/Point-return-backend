import csv
import sys

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.products.dao import DealerDAO


async def import_dealers() -> None:
    """Function for importing dealers."""
    logger.debug(
        'Dealer data is imported from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.dealers}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        counter = 0
        data = csv.reader(csv_file, delimiter=';')
        next(data)
        for id, name in data:
            existing_dealer = await DealerDAO.find_by_id(int(id))
            if not existing_dealer:
                await DealerDAO.create(id=int(id), name=name)
                counter += 1
        logger.debug(
            f'Import completed, {counter} dealers exported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_dealers())
