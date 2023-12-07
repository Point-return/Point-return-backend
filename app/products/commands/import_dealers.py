import sys

import pandas as pd

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.products.dao import DealerDAO


async def import_dealers() -> None:
    """Import dealers."""
    logger.debug(
        'Importing dealer data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.dealers}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        data = pd.read_csv(csv_file, delimiter=';', na_filter=False)
        existing_dealers_ids = await DealerDAO.get_ids()
        for index, row in data.iterrows():
            if row['id'] in existing_dealers_ids:
                data.drop(index, inplace=True)
        new_number = len(data.index)
        dicts = data.to_dict('records')
        await DealerDAO.create_many(dicts)
        logger.debug(
            f'Import completed, {new_number} dealers imported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_dealers())
