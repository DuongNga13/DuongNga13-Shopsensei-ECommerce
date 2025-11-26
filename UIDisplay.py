from typing import List, Tuple

class UIDisplay:
    """
    Lớp mô phỏng giao diện trình duyệt.
    Khi người dùng đăng nhập, hệ thống sẽ hiển thị danh sách sản phẩm đề xuất.
    """
    def show_recommendations(self, user: str, products: List[Tuple[str, float]]):
        print(f"===== RECOMMENDATIONS FOR {user.upper()} =====")
        for product, score in products:
            print(f"- {product} (score: {score:.3f})")
        print("==============================================")