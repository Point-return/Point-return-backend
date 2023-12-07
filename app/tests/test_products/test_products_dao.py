from typing import Any, Dict, List

from app.products.dao import ProductDAO, ProductDealerDAO, StatisticsDAO


async def test_get_product_ids_names(products: List[Dict[str, Any]]) -> None:
    """Test getting if and name of each product.

    Args:
        products: pytest fixrute with products data.
    """
    ids_names = await ProductDAO.get_ids_names()
    for iterator in range(len(ids_names)):
        id_name = ids_names[iterator]
        product = products[iterator]
        assert id_name['id'] == product['id']
        assert id_name['name'] == product['name']
        assert set(id_name.keys()) == {'id', 'name'}


class TestProductDealerKeys:
    """TestClass for testing DAO functions with product-dealer keys."""

    async def test_get_min_key(
        self,
        product_dealer: List[Dict[str, Any]],
    ) -> None:
        """Test getting min product-dealer key.

        Args:
            product_dealer: pytest fixrute with product-dealer data.
        """
        db_min_key = min(map(lambda item: item['key'], product_dealer))
        found_min_key = await ProductDealerDAO.get_min_key()
        assert db_min_key == found_min_key

    async def test_get_max_key(
        self,
        product_dealer: List[Dict[str, Any]],
    ) -> None:
        """Test getting max product-dealer key.

        Args:
            product_dealer: pytest fixrute with product-dealer data.
        """
        db_max_key = max(map(lambda item: item['key'], product_dealer))
        found_max_key = await ProductDealerDAO.get_max_key()
        assert db_max_key == found_max_key

    async def test_get_all_keys(
        self,
        product_dealer: List[Dict[str, Any]],
    ) -> None:
        """Test getting all product-dealer keys.

        Args:
            product_dealer: pytest fixrute with product-dealer data.
        """
        db_keys = set(map(lambda item: item['key'], product_dealer))
        found_keys = set(await ProductDealerDAO.get_keys())
        assert db_keys == found_keys

    async def test_get_key(
        self,
        product_dealer: List[Dict[str, Any]],
    ) -> None:
        """Test getting specific product-dealer key.

        Args:
            product_dealer: pytest fixrute with product-dealer data.
        """
        for product_dealer_item in product_dealer:
            found_key = await ProductDealerDAO.get_key(
                product_id=product_dealer_item['product_id'],
                dealer_id=product_dealer_item['dealer_id'],
            )
            assert found_key == product_dealer_item['key']


class TestStatisticsDAO:
    """TestClass for statistics DAO."""

    async def test_skipped(self, parsed_data: List[Dict[str, Any]]) -> None:
        """Test changing skipper parameter to True.

        Args:
            parsed_data: pytest fixture with parsed data.
        """
        for parsed_data_item in parsed_data:
            parsed_data_item_id = parsed_data_item['id']
            statistic_item = await StatisticsDAO.find_one_or_none(
                parsed_data_id=parsed_data_item_id,
            )
            await StatisticsDAO.update_skip(parsed_data_item_id)
            statistic_item = await StatisticsDAO.find_one_or_none(
                parsed_data_id=parsed_data_item_id,
            )
            assert statistic_item.skipped is True

    async def test_success(self, parsed_data: List[Dict[str, Any]]) -> None:
        """Test changing successfull parameter to True.

        Args:
            parsed_data: pytest fixture with parsed data.
        """
        for parsed_data_item in parsed_data:
            parsed_data_item_id = parsed_data_item['id']
            statistic_item = await StatisticsDAO.find_one_or_none(
                parsed_data_id=parsed_data_item_id,
            )
            await StatisticsDAO.update_success(parsed_data_item_id)
            statistic_item = await StatisticsDAO.find_one_or_none(
                parsed_data_id=parsed_data_item_id,
            )
            assert statistic_item.successfull is True
            assert statistic_item.skipped is False
