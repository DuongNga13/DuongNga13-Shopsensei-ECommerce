from typing import Dict, Any, List, Tuple, Set

from Order import Order
from CartManager import CartManager

class OrderManager:
    def __init__(self, cart_manager: CartManager, initial_orders: Dict[int, Any] = None): 
        self.orders = initial_orders if initial_orders is not None else {} 
        self.order_id_counter = len(self.orders) + 1
        self.cart_manager = cart_manager

    def checkout(self, user_id: str, products_db: Dict[str, Any]) -> Tuple[bool, str]:
        user_cart = self.cart_manager.get_user_cart(user_id)
        if not user_cart:
            return False, "Giỏ hàng trống. Không thể thanh toán."

        # 1. Kiểm tra tồn kho cuối cùng
        for pid, item in user_cart.items():
            product_obj = products_db.get(pid)
            if product_obj is None:
                 return False, f"Lỗi tồn kho: Sản phẩm {item.name} (ID {pid}) không tồn tại trong hệ thống."
            if product_obj.stock < item.quantity:
                return False, f"Lỗi tồn kho: Sản phẩm {item.name} (ID {pid}) không đủ hàng. Chỉ còn {product_obj.stock} sản phẩm."
        
        # 2. Tạo đơn hàng mới
        items_list: List[Any] = list(user_cart.values())
        new_order = Order(
            order_id=self.order_id_counter,
            user_id=user_id,
            items=items_list
        )

        # 3. Cập nhật tồn kho và số lượng đã bán
        for pid, item in user_cart.items():
            product_obj = products_db[pid]
            product_obj.stock -= item.quantity
            product_obj.sold_count += item.quantity
        
        # 4. Lưu đơn hàng và tăng counter
        self.orders[self.order_id_counter] = new_order
        self.order_id_counter += 1
        
        # 5. Xóa giỏ hàng
        del self.cart_manager.cart[user_id]
        
        return True, f"Thanh toán thành công! Đơn hàng #{new_order.order_id} ({new_order.total_amount:,.0f}đ) đã được tạo."

    def get_user_orders(self, user_id: str) -> List[Order]:
        return [order for order in self.orders.values() if order.user_id == user_id]
    
    def get_purchased_products(self, user_id: str) -> Set[str]:
        """
        Lấy danh sách tên các sản phẩm mà user đã mua
        
        Args:
            user_id: ID của người dùng
            
        Returns:
            Set chứa tên các sản phẩm đã mua (để tra cứu nhanh)
        """
        purchased = set()
        
        # Duyệt qua tất cả đơn hàng của user
        for order in self.orders.values():
            if order.user_id == user_id:
                # Thêm tên các sản phẩm trong đơn hàng vào set
                for item in order.items:
                    purchased.add(item.name)
        
        return purchased