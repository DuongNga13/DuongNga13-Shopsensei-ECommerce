import pandas as pd

from User import User
from Product import Product

USER_FILE = "users.xlsx"
PRODUCT_FILE = "shop_products.xlsx"

class DataAccess:
    def load_users(self):
        try:
            df = pd.read_excel(USER_FILE)
            return [User(row['username'], row['password_hash']) for idx, row in df.iterrows()]
        except FileNotFoundError:
            return []

    def save_users(self, users):
        data = [{'username': u.username, 'password_hash': u.password_hash} for u in users]
        df = pd.DataFrame(data)
        df.to_excel(USER_FILE, index=False)

    def load_products(self):
        try:
            df = pd.read_excel(PRODUCT_FILE)
            products = []
            for idx, row in df.iterrows():
                products.append(Product(
                    pid=row['id'],
                    name=row['name'],
                    category=row['category'],
                    price=int(row['price']),
                    stock=int(row['stock']),
                    sizes=row['sizes'],
                    colors=row['colors'],
                    sold_count=int(row['sold_count'])
                ))
            return products
        except FileNotFoundError:
            return []

    def save_products(self, products):
        data = []
        for p in products:
            data.append({
                'id': p.id,
                'name': p.name,
                'category': p.category,
                'price': p.price,
                'stock': p.stock,
                'sizes': p.sizes,
                'colors': p.colors,
                'sold_count': p.sold_count
            })
        df = pd.DataFrame(data)
        df.to_excel(PRODUCT_FILE, index=False)