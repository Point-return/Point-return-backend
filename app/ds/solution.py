import pandas as pd
from fuzzywuzzy import fuzz

from app.config import logger
from app.products.dao import ProductDAO


def get_suitable_products(
    dealer_product: str,
    manufactur_products: pd.Series,
    levenshtein_distance_max: int,
) -> list:
    """Create a model explanation system.

    Returns:
        Array of suitable manufactur products.
    """
    suitable_products = []
    for product in manufactur_products['name']:
        l_d = fuzz.token_sort_ratio(dealer_product, product)
        if l_d >= levenshtein_distance_max:
            manufactur_product_id = manufactur_products[
                manufactur_products['name'] == product
            ]['id'].to_string(index=False)
            suitable_products.append(
                {
                    'id': manufactur_product_id,
                    'product_name': product,
                    'levenshtein_distance': l_d,
                },
            )
    return suitable_products


async def get_solution(
    dealer_product: str,
    length: int = 10,
    levenshtein_distance_max: int = 50,
) -> list:
    """Get solution.

    Args:
        dealer_product:
        lengthL
        levenshtein_distance_max:

    Returns:
        List of solutions.
    """
    manufactur_products1 = pd.DataFrame(await ProductDAO.get_ids_names())
    # manufactur_products = pd.read_csv('app/ds/manufacturer_data.csv')

    suitable_solution = get_suitable_products(
        dealer_product,
        manufactur_products1,
        levenshtein_distance_max,
    )
    solution = sorted(
        suitable_solution,
        key=lambda x: x['levenshtein_distance'],
        reverse=True,
    )
    last_index = length if length < len(solution) else len(solution)
    logger.debug(solution[0:last_index])

    return solution[0:last_index]


if __name__ == '__main__':
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_solution('Средство для удаления ленты  клейкой '))
