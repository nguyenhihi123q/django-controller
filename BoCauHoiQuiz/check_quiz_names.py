import pymysql

# --- CẤU HÌNH DATABASE (Sếp giữ nguyên như file get_lessons trước đó) ---
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lophocdhs',
    'port': 3307,
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

def check_names():
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print(f"{'='*10} DANH SÁCH TÊN QUIZ THỰC TẾ TRONG DB {'='*10}\n")
            
            # Lấy tên quiz trong course 3
            sql = "SELECT id, name FROM mdl_quiz WHERE course = 3 ORDER BY id ASC"
            cursor.execute(sql)
            quizzes = cursor.fetchall()

            if not quizzes:
                print("❌ Không tìm thấy bài Quiz nào trong Course 3.")
                return

            print(f"{'ID':<5} | {'Tên chính xác (Copy dòng này)'}")
            print("-" * 60)

            for q in quizzes:
                # In ra tên nằm trong dấu nháy đơn để sếp dễ nhìn thấy khoảng trắng thừa
                print(f"{q['id']:<5} | '{q['name']}'")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    check_names()