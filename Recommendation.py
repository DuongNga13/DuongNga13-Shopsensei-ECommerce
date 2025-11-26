from typing import Dict, List, Tuple, Set, Optional
from collections import defaultdict
import random


class Recommendation:
    """
    HỆ THỐNG ĐỀ XUẤT TỐI ƯU - Phiên bản cuối cùng
    
    CHIẾN LƯỢC 3 TẦNG:
    1. WARM Products (1-3): Sản phẩm đã tương tác - chưa mua (Conversion 15-40%)
    2. COLLABORATIVE (4-7): Từ users tương tự (Conversion 8-15%)
    3. DISCOVERY (8-10): Content-Based + Popularity (Conversion 3-8%)
    
    CẢI TIẾN:
    - ✅ Đề xuất lại sản phẩm đã view/like/cart (chỉ loại đã mua)
    - ✅ Boost điểm cho sản phẩm WARM
    - ✅ Scoring thông minh (category + popularity + price similarity)
    - ✅ KHÔNG random - sắp xếp theo chất lượng
    - ✅ Phân tầng rõ ràng với tag nguồn gốc
    """
    
    def __init__(self, graph_data: Dict, product_manager):
        self.user_to_products = graph_data['user_to_products']
        self.product_to_users = graph_data['product_to_users']
        self.all_users = graph_data['users']
        self.all_products = graph_data['products']
        self.product_manager = product_manager
        
        # Tham số tối ưu
        self.WARM_BOOST = 1.5           # Boost 50% cho sản phẩm đã tương tác
        self.CATEGORY_WEIGHT = 0.6      # 60% từ category score
        self.POPULARITY_WEIGHT = 0.3    # 30% từ popularity
        self.PRICE_SIMILARITY_WEIGHT = 0.1  # 10% từ price similarity
        
        print(f"✅ Recommendation TỐI ƯU khởi tạo:")
        print(f"   - {len(self.all_users)} users")
        print(f"   - {len(self.all_products)} products trong đồ thị")
        print(f"   - {len(self.product_manager.products)} products trong database")
    
    def get_recommendations(
        self,
        username: str,
        top_n: int = 10,
        purchased_products: Optional[Set[str]] = None
    ) -> List[Tuple[str, float, str]]:
        """
        Lấy đề xuất TỐI ƯU với phân tầng rõ ràng
        
        Returns:
            List[(product_name, score, source_tag)]
            source_tag: "WARM" | "COLLAB" | "CONTENT" | "POPULAR"
        """
        if purchased_products is None:
            purchased_products = set()
        
        print(f"\n{'='*70}")
        print(f"🎯 ĐỀ XUẤT TỐI ƯU CHO USER: {username}")
        print(f"{'='*70}")
        
        # Kiểm tra user
        if username not in self.user_to_products:
            print(f"⚠️ User mới → Dùng Popularity")
            results = self._get_popularity_recommendations(top_n, purchased_products)
            return [(p, s, "POPULAR") for p, s in results]
        
        # ========================================
        # TẦNG 1: WARM Products (Đã tương tác - Chưa mua)
        # ========================================
        print(f"\n🔹 TẦNG 1: WARM Products (Đã tương tác - Chưa mua)")
        warm_results = self._get_warm_recommendations(username, purchased_products)
        print(f"   ✅ {len(warm_results)} sản phẩm WARM")
        
        used_products = {p for p, _, _ in warm_results}
        
        # ========================================
        # TẦNG 2: Collaborative Filtering
        # ========================================
        print(f"\n🔹 TẦNG 2: Collaborative Filtering")
        collab_results = self._collaborative_filtering_optimized(
            username, 
            purchased_products | used_products
        )
        print(f"   ✅ {len(collab_results)} sản phẩm từ Collaborative")
        
        used_products.update(p for p, _, _ in collab_results)
        
        # ========================================
        # TẦNG 3: Discovery (Content + Popularity)
        # ========================================
        print(f"\n🔹 TẦNG 3: Discovery (Content-Based + Popularity)")
        discovery_results = self._get_discovery_recommendations(
            username,
            purchased_products | used_products
        )
        print(f"   ✅ {len(discovery_results)} sản phẩm khám phá")
        
        # ========================================
        # Kết hợp và cân bằng
        # ========================================
        final_results = self._balance_recommendations(
            warm_results,
            collab_results,
            discovery_results,
            top_n
        )
        
        print(f"\n✅ TỔNG: {len(final_results)} sản phẩm đề xuất")
        print(f"   - WARM: {sum(1 for _, _, t in final_results if t == 'WARM')}")
        print(f"   - COLLAB: {sum(1 for _, _, t in final_results if t == 'COLLAB')}")
        print(f"   - CONTENT: {sum(1 for _, _, t in final_results if t == 'CONTENT')}")
        print(f"   - POPULAR: {sum(1 for _, _, t in final_results if t == 'POPULAR')}")
        print(f"{'='*70}\n")
        
        return final_results
    
    def _get_warm_recommendations(
        self,
        username: str,
        exclude: Set[str]
    ) -> List[Tuple[str, float, str]]:
        """
        TẦNG 1: Sản phẩm WARM (Đã tương tác - Chưa mua)
        
        Ưu tiên:
        - Cart (0.775) → Conversion rate 40%
        - Like (0.575) → Conversion rate 15%
        - View (0.375) → Conversion rate 8%
        
        Boost điểm 50% để ưu tiên cao
        """
        user_products = self.user_to_products[username]
        
        warm_products = []
        for product, weight in user_products.items():
            # Chỉ loại sản phẩm ĐÃ MUA (không loại view/like/cart)
            if product not in exclude:
                # BOOST điểm 50%
                boosted_score = weight * self.WARM_BOOST
                warm_products.append((product, boosted_score, "WARM"))
        
        # Sắp xếp theo điểm (cao → thấp)
        warm_products.sort(key=lambda x: x[1], reverse=True)
        
        return warm_products[:3]  # Chỉ lấy top 3
    
    def _collaborative_filtering_optimized(
        self,
        username: str,
        exclude: Set[str]
    ) -> List[Tuple[str, float, str]]:
        """
        TẦNG 2: Collaborative Filtering có tối ưu
        
        Cải tiến:
        - Tính user confidence (users mua nhiều → đáng tin hơn)
        - Tính nhiều con đường
        """
        user_products = self.user_to_products[username]
        candidate_scores = defaultdict(float)
        similar_users = set()
        
        # Duyệt qua các sản phẩm user đã tương tác
        for product_a, weight_ua in user_products.items():
            if product_a not in self.product_to_users:
                continue
            
            other_users = self.product_to_users[product_a]
            
            for other_user, weight_other in other_users.items():
                if other_user == username:
                    continue
                
                similar_users.add(other_user)
                
                # Tính similarity
                similarity = min(weight_ua, weight_other)
                
                # Tính user confidence (users mua nhiều → tin hơn)
                user_confidence = self._get_user_confidence(other_user)
                
                # Lấy sản phẩm của other_user
                if other_user not in self.user_to_products:
                    continue
                
                other_user_products = self.user_to_products[other_user]
                
                for product_b, weight_b in other_user_products.items():
                    if product_b in exclude:
                        continue
                    
                    # Tính điểm CÓ user confidence
                    score = similarity * weight_b * user_confidence
                    candidate_scores[product_b] += score
        
        if similar_users:
            print(f"   👥 {len(similar_users)} users tương tự")
        
        # Sắp xếp
        sorted_candidates = sorted(
            candidate_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [(p, s, "COLLAB") for p, s in sorted_candidates[:5]]  # Top 5
    
    def _get_user_confidence(self, username: str) -> float:
        """
        Tính độ tin cậy của user
        
        Users mua nhiều → đề xuất đáng tin hơn
        Users chỉ view → ít tin hơn
        """
        if username not in self.user_to_products:
            return 1.0
        
        user_products = self.user_to_products[username]
        
        # Đếm số lượng purchase
        purchase_count = 0
        for product, weight in user_products.items():
            if weight >= 0.9:  # Purchase weight ≈ 0.975
                purchase_count += 1
        
        # Tính confidence
        if purchase_count >= 5:
            return 1.5  # Heavy buyer: +50%
        elif purchase_count >= 2:
            return 1.2  # Regular buyer: +20%
        else:
            return 1.0  # Window shopper: normal
    
    def _get_discovery_recommendations(
        self,
        username: str,
        exclude: Set[str]
    ) -> List[Tuple[str, float, str]]:
        """
        TẦNG 3: Discovery (Content-Based + Popularity)
        
        Ưu tiên Content-Based, fallback sang Popularity
        """
        # Thử Content-Based trước
        content_results = self._content_based_filtering_optimized(username, exclude)
        
        if len(content_results) >= 3:
            return content_results[:3]
        
        # Nếu không đủ, thêm Popularity
        popularity_results = self._get_popularity_recommendations(5, exclude)
        popularity_tagged = [(p, s, "POPULAR") for p, s in popularity_results]
        
        # Kết hợp
        combined = content_results + popularity_tagged
        
        # Loại trùng
        seen = set()
        unique = []
        for p, s, t in combined:
            if p not in seen:
                seen.add(p)
                unique.append((p, s, t))
        
        return unique[:3]
    
    def _content_based_filtering_optimized(
        self,
        username: str,
        exclude: Set[str]
    ) -> List[Tuple[str, float, str]]:
        """
        Content-Based CẢI TIẾN:
        
        KHÔNG random - Tính điểm kết hợp:
        1. Category score (60%)
        2. Popularity score (30%)
        3. Price similarity (10%)
        """
        user_products = self.user_to_products[username]
        
        # Đếm category
        category_scores = defaultdict(float)
        for product_name, weight in user_products.items():
            product_obj = self._find_product_by_name(product_name)
            if product_obj:
                category_scores[product_obj.category] += weight
        
        if not category_scores:
            return []
        
        # Top categories
        top_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]  # Chỉ lấy 2 category ưa thích nhất
        
        print(f"   📂 Top categories: {[cat for cat, _ in top_categories]}")
        
        # Tính giá trung bình user quan tâm
        avg_price = self._get_user_avg_price(username)
        
        recommendations = []
        
        for category, cat_score in top_categories:
            # Lấy sản phẩm cùng category
            category_products = [
                p for p in self.product_manager.products
                if p.category == category and p.name not in exclude
            ]
            
            # TÍNH ĐIỂM KẾT HỢP (KHÔNG random!)
            scored_products = []
            for product in category_products:
                # 1. Category score (60%)
                base_score = cat_score * self.CATEGORY_WEIGHT
                
                # 2. Popularity score (30%)
                # Normalize: 500 sold = max
                popularity = min(1.0, product.sold_count / 500)
                popularity_score = popularity * self.POPULARITY_WEIGHT
                
                # 3. Price similarity (10%)
                if avg_price > 0:
                    price_diff = abs(product.price - avg_price) / avg_price
                    price_similarity = 1 - min(1.0, price_diff)
                else:
                    price_similarity = 0.5
                
                price_score = price_similarity * self.PRICE_SIMILARITY_WEIGHT
                
                # Tổng điểm
                final_score = base_score + popularity_score + price_score
                scored_products.append((product, final_score))
            
            # SẮP XẾP theo điểm (KHÔNG random!)
            scored_products.sort(key=lambda x: x[1], reverse=True)
            
            # Lấy top 5 mỗi category
            for product, score in scored_products[:5]:
                recommendations.append((product.name, score, "CONTENT"))
        
        # Sắp xếp tổng thể
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def _get_user_avg_price(self, username: str) -> float:
        """Tính giá trung bình sản phẩm user quan tâm"""
        user_products = self.user_to_products.get(username, {})
        if not user_products:
            return 500000  # Default
        
        prices = []
        for product_name in user_products.keys():
            product = self._find_product_by_name(product_name)
            if product:
                prices.append(product.price)
        
        return sum(prices) / len(prices) if prices else 500000
    
    def _get_popularity_recommendations(
        self,
        top_n: int,
        exclude: Set[str]
    ) -> List[Tuple[str, float]]:
        """Popularity-Based fallback"""
        top_selling = self.product_manager.get_top_selling(50)
        
        recommendations = []
        for product in top_selling:
            if product.name not in exclude:
                score = min(0.3, product.sold_count / 2000)
                recommendations.append((product.name, score))
        
        return recommendations[:top_n]
    
    def _balance_recommendations(
        self,
        warm: List[Tuple[str, float, str]],
        collab: List[Tuple[str, float, str]],
        discovery: List[Tuple[str, float, str]],
        top_n: int
    ) -> List[Tuple[str, float, str]]:
        """
        Cân bằng đề xuất theo chiến lược 3 tầng
        
        Mục tiêu:
        - Vị trí 1-3: WARM (nếu có)
        - Vị trí 4-7: COLLAB (nếu có)
        - Vị trí 8-10: DISCOVERY
        """
        final = []
        
        # TẦNG 1: WARM (tối đa 3)
        final.extend(warm[:3])
        
        # TẦNG 2: COLLAB (tối đa 5, điền đủ top_n nếu thiếu)
        remaining = top_n - len(final)
        if remaining > 0:
            final.extend(collab[:min(5, remaining)])
        
        # TẦNG 3: DISCOVERY (điền cho đủ)
        remaining = top_n - len(final)
        if remaining > 0:
            final.extend(discovery[:remaining])
        
        return final[:top_n]
    
    def _find_product_by_name(self, product_name: str):
        """Tìm product object từ tên"""
        for p in self.product_manager.products:
            if p.name == product_name:
                return p
        return None
    
    def explain_recommendation(self, username: str, product_name: str) -> str:
        """
        Giải thích CẢI TIẾN - Có tag nguồn gốc
        """
        if username not in self.user_to_products:
            return f"❌ User '{username}' chưa có tương tác"
        
        explanation = []
        explanation.append(f"\n{'='*70}")
        explanation.append(f"📊 GIẢI THÍCH: Tại sao đề xuất '{product_name}'?")
        explanation.append(f"{'='*70}\n")
        
        user_products = self.user_to_products[username]
        
        # Kiểm tra WARM
        if product_name in user_products:
            weight = user_products[product_name]
            interaction_type = self._guess_interaction_type(weight)
            explanation.append(f"🔥 WARM Product (Bạn đã tương tác)")
            explanation.append(f"   ✓ Bạn đã {interaction_type} sản phẩm này")
            explanation.append(f"   ✓ Điểm gốc: {weight:.3f}")
            explanation.append(f"   ✓ Điểm sau boost (+50%): {weight * 1.5:.3f}")
            explanation.append(f"   💡 Nhắc nhở: Bạn quan tâm nhưng chưa mua!")
            explanation.append("")
        
        # Kiểm tra Collaborative
        collab_score = 0.0
        collab_paths = []
        
        for product_a, weight_ua in user_products.items():
            if product_a in self.product_to_users:
                other_users = self.product_to_users[product_a]
                
                for other_user, weight_other in other_users.items():
                    if other_user == username:
                        continue
                    
                    similarity = min(weight_ua, weight_other)
                    confidence = self._get_user_confidence(other_user)
                    
                    if other_user in self.user_to_products:
                        other_products = self.user_to_products[other_user]
                        
                        if product_name in other_products:
                            score = similarity * other_products[product_name] * confidence
                            collab_score += score
                            
                            confidence_label = "Heavy buyer" if confidence >= 1.5 else "Regular buyer" if confidence >= 1.2 else "User"
                            
                            collab_paths.append(
                                f"  ✓ {confidence_label} '{other_user}' (tương tự qua '{product_a}') "
                                f"→ '{product_name}' (+{score:.3f})"
                            )
        
        if collab_score > 0:
            explanation.append(f"🤝 Collaborative Score: {collab_score:.3f}")
            for path in collab_paths[:5]:
                explanation.append(path)
            explanation.append("")
        
        # Kiểm tra Content-Based
        product_obj = self._find_product_by_name(product_name)
        if product_obj:
            user_same_category = [
                p for p in user_products.keys()
                if self._find_product_by_name(p) and 
                   self._find_product_by_name(p).category == product_obj.category
            ]
            
            if user_same_category and product_name not in user_products:
                explanation.append(f"📂 Content-Based: Category '{product_obj.category}'")
                explanation.append(f"  ✓ Bạn quan tâm đến {len(user_same_category)} sản phẩm cùng category")
                explanation.append(f"  ✓ Popularity: {product_obj.sold_count} đã bán")
                
                avg_price = self._get_user_avg_price(username)
                price_diff_pct = abs(product_obj.price - avg_price) / avg_price * 100
                explanation.append(f"  ✓ Giá phù hợp: {product_obj.price:,}đ (chênh {price_diff_pct:.0f}% so với sở thích)")
                explanation.append("")
        
        if not collab_score and product_name not in user_products:
            explanation.append("⭐ Sản phẩm phổ biến (Top bán chạy)")
        
        explanation.append(f"{'='*70}")
        
        return "\n".join(explanation)
    
    def _guess_interaction_type(self, weight: float) -> str:
        """Đoán loại tương tác từ weight"""
        if weight >= 0.9:
            return "MUA"
        elif weight >= 0.7:
            return "THÊM VÀO GIỎ"
        elif weight >= 0.5:
            return "THÍCH"
        elif weight >= 0.3:
            return "XEM"
        else:
            return "BỎ QUA"