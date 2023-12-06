from typing import Dict

from fastapi import status
from httpx import AsyncClient

from app.api.v1.router import (
    add_product_key,
    add_skipped,
    dealer_products,
    get_dealers,
    get_recommendations,
)
from app.main import app
from app.users.router import login_user
from app.config import logger


class TestURLs:
    """Test all URLs in system."""

    get_urls = {
        'dealers': app.url_path_for(get_dealers.__name__),
        'parsed_data_exists': app.url_path_for(
            dealer_products.__name__,
            dealerId=1,
        ),
        'parsed_data_not_exists': app.url_path_for(
            dealer_products.__name__,
            dealerId=100,
        ),
        'recommendations_exist': app.url_path_for(
            get_recommendations.__name__,
            dealerpriceId=1,
        ),
        'recommendations_not_exist': app.url_path_for(
            get_recommendations.__name__,
            dealerpriceId=100,
        ),
    }

    patch_urls = {
        'skip': app.url_path_for(add_skipped.__name__, dealerpriceId=1),
        'skip_not_exists': app.url_path_for(
            add_skipped.__name__,
            dealerpriceId=100,
        ),
        'solution': app.url_path_for(
            add_product_key.__name__,
            dealerpriceId=1,
        )
        + '?productId=1',
        'solution_no_product': app.url_path_for(
            add_product_key.__name__,
            dealerpriceId=1,
        )
        + '?productId=100',
        'solution_no_parsed_data': app.url_path_for(
            add_product_key.__name__,
            dealerpriceId=100,
        )
        + '?productId=1',
    }

    post_urls = {
        'login': app.url_path_for(login_user.__name__),
    }

    async def test_status_codes(
        self,
        user: Dict[str, str],
        async_client: AsyncClient,
    ) -> None:
        """Test status codes of all URLs."""
        get_responses_data = (
            (
                self.get_urls['dealers'],
                status.HTTP_200_OK,
                status.HTTP_200_OK,
            ),
            (
                self.get_urls['parsed_data_exists'],
                status.HTTP_200_OK,
                status.HTTP_200_OK,
            ),
            (
                self.get_urls['parsed_data_not_exists'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                self.get_urls['recommendations_exist'],
                status.HTTP_200_OK,
                status.HTTP_200_OK,
            ),
            (
                self.get_urls['recommendations_not_exist'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                self.get_urls['recommendations_not_exist'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
        )
        patch_responses_data = (
            (
                self.patch_urls['solution'],
                status.HTTP_200_OK,
                status.HTTP_200_OK,
            ),
            (
                self.patch_urls['solution_no_product'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                self.patch_urls['solution_no_parsed_data'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
            (
                self.patch_urls['skip'],
                status.HTTP_200_OK,
                status.HTTP_200_OK,
            ),
            (
                self.patch_urls['skip_not_exists'],
                status.HTTP_404_NOT_FOUND,
                status.HTTP_404_NOT_FOUND,
            ),
        )
        for get_url, unauth_status_code, _ in get_responses_data:
            response = await async_client.get(get_url)
            assert response.status_code == unauth_status_code
        for patch_url, unauth_status_code, _ in patch_responses_data:
            response = await async_client.patch(patch_url)
            assert response.status_code == unauth_status_code
        await async_client.post(
            self.post_urls['login'],
            json={
                'email': user['email'],
                'password': user['password'],
            },
        )
