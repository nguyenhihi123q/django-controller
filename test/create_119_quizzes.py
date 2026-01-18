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

COURSE_ID = 3

def fix_and_create_quizzes():
    conn = None
    try:
        conn = pymysql.connect(**DB_CONFIG)
        with conn.cursor() as cursor:
            print("--- BƯỚC 1: DỌN DẸP DỮ LIỆU MỒ CÔI ---")
            # Xóa các context của Quiz (level 70) mà không có Quiz tương ứng tồn tại
            cleanup_sql = """
                DELETE FROM mdl_context 
                WHERE contextlevel = 70 
                AND instanceid NOT IN (SELECT id FROM mdl_quiz)
            """
            cursor.execute(cleanup_sql)
            conn.commit()
            print("✅ Đã dọn sạch các Context lỗi.")

            print(f"\n--- BƯỚC 2: TẠO {119} BÀI QUIZ ---")
            
            # Lấy danh sách bài học
            query_lessons = """
                SELECT cm.id AS cmid, p.id AS instance_id, p.name, cm.section AS section_id
                FROM mdl_course_modules cm
                JOIN mdl_modules m ON cm.module = m.id
                JOIN mdl_page p ON cm.instance = p.id
                WHERE cm.course = %s AND m.name = 'page'
                ORDER BY cm.section ASC, cm.id ASC
            """
            cursor.execute(query_lessons, (COURSE_ID,))
            lessons = cursor.fetchall()
            
            cursor.execute("SELECT id FROM mdl_modules WHERE name = 'quiz'")
            quiz_module_id = cursor.fetchone()['id']

            success_count = 0
            for lesson in lessons:
                try:
                    now = int(time.time())
                    quiz_name = f"Quiz: {lesson['name']}"
                    
                    # Kiểm tra trùng tên Quiz
                    cursor.execute("SELECT id FROM mdl_quiz WHERE course = %s AND name = %s", (COURSE_ID, quiz_name))
                    if cursor.fetchone():
                        continue

                    # 1. Tạo Quiz
                    sql_quiz = """
                        INSERT INTO mdl_quiz (course, name, intro, introformat, timecreated, timemodified, 
                        attempts, grademethod, decimalpoints, sumgrades, grade, questionsperpage)
                        VALUES (%s, %s, %s, 1, %s, %s, 0, 1, 2, 0, 10, 1)
                    """
                    cursor.execute(sql_quiz, (COURSE_ID, quiz_name, f"Kiểm tra bài: {lesson['name']}", now, now))
                    new_quiz_id = cursor.lastrowid

                    # 2. Tạo Course Module
                    sql_cm = "INSERT INTO mdl_course_modules (course, module, instance, section, added) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(sql_cm, (COURSE_ID, quiz_module_id, new_quiz_id, lesson['section_id'], now))
                    new_cm_id = cursor.lastrowid

                    # 3. Xếp vị trí ngay sau bài học
                    cursor.execute("SELECT sequence FROM mdl_course_sections WHERE id = %s", (lesson['section_id'],))
                    current_seq_str = cursor.fetchone()['sequence']
                    if current_seq_str:
                        seq_list = current_seq_str.split(',')
                        if str(lesson['cmid']) in seq_list:
                            idx = seq_list.index(str(lesson['cmid']))
                            seq_list.insert(idx + 1, str(new_cm_id))
                            cursor.execute("UPDATE mdl_course_sections SET sequence = %s WHERE id = %s", (",".join(seq_list), lesson['section_id']))

                    # 4. Tạo Context (Sử dụng INSERT IGNORE để tuyệt đối không dừng do lỗi trùng)
                    sql_ctx = "INSERT IGNORE INTO mdl_context (contextlevel, instanceid, depth) VALUES (70, %s, 0)"
                    cursor.execute(sql_ctx, (new_quiz_id,))
                    
                    success_count += 1
                    if success_count % 10 == 0:
                        print(f"⏳ Đang xử lý... Đã tạo xong {success_count} bài.")
                    
                    conn.commit()

                except Exception as inner_e:
                    print(f"⚠️ Cảnh báo tại bài '{lesson['name']}': {inner_e}")
                    conn.rollback()
                    continue

            print(f"\n🚀 HOÀN TẤT! Đã tạo thành công {success_count} bài Quiz mới.")

    except Exception as e:
        print(f"❌ Lỗi hệ thống: {e}")
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    fix_and_create_quizzes()