import csv
import sys

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.products.dao import ProductDealerDAO


async def import_productdealer() -> None:
    """Функция для импорта связок продукт-дилер."""
    logger.debug(
        'Импортируются данные связок продукт-дилер из: '
        f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.product_dealer}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        counter = 0
        data = csv.reader(csv_file, delimiter=';')
        next(data)
        for (
            id,
            key,
            dealer_id,
            product_id,
        ) in data:
            existing_product_dealer = await ProductDealerDAO.find_by_id(
                int(id),
            )
            if not existing_product_dealer:
                await ProductDealerDAO.create(
                    id=int(id),
                    key=key,
                    dealer_id=int(dealer_id),
                    product_id=int(product_id),
                )
                counter += 1
        logger.debug(
            f'Импорт завершён, импортировано {counter} '
            'связок пользователь-дилер',
        )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_productdealer())
