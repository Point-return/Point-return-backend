import sys
from datetime import datetime

import pandas as pd
from numpy import nan

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.core.utils import convert_string_to_float
from app.products.dao import ParsedProductDealerDAO, StatisticsDAO

IMPORTING_PER_TIME = 1000


async def import_parsed_data() -> None:
    """Import parsing data."""
    logger.debug(
        'Importing parsing data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.parsed_data}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        data = pd.read_csv(csv_file, delimiter=';', na_filter=False)
        data = data.drop('product_key', axis=1)
        existing_parsed_data_ids = await ParsedProductDealerDAO.get_ids()
        for index, row in data.iterrows():
            if row['id'] in existing_parsed_data_ids:
                data.drop(index, inplace=True)
        new_number = len(data.index)
        data['price'] = data['price'].apply(convert_string_to_float)
        data['date'] = data['date'].apply(
            lambda date: datetime.strptime(date, '%Y-%m-%d').date(),
        )
        data.replace({nan: None}, inplace=True)
        data_ids = data[['id']].copy()
        data_ids = data_ids.rename(columns={'id': 'parsed_data_id'})
        dicts = data.to_dict('records')
        amount_of_iterations = len(dicts) // IMPORTING_PER_TIME
        for iterator in range(amount_of_iterations):
            await ParsedProductDealerDAO.create_many(
                data.to_dict('records')[
                    iterator
                    * IMPORTING_PER_TIME : (iterator + 1)
                    * IMPORTING_PER_TIME
                ],
            )
            await StatisticsDAO.create_many(
                data_ids.to_dict('records')[
                    iterator
                    * IMPORTING_PER_TIME : (iterator + 1)
                    * IMPORTING_PER_TIME
                ],
            )
        await ParsedProductDealerDAO.create_many(
            data.to_dict('records')[
                amount_of_iterations * IMPORTING_PER_TIME :
            ],
        )
        await StatisticsDAO.create_many(
            data_ids.to_dict('records')[
                amount_of_iterations * IMPORTING_PER_TIME :
            ],
        )
        logger.debug(
            f'Import completed, {new_number} parsing data imported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_parsed_data())
