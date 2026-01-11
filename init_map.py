import os
import django

# Thiết lập môi trường Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendation_system.settings')
django.setup()

from dashboard.models import KnowledgeMap, SystemConfig

def initialize():
    # 1. Danh sách ánh xạ 10 chương + Bài đầu vào (Dựa trên dữ liệu thực tế của bạn)
    knowledge_data = [
        (3, 'Kiểm tra đầu vào', 'Logic căn bản', 1),
        (12, 'Phần 1: Nhập môn C++', 'Cú pháp & Nhập xuất', 1),
        (4, 'Phần 2: Biến & Kiểu dữ liệu', 'Kiểu dữ liệu', 1),
        (5, 'Phần 3: Toán tử', 'Toán tử & Biểu thức', 2),
        (6, 'Phần 4: Cấu trúc rẽ nhánh', 'Câu lệnh điều kiện', 2),
        (7, 'Phần 5: Vòng lặp', 'Cấu trúc lặp', 2),
        (8, 'Phần 6: Mảng (Arrays)', 'Mảng & Bộ nhớ', 2),
        (9, 'Phần 7: Chuỗi ký tự (Strings)', 'Xử lý văn bản', 2),
        (10, 'Phần 8: Hàm (Functions)', 'Tư duy module', 3),
        (11, 'Phần 9: Con trỏ (Pointers)', 'Quản lý bộ nhớ', 3),
        (13, 'Phần 10: Lập trình hướng đối tượng', 'Tư duy hướng đối tượng', 3),
    ]

    print(">>> Đang nạp Bản đồ kiến thức...")
    for m_id, name, skill, diff in knowledge_data:
        KnowledgeMap.objects.update_or_create(
            moodle_quiz_id=m_id,
            defaults={'chapter_name': name, 'skill_tag': skill, 'difficulty_level': diff}
        )

    # 2. Khởi tạo cấu hình hệ thống (Mặc định Alpha = 0.5) [cite: 381]
    SystemConfig.objects.get_or_create(id=1, defaults={'hybrid_alpha': 0.5})
    
    print("===> HOÀN THÀNH: Bản đồ kiến thức đã sẵn sàng!")

if __name__ == '__main__':
    initialize()