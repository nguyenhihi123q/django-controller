import mysql.connector
import sys

# In ra ngay để kiểm tra Python có chạy không
print("--- KHỞI ĐỘNG KIỂM TRA ---")

try:
    # Thử kết nối thẳng vào cổng 3307
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='lophocdhs',
        port=3307
    )
    
    if conn.is_connected():
        print("✅ KẾT NỐI THÀNH CÔNG CỔNG 3307!")
        cursor = conn.cursor()
        
        # Kiểm tra xem Database có dữ liệu không
        cursor.execute("SELECT COUNT(*) FROM mdl_course")
        row_count = cursor.fetchone()[0]
        print(f"📊 Tìm thấy {row_count} khóa học trong Database.")
        
        conn.close()
    else:
        print("❌ Kết nối thất bại mà không có báo lỗi.")

except mysql.connector.Error as err:
    print(f"❌ Lỗi MySQL: {err}")
except Exception as e:
    print(f"❌ Lỗi hệ thống: {e}")

print("--- KẾT THÚC KIỂM TRA ---")