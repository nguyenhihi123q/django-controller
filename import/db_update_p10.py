import pymysql

# --- CẤU HÌNH DATABASE (Khớp theo XAMPP Port 3307 của Khánh) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4'  # Đảm bảo lưu trữ tiếng Việt và ký tự đặc biệt chuẩn xác
}

p10_data = {
    108: {"desc": "Hiểu về luồng dữ liệu (Stream) và cơ chế lưu trữ bền vững trên ổ cứng.", "obj": "file_io, persistence, streams, theory"},
    109: {"desc": "Làm chủ kỹ thuật xuất dữ liệu văn bản ra file bằng ofstream.", "obj": "file_write, ofstream, text_file, output_stream"},
    110: {"desc": "Kỹ thuật đọc và phân tích nội dung từ tập tin văn bản bằng ifstream.", "obj": "file_read, ifstream, text_file, input_stream"},
    111: {"desc": "Kỹ thuật cấp cao: Lưu trữ trực tiếp đối tượng cấu trúc xuống bộ nhớ dài hạn.", "obj": "binary_write, struct_persistence, data_storage"},
    112: {"desc": "Tải và khôi phục dữ liệu cấu trúc từ tập tin vào bộ nhớ chương trình.", "obj": "binary_read, struct_retrieval, memory_loading"},
    113: {"desc": "Thực hành: Quy trình xử lý danh sách số liệu thông qua tập tin văn bản.", "obj": "practice, numeric_data, file_processing"},
    114: {"desc": "Xây dựng module lưu trữ thông tin sinh viên chuyên nghiệp cho đồ án.", "obj": "practice, list_persistence, student_management"},
    115: {"desc": "Ứng dụng quản lý kho hàng với tính năng sao lưu dữ liệu sản phẩm.", "obj": "practice, inventory_management, real_world_app"},
    116: {"desc": "Thử thách cuối cùng: Hoàn thiện kỹ năng xây dựng ứng dụng C++ hoàn chỉnh.", "obj": "self_study, file_mastery, project_thinking"}
}

def update_p10():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng 'with' để quản lý cursor tự động đóng
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 10 (Cuối cùng) vào Database: {db_config['database']} ---")
            
            for cmid, content in p10_data.items():
                # Tạo nội dung HTML kết hợp mô tả và mục tiêu
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Truy vấn SQL JOIN để cập nhật mô tả bài học trong Moodle (mdl_page)
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Xác nhận lưu các thay đổi vào Database
            conn.commit()
            
            print("\n" + "="*50)
            print("🎉 CHÚC MỪNG KHÁNH! ĐÃ HOÀN TẤT CẬP NHẬT 108 BÀI HỌC!")
            print("="*50)

    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Kiểm tra và đóng kết nối an toàn theo chuẩn PyMySQL
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p10()