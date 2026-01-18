import pymysql

# --- CẤU HÌNH DATABASE (XAMPP Port 3307) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4'  # Đảm bảo hiển thị đúng các ký tự đặc biệt và tiếng Việt
}

p7_data = {
    73: {"desc": "Tìm hiểu về địa chỉ ô nhớ và cách biến con trỏ quản lý RAM trực tiếp.", "obj": "memory_address, pointer, variables, ram_management"},
    74: {"desc": "Làm chủ toán tử lấy địa chỉ & và toán tử giải tham chiếu *.", "obj": "address_of, dereference, pointer_operators, syntax"},
    75: {"desc": "Các phép toán cộng, trừ trên địa chỉ và kỹ thuật điều hướng vùng nhớ.", "obj": "pointer_arithmetic, memory_navigation, offset"},
    76: {"desc": "Cách sử dụng con trỏ void và null để lập trình an toàn, tránh lỗi crash.", "obj": "void_pointer, null_pointer, safe_coding, memory_safety"},
    77: {"desc": "Khám phá mối liên hệ mật thiết giữa mảng và địa chỉ con trỏ.", "obj": "array_pointer_relationship, memory_layout, indexing"},
    78: {"desc": "Kỹ thuật quản lý một danh sách các địa chỉ vùng nhớ khác nhau thông qua mảng.", "obj": "array_of_pointers, memory_organization, advanced_data"},
    79: {"desc": "Tư duy đa tầng với con trỏ cấp 2 và cách quản lý ma trận động.", "obj": "double_pointer, pointer_to_pointer, matrix_memory"},
    80: {"desc": "Thực hành hoán vị giá trị biến thông qua con trỏ trong hàm.", "obj": "practice, swap_function, pass_by_address"},
    81: {"desc": "Ứng dụng con trỏ để tìm kiếm dữ liệu tối ưu trên vùng nhớ.", "obj": "practice, pointer_traversal, algorithm_optimization"},
    82: {"desc": "Sử dụng con trỏ để sắp xếp dữ liệu mà không cần chỉ số mảng.", "obj": "practice, pointer_sorting, memory_efficiency"},
    83: {"desc": "Làm quen với cấp phát động (new/delete) và quản lý vùng nhớ Heap.", "obj": "practice, dynamic_memory, heap_allocation, new_delete"},
    84: {"desc": "Kỹ thuật nâng cao: Hàm trả về con trỏ và cách tránh rò rỉ bộ nhớ.", "obj": "practice, memory_leak, returning_address"},
    85: {"desc": "Tổng hợp các bài toán thử thách kỹ năng quản lý bộ nhớ bậc cao.", "obj": "self_study, pointer_mastery, memory_management_review"}
}

def update_p7():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng context manager cho cursor
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 7 (Con trỏ) vào Database: {db_config['database']} ---")
            
            for cmid, content in p7_data.items():
                # Kết hợp mô tả và mục tiêu thành định dạng HTML
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Query cập nhật dữ liệu
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Lưu các thay đổi
            conn.commit()
            print("\n🏆 CHÚC MỪNG! Bạn đã vượt qua phần khó nhất của khóa học.")

    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Đóng kết nối (PyMySQL sử dụng thuộc tính .open)
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p7()