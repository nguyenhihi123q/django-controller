import pymysql

DB_CONFIG = {
    'host': 'localhost', 'user': 'root', 'password': '',
    'database': 'lophocdhs', 'port': 3307, 'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def force_show():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print("--- ĐANG CƯỜNG HÓA HIỂN THỊ 118 QUIZ ---")
            
            # 1. Bật Visible cho tất cả Module Quiz trong Course 3
            sql_visible = """
                UPDATE mdl_course_modules 
                SET visible = 1, visibleoncoursepage = 1, availability = NULL
                WHERE course = 3 AND module = (SELECT id FROM mdl_modules WHERE name = 'quiz')
            """
            cursor.execute(sql_visible)
            
            # 2. Kiểm tra xem dữ liệu đã thực sự vào bảng mdl_quiz chưa
            cursor.execute("SELECT COUNT(*) as total FROM mdl_quiz WHERE course = 3")
            total_quiz = cursor.fetchone()['total']
            print(f"📊 Database ghi nhận: {total_quiz} bài Quiz đang tồn tại.")

            # 3. Làm sạch chuỗi Sequence (Xóa dấu phẩy thừa ở đầu/cuối hoặc dấu phẩy kép)
            cursor.execute("SELECT id, sequence FROM mdl_course_sections WHERE course = 3")
            sections = cursor.fetchall()
            for s in sections:
                if s['sequence']:
                    clean_seq = s['sequence'].strip(',').replace(',,', ',')
                    cursor.execute("UPDATE mdl_course_sections SET sequence = %s WHERE id = %s", (clean_seq, s['id']))

            conn.commit()
            print("✅ Đã ép hiển thị và làm sạch sơ đồ bài học.")
            
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally: conn.close()

if __name__ == "__main__": force_show()