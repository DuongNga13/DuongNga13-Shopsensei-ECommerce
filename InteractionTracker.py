from typing import Dict, List, Tuple, Optional
import json
import os

class InteractionTracker:
    INTERACTION_FILE = "user_interactions.json"
    
    def __init__(self):
        self.interactions: Dict[str, List[Tuple[str, str, int, str, str]]] = {}
        self.load_interactions()
    
    def load_interactions(self):
        # Đọc dữ liệu tương tác từ file
        try:
            if os.path.exists(self.INTERACTION_FILE):
                with open(self.INTERACTION_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    self.interactions = {}
                    for user, items in data.items():
                        self.interactions[user] = []
                        for item in items:
                            if len(item) == 2:
                                self.interactions[user].append((
                                    "UNKNOWN", 
                                    item[0],    
                                    0,         
                                    "Unknown",  
                                    item[1]     
                                ))
                            elif len(item) >= 5:
                                self.interactions[user].append(tuple(item[:5]))
                            else:
                                continue
                
                print(f"✅ Đã load {len(self.interactions)} user interactions từ file")
        except Exception as e:
            print(f"⚠️ Không thể đọc file tương tác: {e}")
            self.interactions = {}
    
    def save_interactions(self):
        try:
            data_to_save = {}
            for user, items in self.interactions.items():
                data_to_save[user] = [
                    [pid, name, price, category, itype]
                    for pid, name, price, category, itype in items
                ]
            
            with open(self.INTERACTION_FILE, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            print(f"⚠️ Không thể lưu file tương tác: {e}")
    
    def add_interaction(
        self, 
        username: str, 
        product_id: str,
        product_name: str, 
        price: int,
        category: str,
        interaction_type: str
    ):
        if username not in self.interactions:
            self.interactions[username] = []
        
        existing_same_type = None
        for i, (pid, pname, p, cat, itype) in enumerate(self.interactions[username]):
            if pid == product_id and itype == interaction_type:
                existing_same_type = i
                break
        
        if existing_same_type is not None:
            #xoá tương tác cũ
            self.interactions[username].pop(existing_same_type)
            print(f"🔄 Cập nhật: {product_name} (ID: {product_id}) - {interaction_type}")
        else:
            #Thêm tương tác mới
            print(f"➕ Thêm mới: {product_name} (ID: {product_id}) - {interaction_type}")
        
        # Thêm tương tác mới vào đầu
        self.interactions[username].insert(0, (
            product_id,
            product_name,
            price,
            category,
            interaction_type
        ))
        
        # Giới hạn số lượng tương tác
        if len(self.interactions[username]) > 100:
            self.interactions[username] = self.interactions[username][:100]
        
        self.save_interactions()
    
    def get_user_interactions(self, username: str) -> List[Tuple[str, str, int, str, str]]:
        self.load_interactions()
        return self.interactions.get(username, [])
    
    def get_all_interactions(self) -> Dict[str, List[Tuple[str, str, int, str, str]]]:
        self.load_interactions()
        return self.interactions
    
    def get_interactions_for_recommendation(self, username: str) -> List[Tuple[str, str]]:
        self.load_interactions()
        if username not in self.interactions:
            return []
        
        return [(name, itype) for _, name, _, _, itype in self.interactions[username]]
    
    def get_all_interactions_for_recommendation(self) -> Dict[str, List[Tuple[str, str]]]:
        self.load_interactions()
        result = {}
        for username, interactions in self.interactions.items():
            result[username] = [(name, itype) for _, name, _, _, itype in interactions]
        return result
    
    def track_view(self, username: str, product):
        self.add_interaction(
            username, 
            product.id, 
            product.name, 
            product.price, 
            product.category, 
            "view"
        )
    
    def track_cart(self, username: str, product):
        self.add_interaction(
            username,
            product.id,
            product.name,
            product.price,
            product.category,
            "cart"
        )
    
    def track_purchase(self, username: str, product):
        self.add_interaction(
            username,
            product.id,
            product.name,
            product.price,
            product.category,
            "purchase"
        )
    
    def track_like(self, username: str, product):
        self.add_interaction(
            username,
            product.id,
            product.name,
            product.price,
            product.category,
            "like"
        )
    
    def track_skip(self, username: str, product):
        self.add_interaction(
            username,
            product.id,
            product.name,
            product.price,
            product.category,
            "skip"
        )
    
    def _print_interactions(self, username: str):
        print(f"\n{'='*90}")
        print(f"🔍 LỊCH SỬ TƯƠNG TÁC CỦA: {username}")
        print(f"{'='*90}")
        
        self.load_interactions()
        
        if username in self.interactions and self.interactions[username]:
            print(f"\nTổng số tương tác: {len(self.interactions[username])}\n")
            print(f"{'#':<4} {'ID':<8} {'Tên sản phẩm':<30} {'Giá':<15} {'Loại':<12} {'Danh mục':<15}")
            print("-"*90)
            
            for i, (pid, name, price, category, itype) in enumerate(self.interactions[username], 1):
                icon = {
                    "purchase": " 🛒 ",
                    "cart": " 🛍️ ",
                    "like": " ❤️ ",
                    "view": " 👁️ ",
                    "skip": " ⏭️ "
                }.get(itype, " ❓ ")
                
                display_name = name if len(name) <= 28 else name[:27] + "…"
                
                print(f"{i:<4} {pid:<8} {display_name:<30} {price:>12,}đ {icon} {itype:<10} {category:<15}")
        else:
            print("\n❌ Chưa có tương tác nào!")
        
        print(f"{'='*90}\n")