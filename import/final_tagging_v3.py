import pymysql
import time

# === 1. THÔNG TIN CẤU HÌNH (Đã khớp với XAMPP của bạn) ===
db_config = {
    "host": "127.0.0.1", "user": "root", "password": "",
    "database": "lophocdhs", "port": 3307, "charset": "utf8mb4"
}

# === 2. MÃ GENE CHUẨN (Vừa tìm thấy từ thẻ TEST_GENE) ===
COMP = 'core'
ITYPE = 'course_modules'

# === 3. FULL MAPPING 108 BÀI HỌC ===
TAGS_MAP = {
    # Phần 1: Giới thiệu
    "Bài 1 : Đề Cương - Thành Thạo Cpp qua 108 bài học": ["cpp_basic", "overview", "syllabus"],
    "Bài 2 : Giới thiệu về C++": ["cpp_basic", "history"],
    "Bài 3 : Một số công cụ lập trình C++ và cách sử dụng": ["setup", "ide", "compiler"],
    "Bài 4 : Chương trình C++ đầu tiên": ["syntax", "hello_world"],
    "Bài 5 : Ý nghĩa của cout và cin trong C++": ["io_stream", "syntax"],
    "Bài 6 : Các ký tự đặc biệt": ["syntax", "special_characters"],
    # Phần 2: Khái niệm cơ bản
    "Bài 7 : Các loại ghi chú trong C++": ["syntax", "comments"],
    "Bài 8 : Kiểu dữ liệu, định danh và khai báo biến": ["data_types", "variables"],
    "Bài 9 : Hằng số và biểu thức": ["constants", "expressions"],
    "Bài 10 : Chuyển kiểu dữ liệu": ["type_casting"],
    "Bài 11 : Các toán tử trong C++": ["operators", "arithmetic"],
    "Bài 12 : Bài tập rèn luyện - Tính chu vi diện tích Hình tròn": ["exercise", "math"],
    "Bài 13 : Bài tập rèn luyện - Tính chu vi diện tích Tam Giác": ["exercise", "math"],
    "Bài 14 : Bài tập rèn luyện - Các hàm lượng giác": ["math_functions"],
    "Bài 15 : Bài tập rèn luyện - Tính giờ phút giây": ["exercise", "logic"],
    "Bài 16 : Bài tập rèn luyện - Tính điểm trung bình": ["exercise", "math"],
    "Bài 17 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 3: Rẽ nhánh
    "Bài 18 : Câu lệnh If": ["control_flow", "if_condition"],
    "Bài 19 : Câu lệnh if ... else": ["control_flow", "if_else"],
    "Bài 20 : Câu lệnh If ... else lồng nhau": ["control_flow", "nested_if"],
    "Bài 21 : Toán tử 3 ngôi và câu lệnh if ... else": ["ternary_operator"],
    "Bài 22 : Câu lệnh switch": ["control_flow", "switch_case"],
    "Bài 23 : Bài tập rèn luyện-giải phương trình bậc 1": ["exercise", "algorithm"],
    "Bài 24 : Bài tập rèn luyện-giải phương trình bậc 2": ["exercise", "algorithm"],
    "Bài 25 : Bài tập rèn luyện-tính tiêu thụ điện": ["exercise", "logic"],
    "Bài 26 : Bài tập rèn luyện-tính toán số học": ["exercise", "math"],
    "Bài 27 : Bài tập rèn luyện-tính chu vi diện tích tam giác": ["exercise", "algorithm"],
    "Bài 28 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 4: Vòng lặp
    "Bài 29 : Vòng while": ["loops", "while_loop"],
    "Bài 30 : Vòng do... while": ["loops", "do_while"],
    "Bài 31 : Vòng for": ["loops", "for_loop"],
    "Bài 32 : Câu lệnh break": ["loops", "break"],
    "Bài 33 : Câu lệnh continue": ["loops", "continue"],
    "Bài 34 : Bàn về vòng lặp lồng nhau": ["loops", "nested_loops"],
    "Bài 35 : Bài tập rèn luyện-Tính dãy số": ["exercise", "loops"],
    "Bài 36 : Bài tập rèn luyện-Số hoàn thiện": ["exercise", "loops"],
    "Bài 37 : Bài tập rèn luyện-Tổng các chữ số trong 1 số": ["exercise", "loops"],
    "Bài 38 : Bài tập rèn luyện-Game đoán số": ["exercise", "game_logic"],
    "Bài 39 : Bài tập rèn luyện-Vẽ Hình": ["exercise", "loops"],
    "Bài 40 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 5: Mảng
    "Bài 41 : Khái niệm về mảng và cách khai báo": ["arrays", "declaration"],
    "Bài 42 : Truy suất và thao tác trên mảng 1 chiều": ["arrays", "1d_array"],
    "Bài 43 : Tìm kiếm trên mảng 1 chiều": ["arrays", "searching"],
    "Bài 44 : Sắp xếp mảng 1 chiều": ["arrays", "sorting"],
    "Bài 45 : Cách khai báo mảng 2 chiều": ["arrays", "2d_array"],
    "Bài 46 : Truy suất và thao tác trên mảng 2 chiều": ["arrays", "2d_array"],
    "Bài 47 : Bài tập rèn luyện -xử lý mảng 1": ["exercise", "arrays"],
    "Bài 48 : Bài tập rèn luyện -xử lý mảng 2": ["exercise", "arrays"],
    "Bài 49 : Bài tập rèn luyện -xử lý mảng 3": ["exercise", "arrays"],
    "Bài 50 : Bài tập rèn luyện -xử lý mảng 4": ["exercise", "arrays"],
    "Bài 51 : Bài tập rèn luyện -xử lý mảng 5": ["exercise", "arrays"],
    "Bài 52 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 6: Hàm
    "Bài 53 : Khái niệm và cách sử dụng hàm": ["functions", "modular"],
    "Bài 54 : Nguyên tắc hoạt động của hàm": ["functions", "execution_flow"],
    "Bài 55 : Tham số hình thức và tham số thực": ["functions", "parameters"],
    "Bài 56 : Truyền tham trị và tham biến": ["functions", "memory"],
    "Bài 57 : Parameter mặc định": ["functions"],
    "Bài 58 : Giới thiệu về hàm đệ qui": ["recursion", "stack"],
    "Bài 59 : Bài tập rèn luyện-PT Bậc 2": ["exercise", "functions"],
    "Bài 60 : Bài tập rèn luyện-Xử lý mảng bằng hàm": ["exercise", "functions", "arrays"],
    "Bài 61 : Bài tập rèn luyện-Xử lý dãy Fibonacci": ["exercise", "recursion"],
    "Bài 62 : Bài tập rèn luyện-Chu vi diện tích tam giác": ["exercise", "functions"],
    "Bài 63 : Bài tập rèn luyện-Hàm chơi Game đoán số": ["exercise", "functions", "game_logic"],
    "Bài 64 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 7: Con trỏ
    "Bài 65 : Khái niệm con trỏ & biến con trỏ": ["pointers", "memory_address"],
    "Bài 66 : Các Toán tử con trỏ": ["pointers", "dereferencing"],
    "Bài 67 : Các thao tác trên con trỏ": ["pointers", "manipulation"],
    "Bài 68 : Con trỏ void và con trỏ null": ["pointers", "safety"],
    "Bài 69 : Con trỏ và mảng": ["pointers", "arrays"],
    "Bài 70 : Mảng Con trỏ": ["pointers", "array_of_pointers"],
    "Bài 71 : Tương quan giữa Mảng 2 chiều và con trỏ cấp 2": ["pointers", "2d_array"],
    "Bài 72 : Bài tập rèn luyện-con trỏ 1": ["exercise", "pointers"],
    "Bài 73 : Bài tập rèn luyện-con trỏ 2": ["exercise", "pointers"],
    "Bài 74 : Bài tập rèn luyện-con trỏ 3": ["exercise", "pointers"],
    "Bài 75 : Bài tập rèn luyện-con trỏ 4": ["exercise", "pointers"],
    "Bài 76 : Bài tập rèn luyện-con trỏ 5": ["exercise", "pointers"],
    "Bài 77 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 8: Chuỗi
    "Bài 78 : Khái niệm và cấu trúc của chuỗi": ["strings", "char_array"],
    "Bài 79 : Cách nhập chuỗi-xuất chuỗi": ["strings", "io_stream"],
    "Bài 80 : Hàm strcpy,strncpy - sao chép chuỗi": ["strings", "functions"],
    "Bài 81 : Hàm strcat,strncat - nối chuỗi": ["strings", "functions"],
    "Bài 82 : Hàm strchr,strstr - tìm ký tự, chuỗi": ["strings", "searching"],
    "Bài 83 : Hàm strcmp,strncmp - so sánh chuỗi": ["strings", "comparison"],
    "Bài 84 : Hàm toUpper-ToLower- In Hoa, Thường": ["strings", "conversion"],
    "Bài 85 : Bài tập rèn luyện - chuỗi 1": ["exercise", "strings"],
    "Bài 86 : Bài tập rèn luyện - chuỗi 2": ["exercise", "strings"],
    "Bài 87 : Bài tập rèn luyện - chuỗi 3": ["exercise", "strings"],
    "Bài 88 : Bài tập rèn luyện - chuỗi 4": ["exercise", "strings"],
    "Bài 89 : Bài tập rèn luyện - chuỗi 5": ["exercise", "strings"],
    "Bài 90 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 9: Struct
    "Bài 91 : Khái niệm và cách khai báo cấu trúc": ["struct", "custom_types"],
    "Bài 92 : Truy cập các thành viên của biến cấu trúc": ["struct", "member_access"],
    "Bài 93 : Lệnh gán cấu trúc": ["struct", "assignment"],
    "Bài 94 : Mảng cấu trúc": ["struct", "arrays"],
    "Bài 95 : Con trỏ cấu trúc": ["struct", "pointers"],
    "Bài 96 : Bài tập rèn luyện-Cấu trúc nhân viên": ["exercise", "struct"],
    "Bài 97 : Bài tập rèn luyện-Cấu trúc điểm": ["exercise", "struct"],
    "Bài 98 : Bài tập rèn luyện-Cấu trúc phân số": ["exercise", "struct"],
    "Bài 99 : Các bài tập tự rèn luyện": ["self_practice"],
    # Phần 10: Tập tin
    "Bài 100 : Khái niệm về tập tin": ["file_io", "data_persistence"],
    "Bài 101 : cách ghi tập tin text file": ["file_io", "writing"],
    "Bài 102 : Cách đọc tập tin text file": ["file_io", "reading"],
    "Bài 103 : Cách ghi cấu trúc xuống tập tin": ["file_io", "serialization"],
    "Bài 104 : Cách đọc cấu trúc từ tập tin": ["file_io", "deserialization"],
    "Bài 105 : Bài tập rèn luyện-lưu và đọc dãy số": ["exercise", "file_io"],
    "Bài 106 : Bài tập rèn luyện-lưu và đọc danh sách Sinh Viên": ["exercise", "file_io"],
    "Bài 107 : Bài tập rèn luyện-lưu và đọc danh sách Sản phẩm": ["exercise", "file_io"],
    "Bài 108 : Các bài tập tự rèn luyện": ["self_practice"]
}

def run_fix():
    print("--- 🛠 BẮT ĐẦU ĐỒNG BỘ 108 BÀI VỚI MÃ GENE MỚI ---")
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        
        # Xóa sạch liên kết cũ để tránh rác
        cursor.execute(f"DELETE FROM mdl_tag_instance WHERE component = '{COMP}'")
        
        updated = 0
        for lesson_name, tags in TAGS_MAP.items():
            # Bước 1: Lấy CMID (Course Module ID) thay vì Instance ID
            sql_find = """
                SELECT cm.id, ctx.id as contextid 
                FROM mdl_page p
                JOIN mdl_course_modules cm ON p.id = cm.instance
                JOIN mdl_context ctx ON cm.id = ctx.instanceid
                WHERE p.name = %s AND p.course = 3 AND ctx.contextlevel = 70
            """
            cursor.execute(sql_find, (lesson_name.strip(),))
            res = cursor.fetchone()
            
            if res:
                cmid, context_id = res
                print(f"✅ Đang xử lý: {lesson_name} (CMID: {cmid})")
                for t_name in tags:
                    cursor.execute("INSERT IGNORE INTO mdl_tag (userid, name, rawname, tagcollid) VALUES (2, %s, %s, 1)", (t_name.lower(), t_name))
                    cursor.execute("SELECT id FROM mdl_tag WHERE name = %s", (t_name.lower(),))
                    tag_id = cursor.fetchone()[0]
                    
                    # Gán nhãn vào CMID (Itemid = cmid) theo gene chuẩn
                    cursor.execute(f"""
                        INSERT INTO mdl_tag_instance 
                        (tagid, component, itemtype, itemid, contextid, ordering, timecreated) 
                        VALUES (%s, '{COMP}', '{ITYPE}', %s, %s, 0, %s)
                    """, (tag_id, cmid, context_id, int(time.time())))
                updated += 1
        
        conn.commit()
        print(f"\n🚀 THÀNH CÔNG! Đã khớp {updated}/108 bài vào giao diện.")
    except Exception as e:
        print(f"❌ Lỗi: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_fix()