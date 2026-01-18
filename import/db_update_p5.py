import pymysql

# --- CẤU HÌNH DATABASE (XAMPP Port 3307) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4' # Hỗ trợ tiếng Việt đầy đủ
}

p5_data = {
    48: {"desc": "Cách khai báo và cấp phát vùng nhớ liên tục cho tập hợp dữ liệu.", "obj": "array, declaration, memory_allocation, data_structure"},
    49: {"desc": "Kỹ thuật sử dụng chỉ số (index) để thao tác trên từng phần tử mảng.", "obj": "array, indexing, traversal, memory_access"},
    50: {"desc": "Thuật toán tìm kiếm tuyến tính trên mảng 1 chiều.", "obj": "array, linear_search, algorithms, lookup"},
    51: {"desc": "Các thuật toán đổi chỗ để sắp xếp dữ liệu tăng/giảm dần.", "obj": "array, sorting, algorithm, data_organization"},
    52: {"desc": "Khai báo và tư duy không gian với ma trận (mảng của mảng).", "obj": "multi_dimensional_array, matrix, declaration"},
    53: {"desc": "Sử dụng vòng lặp lồng nhau để xử lý hàng và cột của ma trận.", "obj": "matrix, nested_loops, indexing, matrix_manipulation"},
    54: {"desc": "Thực hành tính tổng và các thống kê cơ bản trên mảng.", "obj": "practice, array_math, logic"},
    55: {"desc": "Kỹ thuật tối ưu tìm giá trị lớn nhất và nhỏ nhất trong tập dữ liệu.", "obj": "practice, min_max_algorithm, logic"},
    56: {"desc": "Xử lý thay đổi cấu trúc mảng: Chèn và xóa phần tử.", "obj": "practice, array_modification, indexing"},
    57: {"desc": "Các thuật toán tách mảng và gộp nhiều mảng dữ liệu.", "obj": "practice, array_merging, split_array"},
    58: {"desc": "Các bài toán thực tế nâng cao vận dụng mảng 2 chiều.", "obj": "practice, advanced_matrix, combined_logic"},
    59: {"desc": "Tổng hợp thử thách để làm chủ cấu trúc dữ liệu mảng.", "obj": "self_study, array_mastery, review"}
}

def update_p5():
    conn = None
    try:
        # Khởi tạo kết nối PyMySQL
        conn = pymysql.connect(**db_config)
        
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 5 vào Database: {db_config['database']} ---")
            
            for cmid, content in p5_data.items():
                # Tạo nội dung HTML kết hợp mô tả và mục tiêu
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Query cập nhật thông qua JOIN giữa mdl_page và mdl_course_modules
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Lưu thay đổi
            conn.commit()
            print("\n✨ XONG! Bạn đã hoàn thành 50% lộ trình cập nhật dữ liệu.")

    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Đóng kết nối an toàn
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p5()