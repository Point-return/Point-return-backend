from sqladmin import ModelView
from app.products.models import Dealer

class DealerAdmin(ModelView, model=Dealer):
    column_list = [Dealer.id, Dealer.name]
