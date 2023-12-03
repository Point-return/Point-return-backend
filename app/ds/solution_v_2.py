import pandas as pd
from fuzzywuzzy import fuzz

from app.config import logger
from app.products.dao import ProductDAO


def get_not_continuous_words(data):
    """Separate the combined words in a column 'name'.

    Args:
        data: что за переменная? 
    
    Returns:
        что возвращает модель?
    """
    list_product_word = [
        'PROSEPT',
        'концентрат',
        'Crystal',
        'готовый',
        'Duty',
        'Multipower',
        'MULTIPOWER',
        'White',
        'Belizna',
        'Cooky',
        'Diona',
        'готовое',
        'ULTRA',
        'Antifoam',
        'Bath',
        'Universal',
        'Carpet',
        'концентрированное',
        'Flox',
        'эффектом',
        'splash',
        'epoxy',
        'Candy',
        'Optic',
        'Clean',
        'шампунь',
        'штуки',
        'Super',
        'Plastix',
        'Proplast',
        'Ириса',
        'FLOX',
    ]

    result = data['name']
    for word in list_product_word:
        tmp_str = result.split(str(word))
        if len(tmp_str) > 1:
            result = tmp_str[0] + ' ' + word + ' ' + tmp_str[1]

    return result


def get_not_continuous_words_when_entering(row):
    '''The function separates concatenated
    words when entering a dealer product.
    '''
    list_product_dealer = [
        'антижук',
        'PROSEPT',
        'universal',
        'ULTRA',
        'grill',
        'удаления',
        'floor',
        'remover',
        'средство',
        'стекол',
        'зеркал',
        'пластика',
        'акриловых',
        'bath',
        'acryl',
        'profi',
        'Eco',
        'multipower',
        'xm11',
        'graffiti',
        'плесени',
        'грибка',
        'gel',
        'снятия',
        'shine',
        'грунтовка',
        '20л',
        '10л',
        '2л',
        'hand',
        'cristal',
        'против',
        'лак',
        'полуматовый',
        'глянцевый',
        'невымываемый',
        'машины',
        'splash',
        'орех',
        'сlean',
        'acid',
        'polish',
        'удаления',
        'hard',
        'посуды',
        'полов',
        'комнат',
        'spray',
        'посудомоечной',
        'lime',
        'rinser',
        'sport',
        'спортивной',
        'черных',
        'black',
        'сауны',
        'бани',
        'труб',
        'засоров',
        'extra',
        'после',
        'очистки',
        'ухода',
        'мебелью',
        'зеленый',
        'красный',
        'fungi',
    ]
    result = row
    for word in list_product_dealer:
        result_split = result.split(word)
        if len(result_split) > 1:
            result = result_split[0] + ' ' + word + ' ' + result_split[1]

    return result


def get_suitable_products(
    dealer_product: str,
    manufacturer_products: pd.Series,
    levenshtein_distance_max: int,
) -> list:
    '''A Model Explanation System
    return: Array of suitable manufactur products
    '''
    suitable_products = []
    for product in manufacturer_products['name_split']:
        l_d = fuzz.token_sort_ratio(
            get_not_continuous_words_when_entering(dealer_product), product
        )
        if l_d >= levenshtein_distance_max:
            manufacturer_products_id = manufacturer_products[
                manufacturer_products['name_split'] == product
            ]['id'].to_string(index=False)
            suitable_products.append(
                {
                    'id': manufacturer_products_id,
                    'product_name': product,
                    'levenshtein_distance': l_d,
                }
            )
    return suitable_products


async def get_solution(
    dealer_product: str,
    length: int = 10,
    levenshtein_distance_max: int = 50,
) -> list:
    manufacturer_products = pd.DataFrame(await ProductDAO.get_ids_names())
    # manufacturer_products = pd.read_csv('manufacturer_data.csv')
    manufacturer_products = manufacturer_products.dropna()
    manufacturer_products['name_split'] = manufacturer_products.apply(
        get_not_continuous_words, axis=1
    )
    suitable_solution = get_suitable_products(
        get_not_continuous_words_when_entering(dealer_product),
        manufacturer_products,
        levenshtein_distance_max,
    )
    solution = sorted(
        suitable_solution,
        key=lambda x: x['levenshtein_distance'],
        reverse=True,
    )
    last_index = length if length < len(solution) else len(solution)

    return solution[0:last_index]


if __name__ == '__main__':
    import asyncio

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(get_solution('Средство для удаления ленты  клейкой '))
