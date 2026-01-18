import pymysql

DB_CONFIG = {
    'host': 'localhost', 'user': 'root', 'password': '',
    'database': 'lophocdhs', 'port': 3307,
    'cursorclass': pymysql.cursors.DictCursor
}

def find_sections():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print("--- DANH SÁCH SECTION TRONG KHÓA HỌC ---")
            # Lấy tất cả section của khóa học ID 3
            cursor.execute("SELECT id, name, section FROM mdl_course_sections WHERE course = 3 ORDER BY section ASC")
            sections = cursor.fetchall()
            for s in sections:
                name = s['name'] if s['name'] else f"Section {s['section']}"
                print(f"ID thực tế: {s['id']} | Tên: {name}")
    finally: conn.close()

if __name__ == "__main__": find_sections()