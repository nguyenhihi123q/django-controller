import mysql.connector

# ============================================================================
# 👇 CẤU HÌNH DATABASE (Lấy chuẩn từ file config.php sếp gửi)
# ============================================================================
db_config = {
    'host': 'localhost',
    'port': 3307,        # Port của sếp là 3307
    'user': 'root',
    'password': '',      # Pass để trống
    'database': 'lophocdhs',
    'raise_on_warnings': True
}

COURSE_ID = 3  # ID khóa học C++

def scan_quizzes():
    print(f"\n{'='*90}")
    print(f"🚀 KẾT NỐI ĐẾN DATABASE: {db_config['database']} (Port: {db_config['port']})")
    print(f"{'='*90}\n")

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # SQL: Lấy ID, Tên và đếm số slot (số câu hỏi) trong mỗi bài
        sql = """
            SELECT q.id, q.name, COUNT(qs.id) as so_cau_hoi
            FROM mdl_quiz q
            LEFT JOIN mdl_quiz_slots qs ON q.id = qs.quizid
            WHERE q.course = %s
            GROUP BY q.id, q.name
            ORDER BY q.id ASC
        """

        cursor.execute(sql, (COURSE_ID,))
        results = cursor.fetchall()

        if not results:
            print("❌ Không tìm thấy bài Quiz nào trong Course này!")
            return

        # In tiêu đề bảng
        print(f"{'ID':<6} | {'SL Câu':<8} | {'Trạng thái':<15} | {'Tên Bài Quiz'}")
        print("-" * 90)

        count_full = 0
        count_empty = 0

        for row in results:
            q_id = row['id']
            q_name = row['name']
            count = row['so_cau_hoi']
            
            # Đánh giá trạng thái
            if count == 0:
                status = "🔴 TRỐNG (0)"
                count_empty += 1
            elif count >= 8:
                status = "🟢 ĐÃ CÓ (8+)"
                count_full += 1
            else:
                status = f"🟡 THIẾU ({count})"

            # In ra màn hình
            print(f"{q_id:<6} | {count:<8} | {status:<15} | {q_name}")

        print("-" * 90)
        print(f"📊 TỔNG KẾT:")
        print(f"   - Đã nạp xong: {count_full} bài")
        print(f"   - Chưa nạp (Trống): {count_empty} bài")
        
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"❌ Lỗi kết nối: {err}")
        print("Sếp kiểm tra lại xem XAMPP MySQL đã bật chưa nhé?")

if __name__ == "__main__":
    scan_quizzes()