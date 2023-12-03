from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin

from app.api.v1.router import router_v1
from app.core.admin import authentication_backend
from app.database import engine
from app.products.admin import (
    DealerAdmin,
    ParsedProductDealerAdmin,
    ProductAdmin,
    ProductDealerAdmin,
    StatisticsAdmin,
)
from app.users.admin import UserAdmin
from app.users.router import router_auth, router_users

app = FastAPI(
    title='ProSept',
    version='0.1.0',
)

app.include_router(router_v1, prefix='/api')
app.include_router(router_auth)
app.include_router(router_users)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=['*'],
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(DealerAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductDealerAdmin)
admin.add_view(ParsedProductDealerAdmin)
admin.add_view(UserAdmin)
admin.add_view(StatisticsAdmin)


@app.get('/')
def index() -> str:
    """Тестовая функция."""
    return 'Hello'
