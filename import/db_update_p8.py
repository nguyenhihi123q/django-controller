import pymysql

# --- CẤU HÌNH DATABASE (Khớp theo XAMPP Port 3307 của Khánh) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4' # Hỗ trợ lưu trữ tiếng Việt và ký tự đặc biệt
}

p8_data = {
    86: {"desc": "Bản chất chuỗi là mảng ký tự và tầm quan trọng của ký tự kết thúc null.", "obj": "string, char_array, null_terminator, memory"},
    87: {"desc": "Làm chủ kỹ thuật nhập xuất chuỗi và cách xử lý trôi lệnh trong C++.", "obj": "input_output, cin_getline, buffer_cleaning"},
    88: {"desc": "Sử dụng thư viện cstring để sao chép dữ liệu giữa các vùng nhớ chuỗi.", "obj": "string_copy, cstring_library, memory_safety"},
    89: {"desc": "Kỹ thuật nối chuỗi và quản lý vùng đệm tránh tràn bộ nhớ.", "obj": "string_concatenation, buffer, cstring"},
    90: {"desc": "Các thuật toán tìm kiếm vị trí ký tự và chuỗi con hiệu quả.", "obj": "string_searching, substring, algorithms"},
    91: {"desc": "Cơ chế so sánh chuỗi theo bảng mã ASCII và thứ tự từ điển.", "obj": "string_comparison, lexicographical_order"},
    92: {"desc": "Kỹ thuật biến đổi định dạng chữ viết cho dữ liệu văn bản.", "obj": "string_transformation, ascii, to_upper, to_lower"},
    93: {"desc": "Thực hành đếm tần suất xuất hiện và phân tích cấu trúc chuỗi.", "obj": "practice, character_counting, iteration"},
    94: {"desc": "Ứng dụng chuỗi để giải bài toán đối xứng (Palindrome) kinh điển.", "obj": "practice, string_reversing, palindrome, logic"},
    95: {"desc": "Quy trình chuẩn hóa chuỗi văn bản: Xóa khoảng trắng thừa, viết hoa đầu từ.", "obj": "practice, word_tokenization, string_cleaning"},
    96: {"desc": "Xây dựng chức năng tìm kiếm và thay thế nội dung tự động.", "obj": "practice, find_and_replace, string_manipulation"},
    97: {"desc": "Tổ chức mảng chuỗi và thuật toán sắp xếp danh sách tên sinh viên.", "obj": "practice, string_sorting, array_of_strings"},
    98: {"desc": "Thử thách tổng hợp nâng cao năng lực xử lý dữ liệu văn bản.", "obj": "self_study, string_mastery, comprehensive_review"}
}

def update_p8():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng with để tự động quản lý việc đóng cursor
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 8 (Chuỗi) vào Database: {db_config['database']} ---")
            
            for cmid, content in p8_data.items():
                # Chuẩn bị nội dung HTML
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Truy vấn SQL JOIN để cập nhật mô tả bài học trong Moodle
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Xác nhận thay đổi
            conn.commit()
            print("\n✨ XONG! Chỉ còn 2 chương nữa là hoàn tất 108 bài học.")

    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Kiểm tra và đóng kết nối an toàn
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p8()