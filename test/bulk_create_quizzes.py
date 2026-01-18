import pymysql
import time

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

# --- DANH SÁCH CÁC BÀI CẦN TẠO QUIZ (Khánh hãy điều chỉnh danh sách này) ---
LIST_NEW_QUIZZES = [
    {"section_id": 4, "name": "Quiz: Bài 7: Lộ trình chi tiết"},
    {"section_id": 5, "name": "Quiz: Bài 8: Tại sao chọn C++"},
    {"section_id": 6, "name": "Quiz: Bài 9: Cài đặt môi trường"},
]

COURSE_ID = 3

def bulk_create_quizzes_v2():
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print("--- ĐANG TẠO VỎ QUIZ TỰ ĐỘNG (BẢN V2 - CHỐNG TRÙNG) ---")

            for item in LIST_NEW_QUIZZES:
                now = int(time.time())
                
                # 1. Tạo bản ghi trong mdl_quiz
                sql_quiz = """
                    INSERT INTO mdl_quiz (course, name, intro, introformat, timecreated, timemodified, 
                    attempts, grademethod, decimalpoints, sumgrades, grade, questionsperpage)
                    VALUES (%s, %s, %s, 1, %s, %s, 0, 1, 2, 0, 10, 1)
                """
                cursor.execute(sql_quiz, (COURSE_ID, item['name'], f"Bài kiểm tra cho {item['name']}", now, now))
                quiz_id = cursor.lastrowid

                # 2. Tạo bản ghi trong mdl_course_modules
                cursor.execute("SELECT id FROM mdl_modules WHERE name = 'quiz'")
                module_id = cursor.fetchone()['id']

                sql_cm = "INSERT INTO mdl_course_modules (course, module, instance, section, added) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_cm, (COURSE_ID, module_id, quiz_id, item['section_id'], now))
                cm_id = cursor.lastrowid

                # 3. Cập nhật sequence trong mdl_course_sections
                cursor.execute("SELECT sequence FROM mdl_course_sections WHERE id = %s", (item['section_id'],))
                current_seq = cursor.fetchone()['sequence']
                new_seq = f"{current_seq},{cm_id}" if current_seq else str(cm_id)
                cursor.execute("UPDATE mdl_course_sections SET sequence = %s WHERE id = %s", (new_seq, item['section_id']))

                # 4. KIỂM TRA VÀ TẠO CONTEXT (Sửa lỗi Duplicate Entry)
                cursor.execute("SELECT id FROM mdl_context WHERE contextlevel = 70 AND instanceid = %s", (quiz_id,))
                existing_context = cursor.fetchone()
                
                if not existing_context:
                    # Nếu chưa có thì mới tạo mới
                    sql_ctx = "INSERT INTO mdl_context (contextlevel, instanceid, path, depth) VALUES (70, %s, NULL, 0)"
                    cursor.execute(sql_ctx, (quiz_id,))
                    print(f"✅ Đã tạo mới Quiz: {item['name']} (ID: {quiz_id})")
                else:
                    # Nếu có rồi thì bỏ qua không báo lỗi
                    print(f"⚠️ Quiz ID {quiz_id} đã có context, đã tự động đồng bộ.")

            conn.commit()
            print("\n🚀 HOÀN TẤT! Khánh hãy F5 lại Moodle nhé.")

    except Exception as e:
        print(f"❌ Lỗi: {e}")
        if conn: conn.rollback()
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    bulk_create_quizzes_v2()