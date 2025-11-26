class Product:
    def __init__(self, pid, name, category, price, stock, sizes, colors, sold_count=0):
        self.id = pid
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.sizes = sizes
        self.colors = colors
        self.sold_count = sold_count