class ProductManager:
    def __init__(self, products=None):
        self.products = products if products else []

    def search_products(self, keyword):
        keyword = keyword.lower()
        return [p for p in self.products if keyword in p.name.lower()]

    def get_top_selling(self, n=10):
        return sorted(self.products, key=lambda p: p.sold_count, reverse=True)[:n]

    def get_product_by_id(self, pid):
        for p in self.products:
            if p.id == pid:
                return p
        return None