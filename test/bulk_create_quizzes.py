import requests
import time
import json

# ==============================================================================
# CẤU HÌNH
# ==============================================================================
BRIDGE_URL    = "http://localhost/lophocthaynguyendhs/khanh_moodle_bridge.php"
SECRET_KEY    = "KHANH_CPP_2026"
COURSE_ID     = 3        
TEMPLATE_CMID = 551     # <--- ID Template mới của sếp (theo ảnh log sếp gửi là 549)

# DANH SÁCH BÀI (Giữ nguyên tên bài sếp muốn)
lessons_list = [
    # --- PHẦN 5: MẢNG (ARRAYS) ---
    {"after_cmid": 48, "name": "bài test bài Bài 41 : Khái niệm về mảng và cách khai báo"},
    {"after_cmid": 49, "name": "bài test bài Bài 42 : Truy suất và thao tác trên mảng 1 chiều"},
    {"after_cmid": 50, "name": "bài test bài Bài 43 : Tìm kiếm trên mảng 1 chiều"},
    {"after_cmid": 51, "name": "bài test bài Bài 44 : Sắp xếp mảng 1 chiều"},
    {"after_cmid": 52, "name": "bài test bài Bài 45 : Cách khai báo mảng 2 chiều"},
    {"after_cmid": 53, "name": "bài test bài Bài 46 : Truy suất và thao tác trên mảng 2 chiều"},
    {"after_cmid": 130, "name": "bài test bài Hệ thống kiến thức Phần 5: Mảng (Arrays)"},

    # --- PHẦN 6: HÀM (FUNCTIONS) ---
    {"after_cmid": 60, "name": "bài test bài Bài 53 : Khái niệm và cách sử dụng hàm"},
    {"after_cmid": 61, "name": "bài test bài Bài 54 : Nguyên tắc hoạt động của hàm"},
    {"after_cmid": 62, "name": "bài test bài Bài 55 : Tham số hình thức và tham số thực"},
    {"after_cmid": 63, "name": "bài test bài Bài 56 : Truyền tham trị và tham biến"},
    {"after_cmid": 64, "name": "bài test bài Bài 57 : Parameter mặc định"},
    {"after_cmid": 65, "name": "bài test bài Bài 58 : Giới thiệu về hàm đệ qui"},
    {"after_cmid": 133, "name": "bài test bài Hệ thống kiến thức Phần 6: Hàm (Functions)"},

    # --- PHẦN 7: CON TRỎ (POINTERS) ---
    {"after_cmid": 72, "name": "bài test bài Bài 65 : Khái niệm con trỏ & biến con trỏ"},
    {"after_cmid": 73, "name": "bài test bài Bài 65 : Khái niệm con trỏ & biến con trỏ (Part 2)"}, 
    {"after_cmid": 74, "name": "bài test bài Bài 66 : Các Toán tử con trỏ"},
    {"after_cmid": 75, "name": "bài test bài Bài 67 : Các thao tác trên con trỏ"},
    {"after_cmid": 76, "name": "bài test bài Bài 68 : Con trỏ void và con trỏ null"},
    {"after_cmid": 77, "name": "bài test bài Bài 69 : Con trỏ và mảng"},
    {"after_cmid": 78, "name": "bài test bài Bài 70 : Mảng Con trỏ"},
    {"after_cmid": 79, "name": "bài test bài Bài 71 : Tương quan giữa Mảng 2 chiều và con trỏ cấp 2"},
    {"after_cmid": 136, "name": "bài test bài Hệ thống kiến thức Phần 7: Con trỏ (Pointers)"},

    # --- PHẦN 8: CHUỖI KÝ TỰ (STRINGS) ---
    {"after_cmid": 86, "name": "bài test bài Bài 78 : Khái niệm và cấu trúc của chuỗi"},
    {"after_cmid": 87, "name": "bài test bài Bài 79 : Cách nhập chuỗi-xuất chuỗi"},
    {"after_cmid": 88, "name": "bài test bài Bài 80 : Hàm strcpy,strncpy - sao chép chuỗi"},
    {"after_cmid": 89, "name": "bài test bài Bài 81 : Hàm strcat,strncat - nối chuỗi"},
    {"after_cmid": 90, "name": "bài test bài Bài 82 : Hàm strchr,strstr - tìm ký tự, chuỗi"},
    {"after_cmid": 91, "name": "bài test bài Bài 83 : Hàm strcmp,strncmp - so sánh chuỗi"},
    {"after_cmid": 92, "name": "bài test bài Bài 84 : Hàm toUpper-ToLower- In Hoa, Thường"},
    {"after_cmid": 139, "name": "bài test bài Hệ thống kiến thức Phần 8: Chuỗi ký tự (Strings)"},

    # --- PHẦN 9: STRUCT (CẤU TRÚC) ---
    {"after_cmid": 99, "name": "bài test bài Bài 91 : Khái niệm và cách khai báo cấu trúc"},
    {"after_cmid": 100, "name": "bài test bài Bài 92 : Truy cập các thành viên của biến cấu trúc"},
    {"after_cmid": 101, "name": "bài test bài Bài 93 : Lệnh gán cấu trúc"},
    {"after_cmid": 102, "name": "bài test bài Bài 94 : Mảng cấu trúc"},
    {"after_cmid": 103, "name": "bài test bài Bài 95 : Con trỏ cấu trúc"},
    {"after_cmid": 142, "name": "bài test bài Hệ thống kiến thức Phần 9: Kiểu dữ liệu cấu trúc (Struct)"},

    # --- PHẦN 10: FILES (TẬP TIN) ---
    {"after_cmid": 108, "name": "bài test bài Bài 100 : Khái niệm về tập tin"},
    {"after_cmid": 109, "name": "bài test bài Bài 101 : cách ghi tập tin text file"},
    {"after_cmid": 110, "name": "bài test bài Bài 102 : Cách đọc tập tin text file"},
    {"after_cmid": 111, "name": "bài test bài Bài 103 : Cách ghi cấu trúc xuống tập tin"},
    {"after_cmid": 112, "name": "bài test bài Bài 104 : Cách đọc cấu trúc từ tập tin"},
    {"after_cmid": 145, "name": "bài test bài Hệ thống kiến thức Phần 10: Thao tác với Tập tin (Files)"}
]

print(f"🚀 BẮT ĐẦU CHIẾN DỊCH TẠO QUIZ (BẢN SQL HARDCORE)...")
print(f"👉 Template ID: {TEMPLATE_CMID}")

for i, lesson in enumerate(lessons_list):
    print(f"[{i+1}] {lesson['name']} (Sau CMID {lesson['after_cmid']})...", end=" ")
    
    payload = {
        'key': SECRET_KEY,
        'courseid': COURSE_ID,
        'template_cmid': TEMPLATE_CMID,
        'after_cmid': lesson['after_cmid'],
        'new_name': lesson['name']
    }

    try:
        response = requests.post(BRIDGE_URL, data=payload)
        
        # Kiểm tra phản hồi
        try:
            res = response.json()
            if res.get('status') == 'success':
                print(f"✅ OK! (ID: {res.get('new_cmid')})")
            else:
                print(f"❌ Lỗi Moodle: {res.get('message')}")
        except json.JSONDecodeError:
            # Nếu PHP chết giữa đường và trả về HTML lỗi
            print(f"\n   ☠️ PHP CRASHED! Nội dung trả về:")
            print(response.text[:300]) # In 300 ký tự đầu để soi lỗi

    except Exception as e:
        print(f"\n   ❌ Lỗi kết nối: {e}")
    
    time.sleep(1) # Nghỉ 1 giây cho Database thở

print("-" * 50)
print("🏁 Đã xong! Sếp F5 Moodle kiểm tra lại nhé.")