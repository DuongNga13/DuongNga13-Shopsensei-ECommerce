from typing import List, Any
from datetime import datetime

class Order:
    def __init__(self, order_id: int, user_id: str, items: List[Any]):
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.total_amount = self.calculate_total()
        self.status = "Đang chờ xử lý"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def calculate_total(self) -> int:
        total = sum(item.calculate_subtotal() for item in self.items)
        return total

    def update_status(self, new_status: str):
        valid_statuses = ["Đang chờ xử lý", "Đang xử lý", "Đã giao", "Đã nhận", "Đã hủy"]
        if new_status in valid_statuses:
            self.status = new_status
            return True
        return False

    def view_details(self) -> str:
        details = [
            f"--- Đơn hàng #{self.order_id} (Trạng thái: {self.status}) ---",
            f"Khách hàng: {self.user_id}",
            f"Ngày đặt: {self.created_at}",
            "Mặt hàng:",
        ]
        for item in self.items:
            details.append(f"  - {item}")
        details.append(f"TỔNG CỘNG: {self.total_amount:,.0f}đ")
        return "\n".join(details)