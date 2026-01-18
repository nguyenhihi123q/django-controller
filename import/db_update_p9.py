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

p9_data = {
    99: {"desc": "Cách định nghĩa kiểu dữ liệu mới bằng cách gom nhóm các biến thành phần.", "obj": "struct, custom_data_types, encapsulation, syntax"},
    100: {"desc": "Sử dụng toán tử chấm để thao tác với các thuộc tính của biến cấu trúc.", "obj": "struct_member, data_access, syntax"},
    101: {"desc": "Cơ chế sao chép dữ liệu và các quy tắc gán giá trị giữa các Struct.", "obj": "struct_assignment, memory_copy, data_persistence"},
    102: {"desc": "Kỹ thuật quản lý danh sách đối tượng quy mô lớn thông qua mảng cấu trúc.", "obj": "array_of_structs, data_organization, record_management"},
    103: {"desc": "Làm chủ toán tử mũi tên (->) để thao tác cấu trúc qua con trỏ.", "obj": "pointer_to_struct, arrow_operator, memory_efficiency"},
    104: {"desc": "Thực hành: Xây dựng module quản lý hồ sơ nhân viên chuyên nghiệp.", "obj": "practice, record_management, employee_system"},
    105: {"desc": "Ứng dụng cấu trúc để giải quyết các bài toán tọa độ hình học.", "obj": "practice, geometry_struct, coordinate_system"},
    106: {"desc": "Xây dựng kiểu dữ liệu Phân số và các thuật toán tính toán liên quan.", "obj": "practice, math_struct, operator_logic"},
    107: {"desc": "Thử thách tổng hợp thiết kế cấu trúc dữ liệu cho bài toán thực tế.", "obj": "self_study, struct_mastery, comprehensive_review"}
}

def update_p9():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng 'with' để quản lý cursor tự động
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 9 (Struct) vào Database: {db_config['database']} ---")
            
            for cmid, content in p9_data.items():
                # Tạo nội dung HTML kết hợp mô tả và mục tiêu
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Câu lệnh SQL JOIN để cập nhật bảng mdl_page của Moodle
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Lưu các thay đổi vào Database
            conn.commit()
            print("\n🏆 TUYỆT VỜI! Hệ thống quản lý dữ liệu đã sẵn sàng.")

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
    update_p9()