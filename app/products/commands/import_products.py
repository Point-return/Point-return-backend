import csv
import sys

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.core.utils import (
    convert_string_to_float,
    convert_to_float_and_truncate,
)
from app.products.dao import ProductDAO


async def import_products() -> None:
    """Import products."""
    logger.debug(
        'Imports product data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.products}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        counter = 0
        data = csv.reader(csv_file, delimiter=';')
        next(data)
        for (
            _,
            id,
            article,
            ean_13,
            name,
            cost,
            recommended_price,
            category_id,
            ozon_name,
            name_1c,
            wb_name,
            ozon_article,
            wb_article,
            ym_article,
            wb_article_td,
        ) in data:
            existing_product = await ProductDAO.find_by_id(int(id))
            if not existing_product:
                await ProductDAO.create(
                    id=int(id),
                    article=article,
                    ean_13=convert_to_float_and_truncate(ean_13),
                    name=name,
                    cost=convert_string_to_float(cost),
                    recommended_price=convert_string_to_float(
                        recommended_price,
                    ),
                    category_id=convert_to_float_and_truncate(category_id),
                    ozon_name=ozon_name,
                    name_1c=name_1c,
                    wb_name=wb_name,
                    ozon_article=convert_to_float_and_truncate(ozon_article),
                    wb_article=convert_to_float_and_truncate(wb_article),
                    ym_article=ym_article,
                    wb_article_td=wb_article_td,
                )
                counter += 1
        logger.debug(
            f'Import completed, {counter} products imported',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_products())
