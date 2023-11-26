from fastapi import FastAPI
from sqladmin import Admin

from app.database import engine
from app.products.admin import (
    DealerAdmin,
    ParsedProductDealerAdmin,
    ProductAdmin,
    ProductDealerAdmin,
)
from app.users.admin import UserAdmin

app = FastAPI(
    title='ProSept',
)
admin = Admin(app, engine)
admin.add_view(DealerAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductDealerAdmin)
admin.add_view(ParsedProductDealerAdmin)
admin.add_view(UserAdmin)


@app.get('/')
def index():
    """Тестовая функция."""
    return 'Hello'
