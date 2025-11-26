class WeightNormalizer:
    def __init__(self):
        # Mapping: interaction_type -> (min_weight, max_weight)
        self._normalized_weight = {
            "purchase": (0.95, 1.0),   # Mua = quan tâm cao nhất
            "cart": (0.70, 0.85),       # Thêm vào giỏ = quan tâm cao
            "like": (0.50, 0.65),       # Thích = quan tâm trung bình
            "view": (0.30, 0.45),       # Xem = quan tâm thấp
            "skip": (0.00, 0.15)         # Bỏ qua = không quan tâm
        }

    def get_weight(self, interaction_type: str) -> float:
        if interaction_type not in self._normalized_weight:
            return 0.0
        
        low, high = self._normalized_weight[interaction_type]
        return (low + high) / 2
    
    def get_all_weights(self) -> dict:
        return {
            itype: self.get_weight(itype) 
            for itype in self._normalized_weight.keys()
        }