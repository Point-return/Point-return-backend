from typing import Dict

from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


class TestAdminURL:
    """Тестирование адреса admin."""

    urls = {
        'admin': '/admin',
        'login': '/admin/login',
        'logout': '/admin/logout',
        'missing': '/admin/missing',
    }
    client = TestClient(app)

    def test_unauthorized(self) -> None:
        """URL-адрес существует и выдаёт требуемый статус."""
        response_data = (
            (
                self.urls['admin'],
                self.urls['login'],
                status.HTTP_200_OK,
                self.client,
            ),
            (
                self.urls['login'],
                self.urls['login'],
                status.HTTP_200_OK,
                self.client,
            ),
            (
                self.urls['logout'],
                self.urls['login'],
                status.HTTP_200_OK,
                self.client,
            ),
            (
                self.urls['missing'],
                self.urls['missing'],
                status.HTTP_404_NOT_FOUND,
                self.client,
            ),
        )
        for address, response_url, code, client in response_data:
            response = client.get(address)
            assert response.status_code == code
            assert response.url.path == response_url

    def test_register_in_admin(
        self,
        admin: Dict[str, str],
        user: Dict[str, str],
    ) -> None:
        """URL-адрес перенаправляет на заданную страницу."""
        admin_login_response = self.client.post(
            self.urls['login'],
            data={
                'username': admin['username'],
                'password': admin['password'],
            },
            follow_redirects=True,
        )
        assert admin_login_response.status_code == status.HTTP_200_OK
        assert admin_login_response.url.path == self.urls['admin'] + '/'
        user_login_response = self.client.post(
            self.urls['login'],
            data={
                'username': user['username'],
                'password': user['password'],
            },
            follow_redirects=True,
        )
        assert user_login_response.status_code == status.HTTP_400_BAD_REQUEST
        assert user_login_response.url.path == self.urls['login']
