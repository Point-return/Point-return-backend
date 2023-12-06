import os

from app.config import CSVFilenames

os.environ['MODE'] = 'TEST'

CSVFilenames.products = 'test_products'
CSVFilenames.dealers = 'test_dealers'
CSVFilenames.parsed_data = 'test_dealerprice'
CSVFilenames.product_dealer = 'test_productdealer'
CSVFilenames.users = 'test_users'
