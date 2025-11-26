import xlsxwriter
import random

workbook = xlsxwriter.Workbook('shop_products.xlsx')
worksheet = workbook.add_worksheet()

headers = ["id", "name", "category", "price", "stock", "sizes", "colors", "sold_count"]
for col, header in enumerate(headers):
    worksheet.write(0, col, header)

used_names_count = {}

categories = {
    "Áo": ["Áo thun hoạt hình", "Áo sơ mi", "Áo dài tay", "Áo khoác gió", "Áo hoodie", "Áo ba lỗ", "Áo len", "Áo polo", "Áo crop top", "Áo vest", "Áo bomber", "Áo khoác jean", "Áo khoác da", "Áo khoác dạ", "Áo khoác lông vũ", "Áo peplum", "Áo trễ vai", "Áo yếm", "Áo tunic", "Áo nỉ", "Áo sơ mi denim", "Áo sơ mi caro", "Áo sơ mi voan", "Áo sơ mi lụa", "Áo sơ mi kẻ sọc"],
    "Quần": ["Quần jean", "Quần short", "Quần kaki", "Quần thể thao", "Quần baggy", "Quần tây", "Quần legging", "Quần jogger", "Quần ống rộng", "Quần culottes", "Quần yếm", "Quần chinos", "Quần đùi", "Quần lửng", "Quần tất", "Quần da", "Quần vải", "Quần thun", "Quần ống côn", "Quần ống loe", "Quần lót nam", "Quần lót nữ", "Quần bơi", "Quần pyjama", "Quần công sở", "Quần thể dục", "Quần yoga", "Quần tập gym", "Quần bầu", "Quần ngủ", "Quần thể thao", "Quần công sở", "Quần dạo phố"],
    "Giày": ["Giày thể thao", "Giày sneaker", "Giày búp bê", "Giày cao gót", "Giày sandal", "Giày lười", "Giày tây", "Giày oxford", "Giày derby", "Giày brogue", "Giày chelsea", "Giày boots", "Giày slip-on", "Giày mule", "Giày platform", "Giày espadrille", "Giày loafers", "Giày running", "Giày hiking", "Giày training", "Giày golf", "Giày tennis", "Giày bóng đá", "Giày cầu lông", "Giày bóng rổ", "Giày trượt ván", "Giày leo núi", "Giày đạp xe", "Giày đi bộ", "Giày dép", "Dép xỏ ngón", "Dép lê", "Dép quai hậu", "Dép sandal"],
    "Mũ": ["Mũ lưỡi trai", "Mũ len", "Mũ bucket", "Mũ nón rộng vành", "Mũ snapback", "Mũ fedora", "Mũ beret", "Mũ beanie", "Mũ tai bèo", "Mũ phớt", "Mũ cối", "Mũ bảo hiểm", "Mũ nón thời trang", "Mũ nón thể thao", "Mũ nón đi biển", "Mũ nón đi phượt", "Mũ nón đi chơi", "Mũ nón đi làm", "Mũ nón đi học", "Mũ nón chống nắng", "Mũ nón giữ ấm", "Mũ nón dạ", "Mũ nón vải", "Mũ nón lưới", "Mũ nón ren", "Mũ nón satin", "Mũ nón cotton", "Mũ nón polyester", "Mũ nón nylon"],
    "Phụ kiện": ["Thắt lưng", "Khăn quàng", "Túi xách", "Ví", "Vòng tay", "Kính mát", "Dây chuyền", "Bông tai", "Nhẫn", "Mũ bảo hiểm", "Găng tay", "Tất chân", "Nón len", "Nón thời trang", "Nón thể thao", "Nón đi biển", "Nón đi phượt", "Nón đi chơi", "Nón đi làm", "Nón đi học", "Nón chống nắng", "Nón giữ ấm", "Nón dạ", "Nón vải", "Nón lưới", "Nón ren", "Nón satin", "Nón cotton", "Nón polyester", "Nón nylon", "Dây đeo đồng hồ", "Mặt đồng hồ", "Khóa cài túi", "Phụ kiện tóc", "Kẹp tóc", "Băng đô", "Cài áo", "Ghim cài", "Dây buộc giày", "Lót giày", "Đế giày", "Phụ kiện điện thoại", "Ốp lưng điện thoại", "Giá đỡ điện thoại", "Tai nghe", "Sạc dự phòng"]
}

sizes_options = ["S", "M", "L", "XL", "XXL"]
colors_options = ["Đỏ", "Đen", "Trắng", "Xanh", "Vàng", "Xám", "Hồng", "Tím", "Nâu", "Cam"]

for i in range(1, 201):
    pid = f"P{i:04d}"
    category = random.choice(list(categories.keys()))
    
    base_name = random.choice(categories[category])
    
    if base_name in used_names_count:
        used_names_count[base_name] += 1
    else:
        used_names_count[base_name] = 1
        
    if used_names_count[base_name] > 1:
        name = f"{base_name} #{used_names_count[base_name]}"
    else:
        name = base_name
        
    price = random.randint(2, 40) * 50000
    stock = random.randint(10, 100)
    sizes = ",".join(random.sample(sizes_options, random.randint(1, len(sizes_options))))
    colors = ",".join(random.sample(colors_options, random.randint(1, len(colors_options))))
    sold_count = random.randint(0, 500)

    row = [pid, name, category, price, stock, sizes, colors, sold_count]
    for col, value in enumerate(row):
        worksheet.write(i, col, value)

workbook.close()
print("✔ File shop_products_unique.xlsx đã được tạo thành công với 200 sản phẩm!")