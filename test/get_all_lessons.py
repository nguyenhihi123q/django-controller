import pymysql

# --- CẤU HÌNH DATABASE (Sếp chỉnh lại nếu cần) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def export_lessons_to_python_list():
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            # 1. Truy vấn lấy CMID và Tên bài (Chỉ lấy resource kiểu 'page')
            # Nếu bài học của sếp là URL hay Label, hãy đổi 'page' thành 'url' hoặc 'label'
            query = """
                SELECT cm.id AS cmid, p.name
                FROM mdl_course_modules cm
                JOIN mdl_modules m ON cm.module = m.id
                JOIN mdl_page p ON cm.instance = p.id
                JOIN mdl_course_sections s ON cm.section = s.id
                WHERE cm.course = 3 AND m.name = 'page'
                ORDER BY s.section ASC, cm.id ASC
            """
            cursor.execute(query)
            lessons = cursor.fetchall()

            if not lessons:
                print("# ❌ Không tìm thấy bài học nào (kiểm tra lại Course ID hoặc Module Type).")
                return

            # 2. IN RA MÀN HÌNH ĐÚNG ĐỊNH DẠNG PYTHON
            print(f"# ✅ Tìm thấy {len(lessons)} bài học. Copy đoạn dưới đây vào file Python:\n")
            print("lessons_list = [")

            for lesson in lessons:
                # Tạo tên quiz theo cú pháp sếp muốn
                quiz_name = f"bài test bài {lesson['name']}"
                
                # In ra dòng code Python (f-string)
                # Lưu ý: cmid ở đây là after_cmid cho bài quiz
                print(f'    {{"after_cmid": {lesson["cmid"]}, "name": "{quiz_name}"}},')

            print("]")
            print("\n# 🏁 Hết danh sách. Sếp copy toàn bộ đoạn trong ngoặc vuông nhé!")

    except Exception as e:
        print(f"# ❌ Lỗi kết nối CSDL: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    export_lessons_to_python_list()