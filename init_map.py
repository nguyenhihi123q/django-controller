import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendation_system.settings')
django.setup()

from dashboard.models import KnowledgeMap, SystemConfig

def initialize():
    # CHÚ Ý: Cập nhật ID theo đúng kết quả Terminal của bạn
    knowledge_data = [
        (1, 'Kiểm tra năng lực đầu vào', 'Logic căn bản', 1),
        (10, 'Phần 1: Nhập môn C++', 'Cú pháp & Nhập xuất', 1),
        (2, 'Phần 2: Biến & Kiểu dữ liệu', 'Kiểu dữ liệu', 1),
        (3, 'Phần 3: Toán tử', 'Toán tử & Biểu thức', 2),
        (4, 'Phần 4: Cấu trúc rẽ nhánh', 'Câu lệnh điều kiện', 2),
        (5, 'Phần 5: Vòng lặp', 'Cấu trúc lặp', 2),
        (6, 'Phần 6: Mảng (Arrays)', 'Mảng & Bộ nhớ', 2),
        (7, 'Phần 7: Chuỗi ký tự (Strings)', 'Xử lý văn bản', 2),
        (8, 'Phần 8: Hàm (Functions)', 'Tư duy module', 3),
        (9, 'Phần 9: Con trỏ (Pointers)', 'Quản lý bộ nhớ', 3),
        (11, 'Phần 10: Lập trình hướng đối tượng', 'Tư duy hướng đối tượng', 3),
    ]

    print(">>> Đang cập nhật Bản đồ kiến thức với ID thực tế...")
    # Xóa dữ liệu cũ sai ID để nạp lại cho sạch
    KnowledgeMap.objects.all().delete()
    
    for m_id, name, skill, diff in knowledge_data:
        KnowledgeMap.objects.create(
            moodle_quiz_id=m_id,
            chapter_name=name,
            skill_tag=skill,
            difficulty_level=diff
        )

    SystemConfig.objects.get_or_create(id=1, defaults={'hybrid_alpha': 0.5})
    print("===> THÀNH CÔNG: Django đã khớp hoàn toàn với Moodle!")

if __name__ == '__main__':
    initialize()