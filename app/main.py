from fastapi import FastAPI
from sqladmin import Admin

from app.database import engine
from app.products.admin import (
    DealerAdmin,
    ParsedProductDealerAdmin,
    ProductAdmin,
    ProductDealerAdmin,
)
from app.products.router import router_products
from app.users.admin import UserAdmin
from app.users.router import router_user

app = FastAPI(
    title='ProSept',
)

app.include_router(router_user)
app.include_router(router_products)

admin = Admin(app, engine)
admin.add_view(DealerAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductDealerAdmin)
admin.add_view(ParsedProductDealerAdmin)
admin.add_view(UserAdmin)


@app.get('/')
def index() -> str:
    """Тестовая функция."""
    return 'Hello'
