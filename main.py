import os
from typing import Optional
from User import User
from UserManager import UserManager
from ProductManager import ProductManager
from CartManager import CartManager
from OrderManager import OrderManager
from DataAccess import DataAccess
from InteractionTracker import InteractionTracker
from Recommendation import Recommendation
from GraphEngine import GraphEngine
from WeightNormalizer import WeightNormalizer


class ShopUI:   
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def print_header(title):
        print("\n" + "="*70)
        print(f"  {title.center(66)}")
        print("="*70)
    
    @staticmethod
    def print_divider():
        print("-"*70)
    
    @staticmethod
    def wait_enter():
        input("\n[Nhấn Enter để tiếp tục...]")
    
    @staticmethod
    def display_product_list(products):
        print(f"\n{'ID':<8} {'Tên sản phẩm':<32} {'Giá':<15}")
        ShopUI.print_divider()
        for p in products:
            print(f"{p.id:<8} {p.name:<32} {p.price:>12,}đ")
    
    @staticmethod
    def display_recommendations(products_with_scores, product_manager):
        print(f"\n{'#':<4} {'ID':<8} {'Tên sản phẩm':<32} {'Giá':<15} {'Điểm':<8}")
        ShopUI.print_divider()
        
        displayed = 0
        for product_name, score in products_with_scores:
            matching_products = [p for p in product_manager.products if p.name == product_name]
            
            if matching_products:
                product = matching_products[0]
                displayed += 1
                print(f"{displayed:<4} {product.id:<8} {product.name:<32} {product.price:>12,}đ {score:>6.3f}")
            
            if displayed >= 10:
                break


class ShopApp:
    def __init__(self):
        self.data_access = DataAccess()
        users = self.data_access.load_users()
        products = self.data_access.load_products()
        self.user_manager = UserManager(users)
        self.product_manager = ProductManager(products)
        self.cart_manager = CartManager()
        self.order_manager = OrderManager(self.cart_manager)
        self.products_db = {p.id: p for p in products}
        self.current_user: Optional[User] = None
        self.ui = ShopUI()
        self.interaction_tracker = InteractionTracker()
    
    def run(self):
        while True:
            if self.current_user:
                self._show_user_menu()
            else:
                self._show_guest_menu()
    
    def _show_guest_menu(self):
        while not self.current_user:
            self.ui.clear_screen()
            self.ui.print_header("SHOPSENSEI")
            print("\n👤 Chưa đăng nhập")
            print("\n┌─────────────────────────────────────────┐")
            print("│  1. 📝 Đăng ký                          │")
            print("│  2. 🔐 Đăng nhập                        │")
            print("│  3. 📦 Xem sản phẩm                     │")
            print("│  4. 🔍 Tìm kiếm                         │")
            print("│  5. 🏆 Top bán chạy                     │")
            print("│  0. ❌ Thoát                            │")
            print("└─────────────────────────────────────────┘")
            self.ui.print_divider()
            
            choice = input("Chọn: ").strip()
            actions = {
                "1": self._register, "2": self._login, "3": self._view_products,
                "4": self._search_products, "5": self._view_top_selling, "0": self._exit
            }
            
            if choice in actions:
                if actions[choice]():
                    return
            else:
                print("❌ Không hợp lệ!")
                self.ui.wait_enter()
    
    def _show_user_menu(self):
        while self.current_user:
            self.ui.clear_screen()
            self.ui.print_header("SHOP THỜI TRANG")
            print(f"\n👤 Xin chào: {self.current_user.username}")
            print("\n┌─────────────────────────────────────────┐")
            print("│  1. 📦 Xem sản phẩm                     │")
            print("│  2. 🔍 Tìm kiếm                         │")
            print("│  3. 🏆 Top bán chạy                     │")
            print("│  4. 🛒 Giỏ hàng                         │")
            print("│  5. 📋 Đơn hàng                         │")
            print("│  6. ✨ Đề xuất sản phẩm                 │")
            print("│  7. 🔍 Lịch sử tương tác                │")
            print("│  8. 🚪 Đăng xuất                        │")
            print("│  0. ❌ Thoát                            │")
            print("└─────────────────────────────────────────┘")
            self.ui.print_divider()
            
            choice = input("Chọn: ").strip()
            actions = {
                "1": self._view_products, "2": self._search_products, "3": self._view_top_selling,
                "4": self._view_cart, "5": self._view_orders, "6": self._show_recommendations,
                "7": self._interactions, "8": self._logout, "0": self._exit
            }
            
            if choice in actions:
                if actions[choice]():
                    return
            else:
                print("❌ Không hợp lệ!")
                self.ui.wait_enter()
    
    def _register(self):
        self.ui.clear_screen()
        self.ui.print_header("ĐĂNG KÝ")
        username = input("\nTên đăng nhập: ").strip()
        password = input("Mật khẩu: ").strip()
        
        if not username or not password:
            print("❌ Không được để trống!")
        elif user := self.user_manager.register(username, password):
            print(f"✅ Đăng ký thành công! Chào {username}")
            self.data_access.save_users(self.user_manager.users)
        else:
            print(f"❌ Tên '{username}' đã tồn tại!")
        
        self.ui.wait_enter()
    
    def _login(self):
        self.ui.clear_screen()
        self.ui.print_header("ĐĂNG NHẬP")
        username = input("\nTên đăng nhập: ").strip()
        password = input("Mật khẩu: ").strip()
        
        if user := self.user_manager.login(username, password):
            self.current_user = user
            print(f"✅ Đăng nhập thành công!")
        else:
            print("❌ Sai tài khoản hoặc mật khẩu!")
        
        self.ui.wait_enter()
    
    def _logout(self):
        print(f"👋 Đăng xuất {self.current_user.username}")
        self.current_user = None
        self.ui.wait_enter()
    
    def _view_products(self):
        self.ui.clear_screen()
        self.ui.print_header("DANH SÁCH SẢN PHẨM")
        
        if not self.product_manager.products:
            print("\n❌ Không có sản phẩm!")
            self.ui.wait_enter()
            return
        
        self.ui.display_product_list(self.product_manager.products)
        
        if self.current_user:
            self.ui.print_divider()
            pid = input("\n🔍 Nhập ID để xem chi tiết (Enter để quay lại): ").strip()
            if pid:
                product = self.product_manager.get_product_by_id(pid)
                if product:
                    self._view_product_detail(product)
        else:
            self.ui.wait_enter()
    
    def _search_products(self):
        self.ui.clear_screen()
        self.ui.print_header("TÌM KIẾM")
        keyword = input("\nTừ khóa: ").strip()
        
        if not keyword:
            print("❌ Nhập từ khóa!")
            self.ui.wait_enter()
            return
        
        results = self.product_manager.search_products(keyword)
        if results:
            print(f"\n🔍 Tìm thấy {len(results)} sản phẩm:")
            self.ui.display_product_list(results)
            
            if self.current_user:
                self.ui.print_divider()
                pid = input("\n🔍 Nhập ID để xem chi tiết (Enter để quay lại): ").strip()
                if pid:
                    product = self.product_manager.get_product_by_id(pid)
                    if product:
                        self._view_product_detail(product)
            else:
                self.ui.wait_enter()
        else:
            print(f"\n❌ Không tìm thấy '{keyword}'")
            self.ui.wait_enter()
    
    def _view_top_selling(self):
        self.ui.clear_screen()
        self.ui.print_header("🏆 TOP 10 SẢN PHẨM BÁN CHẠY NHẤT")
        top = self.product_manager.get_top_selling(10)
        
        if top:
            self.ui.display_product_list(top)
            
            if self.current_user:
                self.ui.print_divider()
                pid = input("\n🔍 Nhập ID để xem chi tiết (Enter để quay lại): ").strip()
                if pid:
                    product = self.product_manager.get_product_by_id(pid)
                    if product:
                        self._view_product_detail(product)
            else:
                self.ui.wait_enter()
        else:
            print("\n❌ Không có dữ liệu!")
            self.ui.wait_enter()
    
    def _add_to_cart(self, product_id):
        product = self.product_manager.get_product_by_id(product_id)
        if not product:
            print(f"\n❌ Không tìm thấy sản phẩm với ID: {product_id}")
            self.ui.wait_enter()
            return
        
        print(f"\n📦 {product.name}")
        print(f"💰 Giá: {product.price:,}đ")
        print(f"📊 Tồn kho: {product.stock} sản phẩm")
        self.ui.print_divider()
        
        try:
            quantity = int(input("Số lượng: ").strip())
        except ValueError:
            print("❌ Số lượng không hợp lệ!")
            self.ui.wait_enter()
            return
        
        product_data = {'id': product.id, 'name': product.name, 'price': product.price, 'stock': product.stock}
        success, message = self.cart_manager.add_to_cart(self.current_user.username, product_data, quantity)
        
        if success:
            self.interaction_tracker.track_cart(self.current_user.username, product)
        
        print(f"\n{'✅' if success else '❌'} {message}")
        self.ui.wait_enter()
    
    def _view_product_detail(self, product):
        self.interaction_tracker.track_view(self.current_user.username, product)
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("CHI TIẾT SẢN PHẨM")
            
            print(f"\n{'='*70}")
            print(f"  📦 ID: {product.id}")
            print(f"  🏷️  Tên: {product.name}")
            print(f"  📂 Danh mục: {product.category}")
            print(f"  💰 Giá: {product.price:,}đ")
            print(f"  📊 Tồn kho: {product.stock} sản phẩm")
            print(f"  📏 Sizes: {product.sizes}")
            print(f"  🎨 Màu sắc: {product.colors}")
            print(f"  🔥 Đã bán: {product.sold_count} sản phẩm")
            print(f"{'='*70}")
            
            print("\n┌─────────────────────────────────────────┐")
            print("│  1. 🛒 Thêm vào giỏ hàng               │")
            print("│  2. ❤️  Thích sản phẩm                  │")
            print("│  3. ⏭️  Bỏ qua sản phẩm                 │")
            print("└─────────────────────────────────────────┘")
            
            choice = input("\nChọn (Enter để quay lại menu chính): ").strip()
            
            if choice == "1":
                try:
                    quantity = int(input("\nSố lượng: ").strip())
                    product_data = {
                        'id': product.id, 
                        'name': product.name, 
                        'price': product.price, 
                        'stock': product.stock
                    }
                    success, message = self.cart_manager.add_to_cart(
                        self.current_user.username, 
                        product_data, 
                        quantity
                    )
                    
                    if success:
                        self.interaction_tracker.track_cart(self.current_user.username, product)
                    
                    print(f"\n{'✅' if success else '❌'} {message}")
                    self.ui.wait_enter()
                except ValueError:
                    print("\n❌ Số lượng không hợp lệ!")
                    self.ui.wait_enter()
            
            elif choice == "2":
                self.interaction_tracker.track_like(self.current_user.username, product)
                print("\n✅ ❤️ Đã thích sản phẩm!")
                self.ui.wait_enter()
            
            elif choice == "3":
                self.interaction_tracker.track_skip(self.current_user.username, product)
                print("\n✅ ⏭️ Đã bỏ qua sản phẩm!")
                self.ui.wait_enter()
                break
            
            else:
                break 
    
    def _view_cart(self):
        self.ui.clear_screen()
        self.ui.print_header("GIỎ HÀNG")
        cart = self.cart_manager.get_user_cart(self.current_user.username)
        
        if not cart:
            print("\n🛒 Giỏ hàng trống!")
            self.ui.wait_enter()
            return
        
        print(f"\n{'ID':<8} {'Tên':<30} {'Giá':<15} {'SL':<5} {'Tổng':<15}")
        self.ui.print_divider()
        total = 0
        for item in cart.values():
            subtotal = item.calculate_subtotal()
            total += subtotal
            print(f"{item.product_id:<8} {item.name:<30} {item.unit_price:>12,}đ {item.quantity:>3} {subtotal:>12,}đ")
        
        self.ui.print_divider()
        print(f"{'TỔNG CỘNG:':<54} {total:>12,}đ")
        print("\n1. Thanh toán\n2. Xóa sản phẩm\n0. Quay lại")
        
        choice = input("\nChọn: ").strip()
        if choice == "1":
            self._checkout()
        elif choice == "2":
            pid = input("ID cần xóa: ").strip()
            success, msg = self.cart_manager.remove_from_cart(self.current_user.username, pid)
            print(f"{'✅' if success else '❌'} {msg}")
            self.ui.wait_enter()
    
    def _checkout(self):
        cart = self.cart_manager.get_user_cart(self.current_user.username)
        
        purchased_items = []
        for item in cart.values():
            product = self.product_manager.get_product_by_id(item.product_id)
            if product:
                purchased_items.append(product)
        
        success, message = self.order_manager.checkout(self.current_user.username, self.products_db)
        
        if success:
            for product in purchased_items:
                self.interaction_tracker.track_purchase(self.current_user.username, product)
            self.data_access.save_products(self.product_manager.products)
        
        print(f"\n{'✅' if success else '❌'} {message}")
        self.ui.wait_enter()
    
    def _view_orders(self):
        self.ui.clear_screen()
        self.ui.print_header("ĐƠN HÀNG")
        orders = self.order_manager.get_user_orders(self.current_user.username)
        
        if not orders:
            print("\n📋 Chưa có đơn hàng!")
        else:
            print(f"\n🛍️ Bạn có {len(orders)} đơn hàng:")
            self.ui.print_divider()
            for order in orders:
                print(f"\n{order.view_details()}")
                self.ui.print_divider()
        
        self.ui.wait_enter()

    def _show_recommendations(self):
        self.ui.clear_screen()
        self.ui.print_header("✨ ĐỀ XUẤT SẢN PHẨM THÔNG MINH")
        
        all_interactions = self.interaction_tracker.get_all_interactions_for_recommendation()
        
        user_interactions = all_interactions.get(self.current_user.username, [])
        
        if not user_interactions:
            top_products = self.product_manager.get_top_selling(10)
            self.ui.display_product_list(top_products)
            
            self.ui.print_divider()
            pid = input("\n🔍 Nhập ID để xem chi tiết (Enter để quay lại): ").strip()
            if pid:
                product = self.product_manager.get_product_by_id(pid)
                if product:
                    self._view_product_detail(product)
            return
        
        purchased = self.order_manager.get_purchased_products(self.current_user.username)
        
        normalizer = WeightNormalizer()
        graph_engine = GraphEngine(normalizer)
        graph_data = graph_engine.build_graph(all_interactions)
        
        # Tạo recommender TỐI ƯU
        recommender = Recommendation(graph_data, self.product_manager)
        
        # Lấy đề xuất với TAG nguồn gốc
        recommendations = recommender.get_recommendations(
            username=self.current_user.username,
            top_n=10,
            purchased_products=purchased
        )
        
        if not recommendations:
            print(f"\n❌ Không tìm thấy đề xuất phù hợp")
            print(f"💡 Hãy xem thêm sản phẩm để hệ thống hiểu bạn hơn!")
            self.ui.wait_enter()
            return
        
        # ========================================
        # HIỂN THỊ KẾT QUẢ DƯỚNG DẠNG BẢNG
        # ========================================
        print(f"\n{'='*70}")
        print(f"✨ TOP {len(recommendations)} ĐỀ XUẤT THÔNG MINH")
        print(f"{'='*70}")
        
        # Cấu hình bảng
        HEADER = f"{'#':<4} {'Tên sản phẩm':<32} {'Giá':>15} {'Điểm':>8} {'Nguồn':<10}"
        self.ui.print_divider() 
        print(HEADER)
        self.ui.print_divider()

        # Biểu tượng và Mô tả nguồn 
        SOURCE_MAP = {
            "WARM": ("🔥", "WARM"),
            "COLLAB": ("🤝", "COLLAB"),
            "CONTENT": ("📂", "CONTENT"),
            "POPULAR": ("⭐", "POPULAR"),
        }
        
        # Duyệt và hiển thị
        for rank, (product_name, score, tag) in enumerate(recommendations, 1):
            matching = [p for p in self.product_manager.products if p.name == product_name]
            if matching:
                p = matching[0]
                icon, label = SOURCE_MAP.get(tag, ('?', 'UNKNOWN'))
                
                # Định dạng
                rank_str = f"#{rank}"
                price_str = f"{p.price:,.0f}đ"
                score_str = f"{score:.3f}"
                source_str = f"{icon} {label}"
                
                # In ra dòng bảng
                print(
                    f"{rank_str:<4} "
                    f"{p.name:<32} "
                    f"{price_str:>15} "
                    f"{score_str:>8} "
                    f"{source_str:<10}"
                )

        print(f"{'='*70}")

        # Phân loại theo tag (để phục vụ phần thống kê tiếp theo)
        warm_items = [(p, s, t) for p, s, t in recommendations if t == "WARM"]
        collab_items = [(p, s, t) for p, s, t in recommendations if t == "COLLAB"]
        content_items = [(p, s, t) for p, s, t in recommendations if t == "CONTENT"]
        popular_items = [(p, s, t) for p, s, t in recommendations if t == "POPULAR"]
        
        # Thống kê nguồn gốc TỐI ƯU (giữ nguyên logic gốc)
        print(f"\n📊 Phân tích nguồn đề xuất (Theo chiến lược 3 tầng):")
        print(f"  1. 🔥 WARM Products (1-3): {len(warm_items)} sản phẩm (Conversion 15-40%)")
        print(f"  2. 🤝 COLLABORATIVE (4-7): {len(collab_items)} sản phẩm (Conversion 8-15%)")
        print(f"  3. 💡 DISCOVERY (8-10): {len(content_items) + len(popular_items)} sản phẩm (Conversion 3-8%)")
        
        # Tùy chọn xem giải thích
        self.ui.print_divider()
        choice = input("\n❓ Xem giải thích chi tiết cho sản phẩm #1? (y/n): ").strip().lower()
        if choice == 'y' and recommendations:
            product_name = recommendations[0][0]
            explanation = recommender.explain_recommendation(
                self.current_user.username,
                product_name
            )
            print(explanation)
            self.ui.wait_enter()
        
        # Xem chi tiết sản phẩm
        self.ui.print_divider()
        rank_input = input("\n🔍 Nhập SỐ THỨ TỰ (#1, #2...) để xem chi tiết (Enter để quay lại): ").strip()
        
        if rank_input:
            try:
                # Xử lý input có dấu # hoặc không
                rank = int(rank_input.replace('#', ''))
                if 1 <= rank <= len(recommendations):
                    product_name = recommendations[rank - 1][0]
                    product = None
                    for p in self.product_manager.products:
                        if p.name == product_name:
                            product = p
                            break
                    
                    if product:
                        self._view_product_detail(product)
                else:
                    print(f"❌ Số thứ tự không hợp lệ (1-{len(recommendations)})")
                    self.ui.wait_enter()
            except ValueError:
                print("❌ Vui lòng nhập số!")
                self.ui.wait_enter()

    def _interactions(self):
        self.ui.clear_screen()
        self.ui.print_header("🔍 LỊCH SỬ TƯƠNG TÁC")
        
        self.interaction_tracker._print_interactions(self.current_user.username)
        
        print("\n📋 Sản phẩm đã mua:")
        purchased = self.order_manager.get_purchased_products(self.current_user.username)
        if purchased:
            for i, product in enumerate(purchased, 1):
                print(f"{i}. {product}")
        else:
            print("Chưa mua sản phẩm nào!")
        
        self.ui.wait_enter()
    
    def _exit(self):
        self.ui.clear_screen()
        print("\n" + "="*70)
        print("  CẢM ƠN! HẸN GẶP LẠI 👋".center(70))
        print("="*70 + "\n")
        return True


def main():
    try:
        app = ShopApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n❌ Đã dừng!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()