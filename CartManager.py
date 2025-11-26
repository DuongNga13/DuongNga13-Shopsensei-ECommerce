from typing import Dict, Any, Tuple
from OrderItem import OrderItem

class CartManager:
    def __init__(self):
        self.cart: Dict[str, Dict[int, Any]] = {}

    def get_user_cart(self, user_id: str) -> Dict[int, Any]:
        if user_id not in self.cart:
            self.cart[user_id] = {}
        return self.cart[user_id]

    def add_to_cart(self, user_id: str, product_data: Dict[str, Any], quantity: int) -> Tuple[bool, str]:
        pid = product_data['id']
        current_cart = self.get_user_cart(user_id)
        
        if quantity <= 0:
            return False, "Số lượng phải lớn hơn 0."
        if quantity > product_data.get('stock', 0):
            return False, f"Không đủ hàng tồn kho. Chỉ còn {product_data['stock']} sản phẩm."

        if pid in current_cart:
            current_cart[pid].quantity += quantity
        else:
            item = OrderItem(
                product_id=pid,
                name=product_data['name'],
                unit_price=product_data['price'],
                quantity=quantity
            )
            current_cart[pid] = item

        return True, f"Đã thêm {quantity} x {product_data['name']} vào giỏ hàng."

    def remove_from_cart(self, user_id: str, product_id: int) -> Tuple[bool, str]:
        current_cart = self.get_user_cart(user_id)
        if product_id in current_cart:
            del current_cart[product_id]
            return True, f"Đã xóa sản phẩm ID {product_id} khỏi giỏ hàng."
        return False, "Sản phẩm không có trong giỏ hàng."