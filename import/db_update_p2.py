import pymysql 

# --- CẤU HÌNH DATABASE ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4'
}

p2_data = {
    14: {"desc": "Cách sử dụng // và /* */ để làm sạch mã nguồn.", "obj": "comments, documentation, clean_code"},
    15: {"desc": "Tìm hiểu int, float, char, bool và quy tắc đặt tên.", "obj": "data_types, variables, naming_rules"},
    16: {"desc": "Cách dùng const, #define và xây dựng biểu thức toán.", "obj": "constants, expressions, math_operators"},
    17: {"desc": "Chuyển đổi qua lại giữa các kiểu dữ liệu.", "obj": "type_casting, conversion, data_precision"},
    18: {"desc": "Các phép toán số học, so sánh và toán tử logic nâng cao.", "obj": "operators, arithmetic, logic_operators"},
    19: {"desc": "Thực hành tính chu vi và diện tích hình tròn.", "obj": "practice, geometry, circle_calculation"},
    20: {"desc": "Thực hành tính chu vi và diện tích tam giác.", "obj": "practice, geometry, triangle_calculation"},
    21: {"desc": "Sử dụng thư viện cmath cho sin, cos, tan.", "obj": "math_library, trigonometry, cmath"},
    22: {"desc": "Thuật toán chuyển đổi từ giây sang Giờ:Phút:Giây.", "obj": "algorithm, time_conversion, modulo_operator"},
    23: {"desc": "Tính điểm và làm quen với độ ưu tiên toán tử.", "obj": "practice, average_score, operator_precedence"},
    24: {"desc": "Danh sách bài tập tổng hợp về biến và kiểu dữ liệu.", "obj": "self_study, comprehensive_practice, review"}
}

def update_p2():
    conn = None
    try:
        # 1. Thay đổi cách kết nối sang pymysql
        conn = pymysql.connect(**db_config)
        
        # 2. Sử dụng context manager (with) cho cursor để tự động đóng
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 2 vào Database: {db_config['database']} (Port {db_config['port']}) ---")
            
            for cmid, content in p2_data.items():
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật xong Bài ID: {cmid}")
                
            # 3. Lưu thay đổi
            conn.commit()
            print("\n🎉 THÀNH CÔNG: Đã xong 11 bài của Chương 2!")

    except pymysql.MySQLError as err:
        # 4. Thay đổi lớp bắt lỗi sang pymysql.MySQLError
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # 5. Kiểm tra và đóng kết nối đúng cách trong PyMySQL
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối.")

if __name__ == "__main__":
    update_p2()