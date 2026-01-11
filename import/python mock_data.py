import pymysql
import random
import time

# Danh sach ID Quiz ban vua chup
quiz_ids = [3, 12, 4, 5, 6, 7, 8, 9, 10, 11, 13]

try:
    connection = pymysql.connect(
        host='localhost', user='root', password='',
        database='lophocdhs', port=3307
    )
    with connection.cursor() as cursor:
        # 1. Lay danh sach ID cua 25 sinh vien
        cursor.execute("SELECT id, username FROM mdl_user WHERE username LIKE 'sv%'")
        students = cursor.fetchall()

        print(f"--- DANG BOM DIEM CHO {len(students)} SINH VIEN ---")

        for student_id, username in students:
            # Chia nhom nang luc
            sv_num = int(username.replace('sv', ''))
            if sv_num <= 8:
                range_score = (8, 10) # Nhom gioi
            elif sv_num <= 18:
                range_score = (5, 8)  # Nhom kha
            else:
                range_score = (2, 5)  # Nhom yeu

            for q_id in quiz_ids:
                score = round(random.uniform(range_score[0], range_score[1]), 2)
                
                # Xoa diem cu neu co de tranh trung lap
                cursor.execute("DELETE FROM mdl_grade_grades WHERE itemid = %s AND userid = %s", (q_id, student_id))
                
                # Chen diem moi vao cac cot chuan cua Moodle
                sql = """
                INSERT INTO mdl_grade_grades 
                (itemid, userid, rawgrade, finalgrade, timemodified, timecreated) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                current_time = int(time.time())
                cursor.execute(sql, (q_id, student_id, score, score, current_time, current_time))
        
        connection.commit()
        print("===> XONG! Da nap du lieu diem so thanh cong.")

    connection.close()
except Exception as e:
    print(f"Loi: {e}")