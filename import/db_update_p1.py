import pymysql  # Đã chuyển từ mysql.connector sang pymysql
import sys

# --- CẤU HÌNH DATABASE (Đã khớp theo XAMPP Port 3307 của Khánh) ---
db_config = {
    'host': 'localhost',
    'user': 'root',      
    'password': '',      
    'database': 'lophocdhs', 
    'port': 3307,
    'charset': 'utf8mb4'
}

p1_data = {
    7: {"desc": "Lộ trình chi tiết 108 bài học để trở thành chuyên gia C++.", "obj": "roadmap, syllabus, overview"},
    8: {"desc": "Tìm hiểu tại sao C++ lại mạnh mẽ và các ứng dụng thực tế.", "obj": "cpp_intro, history, features"},
    9: {"desc": "Hướng dẫn cài đặt IDE (VS Code, Visual Studio) và Compiler.", "obj": "tools, ide, compiler, setup"},
    10: {"desc": "Viết code Hello World và giải thích cấu trúc cơ bản.", "obj": "syntax, main_function, basic_structure"},
    12: {"desc": "Làm chủ cơ chế nhập xuất dữ liệu màn hình.", "obj": "iostream, cin, cout, stream"},
    13: {"desc": "Cách sử dụng các ký tự điều khiển như \\n, \\t.", "obj": "formatting, escape_sequences, syntax"}
}

def update_via_db():
    conn = None
    try:
        print(f"--- Đang khởi động kết nối tới {db_config['database']} (Port: {db_config['port']}) ---")
        
        # Kết nối bằng PyMySQL - Không bị sập trên Python 3.13
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        print("✅ Kết nối thành công! Đang cập nhật dữ liệu...")
        
        for cmid, content in p1_data.items():
            full_intro = f"{content['desc']}<br><b>Mục tiêu:</b> {content['obj']}"
            
            # Cập nhật bảng mdl_page
            query = """
                UPDATE mdl_page p
                JOIN mdl_course_modules cm ON p.id = cm.instance
                SET p.intro = %s
                WHERE cm.id = %s
            """
            cursor.execute(query, (full_intro, cmid))
            print(f"   + Đã cập nhật Bài ID: {cmid}")
            
        conn.commit()
        print("\n" + "="*40)
        print("🎉 KẾT QUẢ: Đã cập nhật xong Chương 1!")
        print("="*40)
        
    except Exception as err:
        print(f"❌ Lỗi: {err}")
    finally:
        if conn:
            conn.close()
            print("🔌 Đã đóng kết nối Database.")

if __name__ == "__main__":
    update_via_db()