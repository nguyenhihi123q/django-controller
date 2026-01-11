import pymysql
import random
import time

try:
    connection = pymysql.connect(
        host='localhost', user='root', password='',
        database='lophocdhs', port=3307
    )
    with connection.cursor() as cursor:
        # 1. Lấy danh sách 25 sinh viên và 11 bài Quiz (đã có từ trước)
        cursor.execute("SELECT id, username FROM mdl_user WHERE username LIKE 'sv%'")
        students = cursor.fetchall()
        
        # ID của các bài Quiz chúng ta đã biết
        quiz_ids = [3, 12, 4, 5, 6, 7, 8, 9, 10, 11, 13]

        print("--- ĐANG TẠO KỊCH BẢN HÀNH VI CHO 25 SINH VIÊN ---")

        for student_id, username in students:
            sv_num = int(username.replace('sv', ''))
            
            # CHIA KỊCH BẢN
            if sv_num <= 5: # NHÓM 1: HỌC NHẢY CÓC (Skipper)
                # Chỉ hoàn thành chương 1, 2 nhưng lại click vào chương 10
                completed_quizzes = [3, 12, 4] 
                view_count_logic = lambda q: 50 if q == 13 else random.randint(1, 5)
                feedback = 3 # Khó
            
            elif sv_num <= 10: # NHÓM 2: CẦN CÙ NHƯNG YẾU (Struggler)
                completed_quizzes = quiz_ids[:6]
                view_count_logic = lambda q: random.randint(20, 40) # Xem rất nhiều lần
                feedback = 3 # Khó
            
            else: # NHÓM 3: HỌC TỐT/BÌNH THƯỜNG
                completed_quizzes = quiz_ids
                view_count_logic = lambda q: random.randint(2, 8)
                feedback = random.choice([1, 2]) # Dễ hoặc Vừa

            # NẠP DỮ LIỆU VÀO CÁC BẢNG CỦA MOODLE
            for q_id in quiz_ids:
                v_count = view_count_logic(q_id)
                
                # A. Nạp Cảm nhận (Choice) - Giả sử ID choice cho mỗi chương là q_id + 100
                # (Trong thực tế bạn cần check ID choice chuẩn, ở đây ta giả lập để lấy data cho Django)
                cursor.execute("REPLACE INTO mdl_choice_answers (choiceid, userid, optionid, timemodified) VALUES (%s, %s, %s, %s)", 
                               (q_id, student_id, feedback, int(time.time())))

                # B. Nạp Tiến độ hoàn thành (Completion)
                status = 1 if q_id in completed_quizzes else 0
                cursor.execute("REPLACE INTO mdl_course_modules_completion (coursemoduleid, userid, completionstate, timemodified) VALUES (%s, %s, %s, %s)",
                               (q_id, student_id, status, int(time.time())))

                # C. Nạp Nhật ký hành vi (Logs) - Mô phỏng lượt click
                for _ in range(v_count):
                    cursor.execute("""
                        INSERT INTO mdl_logstore_standard_log 
                        (eventname, component, action, target, objectid, userid, courseid, timecreated, contextid, contextlevel, contextinstanceid)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, ('\\core\\event\\course_module_viewed', 'mod_quiz', 'viewed', 'course_module', q_id, student_id, 3, int(time.time()), 1, 50, q_id))

        connection.commit()
        print("===> XONG! Đã nạp kịch bản hành vi. Bây giờ dữ liệu đã đủ 'xấu' và 'tốt' để thuật toán phân tích.")

    connection.close()
except Exception as e:
    print(f"Loi: {e}")