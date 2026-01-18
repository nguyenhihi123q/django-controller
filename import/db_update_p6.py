import pymysql

# --- CẤU HÌNH DATABASE (XAMPP Port 3307) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4' # Quan trọng để hiển thị đúng tiếng Việt
}

p6_data = {
    60: {"desc": "Tư duy chia để trị và cách đóng gói mã nguồn để tái sử dụng.", "obj": "function, modularity, code_reuse, syntax"},
    61: {"desc": "Hiểu về cơ chế gọi hàm và luồng xử lý trong bộ nhớ Stack.", "obj": "function_call, execution_flow, stack_memory"},
    62: {"desc": "Phân biệt dữ liệu truyền vào và biến đại diện trong định nghĩa hàm.", "obj": "parameters, arguments, function_scope"},
    63: {"desc": "Kỹ thuật truyền địa chỉ để thay đổi giá trị biến gốc từ trong hàm.", "obj": "pass_by_value, pass_by_reference, memory_address"},
    64: {"desc": "Cách thiết lập giá trị sẵn có cho tham số để tối ưu lời gọi hàm.", "obj": "default_parameters, function_overloading, syntax"},
    65: {"desc": "Khái niệm hàm tự gọi lại chính nó và cách kiểm soát điểm dừng.", "obj": "recursion, base_case, recursive_step, thinking"},
    66: {"desc": "Áp dụng hàm để tổ chức mã nguồn cho giải thuật phương trình bậc 2.", "obj": "practice, math_functions, modular_design"},
    67: {"desc": "Kỹ thuật truyền và thao tác trên mảng thông qua tham số hàm.", "obj": "practice, array_parameter, integration"},
    68: {"desc": "Giải quyết bài toán dãy Fibonacci bằng cả tư duy vòng lặp và đệ quy.", "obj": "practice, fibonacci, recursion_algorithm"},
    69: {"desc": "Xây dựng các hàm chuyên biệt để xử lý tính toán hình học.", "obj": "practice, geometry_functions, modularity"},
    70: {"desc": "Tái cấu trúc mã nguồn trò chơi theo phong cách lập trình hàm chuyên nghiệp.", "obj": "practice, logic_abstraction, game_design"},
    71: {"desc": "Tổng hợp thử thách nâng cao để làm chủ kỹ năng thiết kế hàm.", "obj": "self_study, function_mastery, review"}
}

def update_p6():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng 'with' để quản lý cursor an toàn
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 6 vào Database: {db_config['database']} ---")
            
            for cmid, content in p6_data.items():
                # Tạo nội dung HTML cho Moodle
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Câu lệnh SQL thực hiện JOIN giữa bảng mdl_page và mdl_course_modules
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
            
            # Commit để lưu thay đổi vào DB
            conn.commit()
            print("\n🚀 TUYỆT VỜI! Chương Hàm đã sẵn sàng để phân tích dữ liệu.")

    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Đóng kết nối đúng cách theo chuẩn PyMySQL
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p6()