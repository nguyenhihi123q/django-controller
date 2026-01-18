import pymysql

# --- CẤU HÌNH DATABASE (XAMPP Port 3307) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4' # Đảm bảo hiển thị đúng tiếng Việt
}

p3_data = {
    25: {"desc": "Cấu trúc điều kiện đơn giản nhất trong lập trình.", "obj": "logic, branching, if_statement, decision_making"},
    26: {"desc": "Xử lý hai nhánh hành động đối lập nhau.", "obj": "branching, if_else, binary_logic"},
    27: {"desc": "Kỹ thuật kiểm tra nhiều tầng điều kiện phức tạp.", "obj": "nested_logic, complex_branching, tiered_conditions"},
    28: {"desc": "Cách viết code rẽ nhánh ngắn gọn và tối ưu bằng toán tử 3 ngôi.", "obj": "ternary_operator, shorthand_syntax, optimization"},
    29: {"desc": "Sử dụng Switch Case để so khớp các giá trị rời rạc.", "obj": "switch_case, multi_way_branching, discrete_logic"},
    30: {"desc": "Giải thuật toán học cho phương trình ax + b = 0.", "obj": "algorithm, equation_solving, math_logic"},
    31: {"desc": "Giải thuật biện luận Delta cho phương trình bậc 2.", "obj": "algorithm, quadratic_equation, math_logic, delta_logic"},
    32: {"desc": "Bài toán thực tế sử dụng các khoảng giá trị để tính tiền điện.", "obj": "practice, real_world_logic, conditional_ranges"},
    33: {"desc": "Xây dựng chương trình máy tính bỏ túi cơ bản với các phép tính.", "obj": "practice, calculator_logic, arithmetic_operators"},
    34: {"desc": "Kiểm tra tính hợp lệ và tính toán diện tích tam giác.", "obj": "practice, geometry, triangle_logic, valid_triangle"},
    35: {"desc": "Danh sách bài tập tổng hợp rèn luyện tư duy logic rẽ nhánh.", "obj": "self_study, logic_practice, comprehensive_review"}
}

def update_p3():
    conn = None
    try:
        # Khởi tạo kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # Sử dụng 'with' để quản lý cursor (tự động đóng cursor)
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 3 vào Database: {db_config['database']} ---")
            
            for cmid, content in p3_data.items():
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Câu lệnh SQL Update
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
            print("\n🚀 THÀNH CÔNG: Đã xong 11 bài của Chương 3!")
            
    except pymysql.MySQLError as err:
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # Kiểm tra trạng thái mở của kết nối để đóng
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p3()