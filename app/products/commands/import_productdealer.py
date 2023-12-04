import csv
import sys

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.products.dao import ProductDealerDAO
from app.products.utils import generate_product_dealer_key


async def import_productdealer() -> None:
    """Import product-dealer links."""
    logger.debug(
        'Product-dealer link data is imported from: '
        f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.product_dealer}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        counter = 0
        data = csv.reader(csv_file, delimiter=';')
        wrong_data = []
        next(data)
        for (
            _,
            key,
            dealer_id,
            product_id,
        ) in data:
            try:
                integer_key = int(key)
            except ValueError:
                wrong_data.append((dealer_id, product_id))
                continue
            existing_product_dealer = await ProductDealerDAO.find_one_or_none(
                key=integer_key,
            )
            if not existing_product_dealer:
                await ProductDealerDAO.create(
                    key=integer_key,
                    dealer_id=int(dealer_id),
                    product_id=int(product_id),
                )
                counter += 1
    for dealer_id, product_id in wrong_data:
        existing_product_dealer = await ProductDealerDAO.find_one_or_none(
            dealer_id=int(dealer_id),
            product_id=int(product_id),
        )
        if not existing_product_dealer:
            await ProductDealerDAO.create(
                key=await generate_product_dealer_key(),
                dealer_id=int(dealer_id),
                product_id=int(product_id),
            )
            counter += 1
    logger.debug(
        f'Import completed, imported {counter} ' 'user-dealer links',
    )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_productdealer())
