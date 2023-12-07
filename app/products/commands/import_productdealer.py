import sys

import pandas as pd

from app.config import DATA_IMPORT_LOCATION, CSVFilenames, logger
from app.products.dao import ProductDealerDAO
from app.products.utils import generate_product_dealer_key


async def import_productdealer() -> None:
    """Import product-dealer links."""
    logger.debug(
        'Importing product-dealer data from: ' f'{DATA_IMPORT_LOCATION}',
    )
    with open(
        f'{DATA_IMPORT_LOCATION}/{CSVFilenames.product_dealer}.csv',
        'r',
        encoding='utf-8-sig',
    ) as csv_file:
        data = pd.read_csv(csv_file, delimiter=';', na_filter=False)
        data = data.drop('id', axis=1)
        existing_productdealer_keys = await ProductDealerDAO.get_keys()
        wrong_data = pd.DataFrame(columns=data.columns)
        for index, row in data.iterrows():
            if not row['key'].isnumeric():
                wrong_data = pd.concat(
                    [wrong_data, pd.DataFrame([row])],
                    ignore_index=True,
                )
                data.drop(index, inplace=True)
        data['key'] = data['key'].apply(int)
        for index, row in data.iterrows():
            if int(row['key']) in existing_productdealer_keys:
                data.drop(index, inplace=True)
        new_number = len(data.index)
        await ProductDealerDAO.create_many(data.to_dict('records'))
        wrong_data = wrong_data.drop('key', axis=1)
        new_wrong_number = len(wrong_data.index)
        for index, row in wrong_data.iterrows():
            await ProductDealerDAO.create(
                **row,
                key=await generate_product_dealer_key(),
            )
    logger.debug(
        f'Import completed, imported {new_number+new_wrong_number} '
        'product-dealer links',
    )


if __name__ == '__main__':
    import asyncio

    if sys.platform == 'win32' and sys.version_info.minor >= 8:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.get_event_loop_policy().new_event_loop()
    asyncio.run(import_productdealer())
