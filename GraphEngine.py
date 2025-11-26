from typing import Dict, List, Tuple, Set
from collections import defaultdict
from WeightNormalizer import WeightNormalizer


class GraphEngine:    
    def __init__(self, normalizer: WeightNormalizer):
        self.normalizer = normalizer
    
    def build_graph(self, user_interactions: Dict[str, List[Tuple[str, str]]]) -> Dict:
        user_to_products = defaultdict(lambda: defaultdict(float))
        product_to_users = defaultdict(lambda: defaultdict(float))
        all_users = set()
        all_products = set()
        
        print(f"\n{'='*70}")
        print(f"🔨 XÂY DỰNG ĐỒ THỊ (Cộng dồn trọng số)")
        print(f"{'='*70}")
        
        for user, interactions in user_interactions.items():
            all_users.add(user)
            
            product_interaction_count = defaultdict(int)
            for product, _ in interactions:
                product_interaction_count[product] += 1
            
            for product, interaction_type in interactions:
                weight = self.normalizer.get_weight(interaction_type)
                
                user_to_products[user][product] += weight
                product_to_users[product][user] += weight
                
                all_products.add(product)
            
            multi_interaction_products = {
                p: count for p, count in product_interaction_count.items() 
                if count > 1
            }
            
            if multi_interaction_products:
                print(f"\n📊 User '{user}': Phát hiện sản phẩm có nhiều tương tác:")
                for product, count in multi_interaction_products.items():
                    total_weight = user_to_products[user][product]
                    print(f"   - '{product}': {count} tương tác → Tổng điểm: {total_weight:.3f}")
        
        user_to_products = {
            user: dict(products) 
            for user, products in user_to_products.items()
        }
        product_to_users = {
            product: dict(users) 
            for product, users in product_to_users.items()
        }
        
        print(f"\n✅ Đã xây dựng đồ thị:")
        print(f"   👤 Số users: {len(all_users)}")
        print(f"   📦 Số products: {len(all_products)}")
        print(f"   🔗 Số cạnh (user→product): {sum(len(v) for v in user_to_products.values())}")
        
        sample_users = list(all_users)[:3]
        for user in sample_users:
            products = user_to_products.get(user, {})
            print(f"   📊 User '{user}': {len(products)} sản phẩm")
            
            top_products = sorted(products.items(), key=lambda x: x[1], reverse=True)[:3]
            for product, weight in top_products:
                print(f"      → '{product}': {weight:.3f}")
        
        print(f"{'='*70}\n")
        
        return {
            'user_to_products': user_to_products,
            'product_to_users': product_to_users,
            'users': all_users,
            'products': all_products
        }