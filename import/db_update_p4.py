import pymysql

# --- CẤU HÌNH DATABASE (Đã khớp theo XAMPP Port 3307) ---
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4'  # Đảm bảo không lỗi font tiếng Việt
}

p4_data = {
    36: {"desc": "Sử dụng vòng lặp khi chưa biết trước số lần lặp cụ thể.", "obj": "loop, while_loop, condition, iteration"},
    37: {"desc": "Thực hiện khối lệnh ít nhất một lần trước khi kiểm tra điều kiện.", "obj": "loop, do_while, iteration, post_condition"},
    38: {"desc": "Tối ưu hóa vòng lặp với số lần xác định và bộ đếm.", "obj": "loop, for_loop, counter, iteration"},
    39: {"desc": "Kỹ thuật thoát vòng lặp ngay lập tức khi đạt mục tiêu.", "obj": "loop_control, break, termination"},
    40: {"desc": "Bỏ qua lần lặp hiện tại để chuyển sang bước kế tiếp.", "obj": "loop_control, continue, skip_iteration"},
    41: {"desc": "Tư duy đa chiều xử lý bài toán ma trận và hình khối.", "obj": "nested_loops, complex_logic, matrix_thinking"},
    42: {"desc": "Ứng dụng vòng lặp để tính toán các dãy số toán học.", "obj": "practice, series_calculation, arithmetic_progression"},
    43: {"desc": "Giải thuật kiểm tra số hoàn thiện trong lập trình.", "obj": "practice, perfect_number, math_algorithm"},
    44: {"desc": "Kỹ thuật tách và xử lý từng chữ số trong một số nguyên.", "obj": "practice, math_logic, digit_extraction"},
    45: {"desc": "Xây dựng trò chơi logic đoán số với vòng lặp vô tận có điều kiện.", "obj": "practice, game_logic, random_number, combined_logic"},
    46: {"desc": "Rèn luyện tư duy vòng lặp lồng nhau qua bài toán in hình nghệ thuật.", "obj": "practice, pattern_printing, visualization, nested_loops"},
    47: {"desc": "Tổng hợp các thử thách nâng cao để làm chủ kỹ năng xử lý vòng lặp.", "obj": "self_study, comprehensive_review, loop_mastery"}
}

def update_p4():
    conn = None
    try:
        # 1. Kết nối bằng PyMySQL
        conn = pymysql.connect(**db_config)
        
        # 2. Sử dụng 'with' để quản lý cursor an toàn
        with conn.cursor() as cursor:
            print(f"--- Đang cập nhật PHẦN 4 vào Database: {db_config['database']} (Port {db_config['port']}) ---")
            
            for cmid, content in p4_data.items():
                full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
                
                # Câu lệnh SQL (Giữ nguyên cấu trúc JOIN của Moodle)
                query = """
                    UPDATE mdl_page p
                    JOIN mdl_course_modules cm ON p.id = cm.instance
                    SET p.intro = %s
                    WHERE cm.id = %s
                """
                
                cursor.execute(query, (full_intro, cmid))
                print(f"✅ Đã cập nhật thành công Bài ID: {cmid}")
            
            # 3. Xác nhận thay đổi
            conn.commit()
            print("\n🔥 TUYỆT VỜI: Đã hoàn tất 12 bài của Chương 4!")

    except pymysql.MySQLError as err:
        # 4. Bắt lỗi riêng cho PyMySQL
        print(f"❌ Lỗi Database: {err}")
    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        # 5. Đóng kết nối đúng cách
        if conn and conn.open:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_p4()