# 🛍️ ShopSensei - Hệ Thống E-commerce Thông Minh
---

## 📋 Mục Lục

- [Giới Thiệu](#-giới-thiệu)
- [Tính Năng](#-tính-năng)
- [Kiến Trúc Hệ Thống](#-kiến-trúc-hệ-thống)
- [Thuật Toán Đề Xuất](#-thuật-toán-đề-xuất)
- [Cài Đặt](#-cài-đặt)
- [Sử Dụng](#-sử-dụng)
- [Cấu Trúc Dự Án](#-cấu-trúc-dự-án)
- [Demo](#-demo)
- [Đóng Góp](#-đóng-góp)
- [License](#-license)

---

## 🎯 Giới Thiệu

**ShopSensei** là một hệ thống thương mại điện tử được xây dựng bằng Python, tập trung vào việc cung cấp trải nghiệm mua sắm được cá nhân hóa thông qua thuật toán đề xuất sản phẩm thông minh.

### Vấn đề giải quyết

- ❌ **Cold Start Problem**: Người dùng mới không nhận được đề xuất phù hợp
- ❌ **Filter Bubble**: Hệ thống chỉ đề xuất sản phẩm tương tự đã xem
- ❌ **Lack of Diversity**: Thiếu đa dạng trong đề xuất

### Giải pháp

- ✅ **Collaborative Filtering**: Học từ hành vi người dùng tương tự
- ✅ **Content-Based Filtering**: Đề xuất dựa trên category sản phẩm
- ✅ **Hybrid Approach**: Kết hợp nhiều phương pháp cho kết quả tối ưu

---

## ✨ Tính Năng

### 🔐 Quản Lý Người Dùng
- Đăng ký / Đăng nhập với mã hóa mật khẩu (SHA-256)
- Lưu trữ thông tin người dùng an toàn

### 🛒 Mua Sắm
- Xem danh sách sản phẩm với đầy đủ thông tin
- Tìm kiếm sản phẩm theo từ khóa
- Thêm sản phẩm vào giỏ hàng
- Quản lý giỏ hàng (thêm, xóa, cập nhật)
- Thanh toán và tạo đơn hàng
- Xem lịch sử đơn hàng

### 🎯 Đề Xuất Thông Minh
- **Collaborative Filtering**: Đề xuất dựa trên người dùng tương tự
- **Content-Based**: Đề xuất theo danh mục sản phẩm
- **Popularity-Based**: Đề xuất top bán chạy (fallback)
- Giải thích chi tiết lý do đề xuất

### 📊 Theo Dõi Tương Tác
- Lưu lịch sử xem sản phẩm
- Theo dõi sản phẩm yêu thích
- Ghi nhận hành vi thêm vào giỏ
- Lưu trữ lịch sử mua hàng

---

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────┐
│                      USER INTERFACE                      │
│                      (main.py)                           │
└─────────────────┬───────────────────────────────────────┘
                  │
    ┌─────────────┴─────────────────────────────────┐
    │                                                │
┌───▼────────────┐                         ┌────────▼────────┐
│  User Manager  │                         │ Product Manager │
│                │                         │                 │
│ • Register     │                         │ • Search        │
│ • Login        │                         │ • Top Selling   │
│ • Auth         │                         │ • Get by ID     │
└────────────────┘                         └─────────────────┘
                  │
    ┌─────────────┴─────────────────────────────────┐
    │                                                │
┌───▼──────────────┐                      ┌─────────▼──────────┐
│  Cart Manager    │                      │  Order Manager     │
│                  │                      │                    │
│ • Add to Cart    │                      │ • Checkout         │
│ • Remove         │                      │ • View Orders      │
│ • Calculate      │                      │ • Purchase History │
└──────────────────┘                      └────────────────────┘
                  │
    ┌─────────────┴─────────────────────────────────┐
    │                                                │
┌───▼────────────────┐                   ┌──────────▼──────────┐
│ Interaction        │                   │ Recommendation      │
│ Tracker            │                   │ Engine              │
│                    │                   │                     │
│ • Track View       │────────────┬─────▶│ • Collaborative    │
│ • Track Like       │            │      │ • Content-Based    │
│ • Track Cart       │            │      │ • Popularity       │
│ • Track Purchase   │            │      └────────────────────┘
└────────────────────┘            │
                                  │
                         ┌────────▼─────────┐
                         │  Graph Engine    │
                         │                  │
                         │ • Build Graph    │
                         │ • User→Product   │
                         │ • Product→User   │
                         └──────────────────┘
```

---

## 🧠 Thuật Toán Đề Xuất

### 1️⃣ Collaborative Filtering (BFS 2 Bước)

**Nguyên lý**: Tìm sản phẩm mới qua người dùng có sở thích tương tự

```
User A (Bạn) ──[Like]──▶ Sản phẩm P1 ◀──[Like]── User B (Người tương tự)
                                                      │
                                                      │
                                                   [Buy]
                                                      │
                                                      ▼
                                              Sản phẩm P2 (Đề xuất!)
```

**Công thức tính điểm**:
```
Score(P2) = Similarity(A, B) × Weight(B → P2)
Similarity(A, B) = min(Weight(A → P1), Weight(B → P1))
```

**Trọng số tương tác**:
- Purchase (Mua): 0.975
- Cart (Giỏ hàng): 0.775
- Like (Thích): 0.575
- View (Xem): 0.375
- Skip (Bỏ qua): 0.075

### 2️⃣ Content-Based Filtering

**Nguyên lý**: Đề xuất sản phẩm cùng category với sản phẩm đã thích

```
User thích: Áo thun A, Áo sơ mi B (Category: "Áo")
           ↓
Phân tích: User ưa thích category "Áo"
           ↓
Đề xuất: Áo khoác C, Áo len D, Áo polo E...
```

### 3️⃣ Popularity-Based (Fallback)

Khi không đủ dữ liệu cho Collaborative hoặc Content-Based:
- Đề xuất top 10-20 sản phẩm bán chạy nhất
- Điểm dựa trên `sold_count`

### 🎯 Chiến Lược 3 Tầng

```python
def get_recommendations(user):
    # TẦNG 1: Collaborative Filtering
    results = collaborative_filtering(user)
    if len(results) >= 10:
        return results[:10]
    
    # TẦNG 2: Content-Based
    results += content_based_filtering(user)
    if len(results) >= 10:
        return results[:10]
    
    # TẦNG 3: Popularity
    results += popularity_based()
    return results[:10]
```

---

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống

- Python 3.7 trở lên
- pip (Python package manager)

### Các Bước Cài Đặt

1. **Clone repository**
```bash
git clone https://github.com/yourusername/shopsensei.git
cd shopsensei
```

2. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

3. **Tạo file dữ liệu mẫu** (nếu chưa có)
```bash
python Creatproduct.py
```

4. **Chạy ứng dụng**
```bash
python main.py
```

### Dependencies

```
pandas>=1.3.0
xlsxwriter>=3.0.0
openpyxl>=3.0.0
```

---

## 📖 Sử Dụng

### 1. Đăng ký tài khoản

```
┌──────────────────────────────────────┐
│  1. 📝 Đăng ký                        │
│  2. 🔐 Đăng nhập                      │
│  3. 📦 Xem sản phẩm                   │
│  4. 🔍 Tìm kiếm                       │
│  5. 🏆 Top bán chạy                   │
│  0. ❌ Thoát                          │
└──────────────────────────────────────┘
Chọn: 1

Tên đăng nhập: alice
Mật khẩu: ****

✅ Đăng ký thành công! Chào alice
```

### 2. Xem và tương tác với sản phẩm

```
📦 DANH SÁCH SẢN PHẨM
──────────────────────────────────────
ID       Tên sản phẩm                    Giá
P0001    Áo thun hoạt hình              150,000đ
P0002    Áo sơ mi                        200,000đ
...

🔍 Nhập ID để xem chi tiết: P0001

═══════════════════════════════════════
  📦 ID: P0001
  🏷️  Tên: Áo thun hoạt hình
  📂 Danh mục: Áo
  💰 Giá: 150,000đ
  📊 Tồn kho: 50 sản phẩm
═══════════════════════════════════════

┌──────────────────────────────────────┐
│  1. 🛒 Thêm vào giỏ hàng             │
│  2. ❤️  Thích sản phẩm               │
│  3. ⭐️  Bỏ qua sản phẩm              │
└──────────────────────────────────────┘
```

### 3. Nhận đề xuất cá nhân hóa

```
✨ ĐỀ XUẤT SẢN PHẨM DÀNH CHO BẠN
══════════════════════════════════════

📊 Đang phân tích 15 tương tác của bạn...

🔹 TẦNG 1: Collaborative Filtering
   ✅ Tìm thấy 5 sản phẩm

🔹 TẦNG 2: Content-Based Filtering
   ✅ Tìm thấy 8 sản phẩm

✅ TỔNG: 13 sản phẩm đề xuất

#    ID       Tên sản phẩm                Giá           Điểm
──────────────────────────────────────────────────────────────
1    P0045    Giày sneaker              1,200,000đ    0.876
2    P0023    Áo khoác jean               600,000đ    0.654
3    P0067    Quần jogger                 450,000đ    0.543
...
```

### 4. Xem giải thích đề xuất

```
❓ Xem giải thích chi tiết cho sản phẩm #1? (y/n): y

═══════════════════════════════════════════════════════════════
📊 GIẢI THÍCH: Tại sao đề xuất 'Giày sneaker'?
═══════════════════════════════════════════════════════════════

🤝 Điểm Collaborative: 0.876
  ✓ User 'bob' (tương tự qua 'Áo thun hoạt hình') → 'Giày sneaker' (+0.650)
  ✓ User 'charlie' (tương tự qua 'Quần jean') → 'Giày sneaker' (+0.226)

📂 Category: Giày
  ✓ Bạn đã xem 2 sản phẩm category "Giày"
    - Giày thể thao
    - Giày cao gót

═══════════════════════════════════════════════════════════════
```

---

## 📁 Cấu Trúc Dự Án

```
shopsensei/
│
├── main.py                    # Entry point, UI chính
├── User.py                    # Model người dùng
├── UserManager.py             # Quản lý user (register, login)
├── Product.py                 # Model sản phẩm
├── ProductManager.py          # Quản lý sản phẩm (search, top selling)
├── OrderItem.py               # Model item trong đơn hàng
├── Order.py                   # Model đơn hàng
├── OrderManager.py            # Quản lý đơn hàng (checkout, history)
├── CartManager.py             # Quản lý giỏ hàng
├── InteractionTracker.py      # Theo dõi tương tác user
├── WeightNormalizer.py        # Normalize trọng số tương tác
├── GraphEngine.py             # Xây dựng đồ thị user-product
├── Recommendation.py          # Thuật toán đề xuất
├── DataAccess.py              # Đọc/ghi dữ liệu Excel
├── Creatproduct.py            # Script tạo dữ liệu mẫu
├── UIDisplay.py               # Utility hiển thị
│
├── users.xlsx                 # Database users
├── shop_products.xlsx         # Database products
├── user_interactions.json     # Lịch sử tương tác
│
├── requirements.txt           # Python dependencies
├── README.md                  # Documentation
└── LICENSE                    # License file
```

---

## 🎥 Demo

### Kịch bản Demo 1: Collaborative Filtering

```
User Alice:
  - Mua: Áo thun A, Quần jean B
  
User Bob:
  - Mua: Áo thun A, Giày C

Khi Alice xem đề xuất:
  → Hệ thống tìm thấy Bob (cùng thích Áo thun A)
  → Đề xuất Giày C cho Alice ✅
```

### Kịch bản Demo 2: Content-Based

```
User Charlie:
  - Xem: Áo khoác A, Áo len B (category: "Áo")
  
Khi Charlie xem đề xuất:
  → Hệ thống phát hiện Charlie thích category "Áo"
  → Đề xuất: Áo sơ mi C, Áo hoodie D, Áo polo E ✅
```

### Screenshots

*(Thêm screenshots ở đây)*

---

## 🧪 Testing

### Chạy test cases

```bash
python -m pytest tests/
```

### Test Coverage

```bash
pytest --cov=. tests/
```

### Manual Testing

1. **Test Collaborative Filtering**:
   - Tạo 2 users
   - Cả 2 mua chung 1 sản phẩm
   - User 1 mua thêm sản phẩm X
   - Kiểm tra User 2 có được đề xuất sản phẩm X không

2. **Test Content-Based**:
   - User xem nhiều sản phẩm cùng category
   - Kiểm tra đề xuất có tập trung vào category đó không

3. **Test Fallback**:
   - User mới không có tương tác
   - Kiểm tra có hiển thị top bán chạy không

---

## 🔧 Configuration

### Điều chỉnh trọng số tương tác

File: `WeightNormalizer.py`

```python
self._normalized_weight = {
    "purchase": (0.95, 1.0),    # Mua hàng: 0.975
    "cart": (0.70, 0.85),       # Giỏ hàng: 0.775
    "like": (0.50, 0.65),       # Thích: 0.575
    "view": (0.30, 0.45),       # Xem: 0.375
    "skip": (0.0, 0.15)         # Bỏ qua: 0.075
}
```

### Điều chỉnh số lượng đề xuất

File: `main.py`

```python
recommendations = recommender.get_recommendations(
    username=self.current_user.username,
    top_n=10,  # Thay đổi số lượng đề xuất
    exclude_products=purchased
)
```

---

## 🤝 Đóng Góp

Chúng tôi hoan nghênh mọi đóng góp! Vui lòng làm theo các bước sau:

1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

### Coding Standards

- Tuân thủ PEP 8
- Viết docstrings cho functions
- Thêm type hints
- Viết unit tests cho code mới

---

## 📊 Performance

### Độ phức tạp thuật toán

| Thuật toán | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Collaborative Filtering | O(U × P × U) | O(U × P) |
| Content-Based | O(P × C) | O(C) |
| Popularity-Based | O(P log P) | O(P) |

*U = số users, P = số products, C = số categories*

### Benchmark

Với 1000 users, 10000 products:
- Xây dựng đồ thị: ~0.5s
- Tính toán đề xuất: ~0.2s/user
- Memory usage: ~50MB

---

## 🐛 Troubleshooting

### Lỗi thường gặp

**1. Không tìm thấy file Excel**
```bash
FileNotFoundError: users.xlsx

Giải pháp:
python Creatproduct.py  # Tạo dữ liệu mẫu
```

**2. Không có đề xuất**
```
Nguyên nhân: User chưa có tương tác
Giải pháp: Xem, thích, hoặc mua một vài sản phẩm trước
```

**3. Import Error**
```bash
ModuleNotFoundError: No module named 'pandas'

Giải pháp:
pip install -r requirements.txt
```

---

## 📚 Tài Liệu Tham Khảo

### Papers
- [Collaborative Filtering for Implicit Feedback Datasets](https://ieeexplore.ieee.org/document/4781121)
- [Matrix Factorization Techniques for Recommender Systems](https://datajobs.com/data-science-repo/Recommender-Systems-[Netflix].pdf)

### Books
- *Programming Collective Intelligence* - Toby Segaran
- *Recommender Systems Handbook* - Francesco Ricci et al.

### Online Resources
- [Google's Recommendation Systems Course](https://developers.google.com/machine-learning/recommendation)
- [Netflix Prize](https://www.netflixprize.com/)

---

## 👥 Contributors

https://github.com/DuongNga13/DuongNga13-Shopsensei-ECommerce
---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Cảm ơn cộng đồng Python
- Inspired by Amazon, Netflix recommendation systems
- Dataset generated using `Creatproduct.py`

---

## 📞 Contact

**Your Name**
- GitHub: https://github.com/DuongNga13
- Email: duongnga1326@gmail.com

**Project Link**: https://github.com/DuongNga13/DuongNga13-Shopsensei-ECommerce

---


Made with ❤️ by [Your Name]

</div>
