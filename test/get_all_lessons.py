import pymysql

# --- CẤU HÌNH DATABASE ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_108_lessons():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print(f"{'='*10} DANH SÁCH 108 BÀI HỌC TRONG KHÓA HỌC {'='*10}\n")
            
            # Truy vấn lấy cmid (Course Module ID) và tên của tất cả các Page trong Course 3
            query = """
                SELECT cm.id AS cmid, p.id AS page_id, p.name, s.name AS section_name, s.id AS section_id
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
                print("❌ Không tìm thấy bài học (Page) nào. Hãy kiểm tra lại khóa học.")
                return

            print(f"{'STT':<5} | {'CMID':<8} | {'Tên bài học':<40} | {'Thuộc Section'}")
            print("-" * 80)

            for index, lesson in enumerate(lessons, 1):
                section_display = lesson['section_name'] if lesson['section_name'] else f"Section ID {lesson['section_id']}"
                print(f"{index:<5} | {lesson['cmid']:<8} | {lesson['name'][:40]:<40} | {section_display}")

            print(f"\n✅ Tổng cộng tìm thấy: {len(lessons)} bài học.")
            print("\n💡 Ghi chú: Hãy dùng CMID này để gắn bộ Quiz tương ứng sau mỗi bài.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    get_108_lessons()