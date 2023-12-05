import sys

import pandas as pd
from numpy import nan

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.core.utils import (
    convert_string_to_float,
    convert_to_float_and_truncate,
)
from app.products.dao import ProductDAO


async def import_products() -> None:
    """Import products."""
    logger.debug(
        'Importing product data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.products}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        data = pd.read_csv(
            csv_file,
            delimiter=';',
            index_col=0,
            na_filter=False,
        )
        data.replace({nan: None}, inplace=True)
        for column in ['ean_13', 'category_id', 'ozon_article', 'wb_article']:
            data[column] = data[column].apply(convert_to_float_and_truncate)
        for column in ['cost', 'recommended_price']:
            data[column] = data[column].apply(convert_string_to_float)
        data.replace({nan: None}, inplace=True)
        existing_products_ids = await ProductDAO.get_ids()
        for index, row in data.iterrows():
            if row['id'] in existing_products_ids:
                data.drop(index, inplace=True)
        new_number = len(data.index)
        await ProductDAO.create_many(data.to_dict('records'))
        logger.debug(
            f'Import completed, {new_number} products imported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_products())
