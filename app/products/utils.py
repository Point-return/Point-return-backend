from app.products.dao import ProductDealerDAO


async def generate_product_dealer_key() -> int:
    """Generate unique key for new ProductDealer model.

    Returns:
        Generated key.
    """
    minimum_key = await ProductDealerDAO.get_min_key()
    if minimum_key > 1:
        return minimum_key - 1
    maximum_key = await ProductDealerDAO.get_max_key()
    keys = await ProductDealerDAO.get_keys()
    if len(keys) < maximum_key - minimum_key + 1:
        allowed_between_keys = set(range(minimum_key, maximum_key + 1)) - set(
            keys,
        )
        return min(allowed_between_keys)
    return maximum_key + 1
