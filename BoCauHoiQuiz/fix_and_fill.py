import requests
import json
import time

# CẤU HÌNH
BRIDGE_URL = "http://localhost/lophocthaynguyendhs/khanh_question_bridge.php"
KEY = "KHANH_CPP_2026"
COURSE_ID = 3

# Tên bài Quiz (Sếp nhớ để chính xác như lần trước)
TARGET_QUIZ_NAME = "bài test bài Giới thiệu về C++"

# DỮ LIỆU CÂU HỎI (Copy từ file trước)
questions_data = [
    {
        "content": "<p>Ai là người đã phát triển ngôn ngữ lập trình C++?</p>",
        "answers": ["Dennis Ritchie", "Bjarne Stroustrup", "James Gosling", "Guido van Rossum"],
        "correct_index": 1
    },
    {
        "content": "<p>C++ là ngôn ngữ lập trình thuộc loại nào?</p>",
        "answers": ["Hướng thủ tục", "Hướng đối tượng", "Đa mô hình (Multi-paradigm)", "Kịch bản"],
        "correct_index": 2
    },
    {
        "content": "<p>Đuôi file mặc định của C++ là gì?</p>",
        "answers": [".c", ".cpp", ".py", ".java"],
        "correct_index": 1
    },
    {
        "content": "<p>Hàm chính để chạy chương trình C++ tên là gì?</p>",
        "answers": ["start()", "program()", "main()", "init()"],
        "correct_index": 2
    },
    {
        "content": "<p>Lệnh in ra màn hình trong C++?</p>",
        "answers": ["printf", "System.out.println", "cout", "print"],
        "correct_index": 2
    },
    {
        "content": "<p>Kết thúc câu lệnh trong C++ dùng dấu gì?</p>",
        "answers": ["; (Chấm phẩy)", ". (Chấm)", ", (Phẩy)", ": (Hai chấm)"],
        "correct_index": 0
    },
    {
        "content": "<p>Để sử dụng nhập xuất (cin/cout), ta cần thư viện nào?</p>",
        "answers": ["<math.h>", "<iostream>", "<stdio.h>", "<string>"],
        "correct_index": 1
    },
    {
        "content": "<p>IDE phổ biến để code C++?</p>",
        "answers": ["Photoshop", "Visual Studio", "Word", "Excel"],
        "correct_index": 1
    }
]

# --- QUY TRÌNH CHỮA LỖI VÀ NẠP LẠI ---

# 1. RESET (Xóa dữ liệu hỏng)
print(f"🧹 Đang Reset bài Quiz: '{TARGET_QUIZ_NAME}'...", end=" ")
try:
    res = requests.post(BRIDGE_URL, data={
        'key': KEY, 'courseid': COURSE_ID, 
        'quiz_name': TARGET_QUIZ_NAME, 
        'action': 'reset_quiz'
    }).json()
    
    if res['status'] == 'success':
        print("✅ OK!")
    else:
        print(f"❌ Lỗi: {res['message']}")
        exit() # Dừng nếu không reset được
except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")
    exit()

time.sleep(1) # Nghỉ chút cho DB hồi phục

# 2. NẠP LẠI (Dữ liệu chuẩn)
print(f"🚀 Đang nạp lại câu hỏi...", end=" ")
try:
    response = requests.post(BRIDGE_URL, data={
        'key': KEY, 'courseid': COURSE_ID, 
        'quiz_name': TARGET_QUIZ_NAME, 
        'action': 'add_questions',
        'questions_data': json.dumps(questions_data, ensure_ascii=False)
    })
    
    # --- ĐOẠN NÀY QUAN TRỌNG ĐỂ DEBUG ---
    try:
        res = response.json()
        if res['status'] == 'success':
            print(f"✅ THÀNH CÔNG! Đã nạp {res['count']} câu.")
        else:
            print(f"❌ Lỗi Logic: {res['message']}")
    except json.JSONDecodeError:
        print("\n❌ PHP BỊ CRASH! Đây là nội dung lỗi nhận được:")
        print("-" * 50)
        print(response.text) # In hết nội dung HTML ra để đọc lỗi
        print("-" * 50)

except Exception as e:
    print(f"❌ Lỗi kết nối: {e}")