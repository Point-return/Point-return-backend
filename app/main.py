import logging
from logging.config import dictConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.config import LoggingConfig
from app.core.admin import authentication_backend
from app.database import engine
from app.products.admin import (
    DealerAdmin,
    ParsedProductDealerAdmin,
    ProductAdmin,
    ProductDealerAdmin,
)
from app.products.router import router_products
from app.users.admin import UserAdmin
from app.users.router import router_auth, router_users

dictConfig(LoggingConfig().dict())
logger = logging.getLogger('point_logger')


app = FastAPI(
    title='ProSept',
    version='0.1.0',
)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_products)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["*"],
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(DealerAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductDealerAdmin)
admin.add_view(ParsedProductDealerAdmin)
admin.add_view(UserAdmin)


@app.get('/test')
def index() -> str:
    """Тестовая функция."""
    return 'Hello'
