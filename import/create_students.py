import pymysql
import hashlib
import time

# 1. CẤU HÌNH KẾT NỐI (Lấy chuẩn từ config.php của bạn)
db_config = {
    "host": "127.0.0.1",
    "user": "root",
    "password": "",
    "database": "lophocdhs", #
    "port": 3307,             #
    "charset": "utf8mb4"
}

def create_students():
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        print("--- 👤 ĐANG BẮT ĐẦU TẠO 10 SINH VIÊN ẢO ---")

        # Tìm ID của phương thức đăng ký thủ công (manual enrol) cho khóa học C++ (Course ID 3)
        cursor.execute("SELECT id FROM mdl_enrol WHERE courseid = 3 AND enrol = 'manual'")
        enrol_res = cursor.fetchone()
        
        if not enrol_res:
            print("❌ Lỗi: Không tìm thấy phương thức đăng ký thủ công cho Khóa học 3.")
            return
        
        enrol_id = enrol_res[0]

        for i in range(1, 11):
            username = f"sv{i:02d}"
            email = f"{username}@student.edu.vn"
            firstname = "Sinh viên"
            lastname = f"Thứ {i:02d}"
            
            # Mật khẩu mặc định: Student123@ (Moodle dùng MD5 đơn giản cho manual import nếu cần)
            password_hash = hashlib.md5("Student123@".encode()).hexdigest()

            # A. Chèn sinh viên vào bảng mdl_user
            sql_user = """
                INSERT IGNORE INTO mdl_user 
                (auth, confirmed, username, password, firstname, lastname, email, city, country, lang, timezone, timecreated) 
                VALUES ('manual', 1, %s, %s, %s, %s, %s, 'Hue', 'VN', 'vi', '99', %s)
            """
            cursor.execute(sql_user, (username, password_hash, firstname, lastname, email, int(time.time())))
            
            # Lấy ID của user vừa tạo
            cursor.execute("SELECT id FROM mdl_user WHERE username = %s", (username,))
            user_id = cursor.fetchone()[0]

            # B. Đăng ký sinh viên vào khóa học (Ghi danh)
            sql_enrol = """
                INSERT IGNORE INTO mdl_user_enrolments 
                (enrolid, userid, status, timestart, timecreated, timemodified) 
                VALUES (%s, %s, 0, %s, %s, %s)
            """
            now = int(time.time())
            cursor.execute(sql_enrol, (enrol_id, user_id, now, now, now))
            
            print(f"✅ Đã tạo & Ghi danh: {username} (User ID: {user_id})")

        conn.commit()
        print("\n🚀 THÀNH CÔNG! 10 sinh viên đã sẵn sàng trong hệ thống.")

    except Exception as e:
        print(f"⚠️ Lỗi kỹ thuật: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    create_students()