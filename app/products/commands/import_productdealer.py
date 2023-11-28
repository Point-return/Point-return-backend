import csv

from app.config import DATA_IMPORT_LOCATION, CSVFilenames
from app.products.dao import ProductDealerDAO


async def import_productdealer() -> None:
    """Функция для импорта связок продукт-дилер."""
    print(  # noqa: T201
        'Импортируются данные связок продукт-дилер из:',
        DATA_IMPORT_LOCATION,
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
        print(  # noqa: T201
            f'Импорт завершён, импортировано {counter} '
            'связок пользователь-дилер',
        )


if __name__ == '__main__':
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(import_productdealer())
