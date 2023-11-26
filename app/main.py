import uvicorn
from fastapi import FastAPI
from sqladmin import Admin
from app.database import engine
from app.products.admin import DealerAdmin


app = FastAPI(
    title='ProSept',
)
admin = Admin(app, engine)
admin.add_view(DealerAdmin)

@app.get('/')
def index():
    return 'Hello'


def main():
    uvicorn.run(app, host='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
