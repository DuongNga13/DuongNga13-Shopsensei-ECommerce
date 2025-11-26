class OrderItem:
    def __init__(self, product_id: int, name: str, unit_price: int, quantity: int):
        self.product_id = product_id
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        
    def calculate_subtotal(self) -> int:
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.name} x {self.quantity} (Giá: {self.unit_price:,.3f}đ)"