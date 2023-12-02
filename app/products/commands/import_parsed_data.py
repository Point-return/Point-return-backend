import csv
import sys
from datetime import datetime

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.core.utils import convert_string_to_float
from app.products.dao import ParsedProductDealerDAO, ProductDealerDAO


async def import_parsed_data() -> None:
    """Функция для импорта данных парсинга."""
    logger.debug(
        'Импортируются данные парсинга из: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.parsed_data}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        counter = 0
        data = csv.reader(csv_file, delimiter=';')
        next(data)
        for (
            id,
            product_key,
            price,
            product_url,
            product_name,
            date,
            dealer_id,
        ) in data:
            existing_parsed_data = await ParsedProductDealerDAO.find_by_id(
                int(id),
            )
            if not existing_parsed_data:
                product_dealer = await ProductDealerDAO.find_one_or_none(
                    key=product_key,
                )
                if product_dealer:
                    await ParsedProductDealerDAO.create(
                        id=int(id),
                        product_key=product_key,
                        price=convert_string_to_float(price),
                        product_url=product_url,
                        product_name=product_name,
                        date=datetime.strptime(date, '%Y-%m-%d').date(),
                        dealer_id=int(dealer_id),
                    )
                else:
                    await ParsedProductDealerDAO.create(
                        id=int(id),
                        price=convert_string_to_float(price),
                        product_url=product_url,
                        product_name=product_name,
                        date=datetime.strptime(date, '%Y-%m-%d').date(),
                        dealer_id=int(dealer_id),
                    )
                counter += 1
        logger.debug(
            f'Импорт завершён, импортировано {counter} данных парсинга',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_parsed_data())
