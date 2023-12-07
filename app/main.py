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
    docs_url='/api/v1/docs',
    openapi_url='/api/v1/openapi.json',
)

app.include_router(router_v1, prefix='/api')
app.include_router(router_auth)
app.include_router(router_users)

origins = [
    'http://localhost:3000',
    'http://localhost:5000',
    'http://localhost:5173',
    'http://localhost:8000',
    'http://81.31.246.3:3000',
    'http://81.31.246.3:5000',
    'http://81.31.246.3:5173',
    'http://81.31.246.3:8000',
    'https://81.31.246.3:3000',
    'https://81.31.246.3:5000',
    'https://81.31.246.3:5173',
    'https://81.31.246.3:8000',
    'http://point-return.sytes.net',
    'https://point-return.sytes.net',
    'http://point-return.github.io',
    'https://point-return.github.io',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=[
        'Content-Type',
        'Set-Cookie',
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Origin',
        'Authorization',
    ],
)

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(DealerAdmin)
admin.add_view(ProductAdmin)
admin.add_view(ProductDealerAdmin)
admin.add_view(ParsedProductDealerAdmin)
admin.add_view(UserAdmin)
admin.add_view(StatisticsAdmin)
