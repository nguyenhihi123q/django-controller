from django.shortcuts import render, redirect
from django.contrib import messages  # Thêm thư viện thông báo
from .recommender import (
    fetch_student_grades, 
    calculate_cosine_similarity, 
    move_student_to_group, 
    remove_student_from_group
)
from .models import KnowledgeMap
import requests

# 1. CẤU HÌNH HỆ THỐNG
MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "b39e2c5a3e5df14a9701ab52ff6924e5"

PROGRESSION_MAP = {
    2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 9: 8, 10: 9,
}

SECTIONS_LIST = [
    {'name': 'Phần 2: Các khái niệm cơ bản', 'group_id': 1},
    {'name': 'Phần 3: Cấu trúc điều khiển', 'group_id': 2},
    {'name': 'Phần 4: Mảng', 'group_id': 3},
    {'name': 'Phần 5: Chuỗi ký tự', 'group_id': 4},
    {'name': 'Phần 6: Con trỏ', 'group_id': 5},
    {'name': 'Phần 7: Hàm và Đệ quy', 'group_id': 6},
    {'name': 'Phần 8: Kiểu dữ liệu cấu trúc', 'group_id': 7},
    {'name': 'Phần 9: Lập trình hướng đối tượng', 'group_id': 8},
    {'name': 'Phần 10: Xử lý File', 'group_id': 9},
]

# 2. HÀM TỰ ĐỘNG (CÓ KIỂM TRA OVERRIDE)
def auto_check_and_unlock(request, student_id, my_grades):
    actions_taken = []
    # Lấy danh sách các phần giáo viên đã cố tình KHÓA từ session
    manual_locks = request.session.get(f'manual_locks_{student_id}', [])

    for quiz_id, group_id in PROGRESSION_MAP.items():
        # Nếu giáo viên đã KHÓA thủ công phần này, không tự động mở lại
        if group_id in manual_locks:
            continue
            
        grade = my_grades.get(quiz_id, 0.0)
        if grade >= 5.0:
            success = move_student_to_group(student_id, group_id)
            if success:
                actions_taken.append(f"Tự động mở khóa lộ trình dựa trên điểm bài Quiz {quiz_id}")
    return actions_taken

# 3. VIEW: ĐIỀU KHIỂN THỦ CÔNG (CẬP NHẬT THÔNG BÁO)
def manual_control(request, student_id, group_id, action):
    if request.method == "POST":
        # Lấy danh sách khóa hiện tại trong session
        session_key = f'manual_locks_{student_id}'
        manual_locks = request.session.get(session_key, [])

        if action == "lock":
            success = remove_student_from_group(student_id, group_id)
            if success:
                # Thêm vào danh sách khóa để auto-unlock không ghi đè
                if group_id not in manual_locks:
                    manual_locks.append(group_id)
                messages.warning(request, f"🔒 Đã khóa thành công Phần học (Group ID: {group_id})")
        
        elif action == "unlock":
            success = move_student_to_group(student_id, group_id)
            if success:
                # Xóa khỏi danh sách khóa để cho phép auto-unlock hoạt động lại
                if group_id in manual_locks:
                    manual_locks.remove(group_id)
                messages.success(request, f"🔓 Đã mở khóa thành công Phần học (Group ID: {group_id})")
        
        request.session[session_key] = manual_locks
            
    return redirect('student_detail', student_id=student_id)

# 4. VIEW: DANH SÁCH SINH VIÊN (Giữ nguyên)
def student_list(request):
    params = {'wstoken': TOKEN, 'wsfunction': 'core_enrol_get_enrolled_users', 'moodlewsrestformat': 'json', 'courseid': 3}
    try:
        response = requests.get(MOODLE_URL, params=params).json()
        students = response if isinstance(response, list) else []
    except: students = []
    return render(request, 'dashboard/index.html', {'students': students})

# 5. VIEW: CHI TIẾT SINH VIÊN (CẬP NHẬT TRUYỀN REQUEST)
def student_detail(request, student_id):
    my_grades = fetch_student_grades(student_id)
    all_lessons = KnowledgeMap.objects.all()
    
    # Truyền request vào để kiểm tra session manual_locks
    actions_taken = auto_check_and_unlock(request, student_id, my_grades)
    
    # CF và Hybrid logic (Giữ nguyên phần tính toán của bạn)
    params = {'wstoken': TOKEN, 'wsfunction': 'core_enrol_get_enrolled_users', 'moodlewsrestformat': 'json', 'courseid': 3}
    try: all_users = requests.get(MOODLE_URL, params=params).json()
    except: all_users = []

    similar_students_data = []
    if isinstance(all_users, list):
        for user in all_users:
            other_id = user.get('id')
            if other_id and int(other_id) != int(student_id):
                other_grades = fetch_student_grades(other_id)
                if other_grades:
                    score = calculate_cosine_similarity(my_grades, other_grades)
                    similar_students_data.append({
                        'id': other_id, 'username': user.get('username'),
                        'fullname': user.get('fullname'), 'score': score, 'grades': other_grades
                    })

    top_similars = sorted(similar_students_data, key=lambda x: x['score'], reverse=True)[:5]

    recommendations = []
    for lesson in all_lessons:
        m_id = lesson.moodle_quiz_id
        my_score = my_grades.get(m_id, 0.0)
        cbf_score = (10 - my_score) if my_score < 5 else 0
        peer_scores = [s['grades'].get(m_id, 0.0) * s['score'] for s in top_similars[:3]]
        cf_score = sum(peer_scores) / len(peer_scores) if peer_scores else 0
        priority = (0.7 * cbf_score) + (0.3 * cf_score)
        if priority > 2.0:
            recommendations.append({
                'chapter': lesson.chapter_name, 'skill': lesson.skill_tag,
                'priority': round(priority, 2),
                'moodle_url': f"http://localhost/lophocthaynguyendhs/mod/quiz/view.php?id={m_id}"
            })

    low_skills = []
    for item in all_lessons:
        grade = my_grades.get(item.moodle_quiz_id, 0.0)
        if grade < 5.0:
            low_skills.append({'chapter': item.chapter_name, 'skill': item.skill_tag, 'grade': grade})

    return render(request, 'dashboard/student_detail.html', {
        'student_id': student_id,
        'low_skills': low_skills,
        'actions_taken': actions_taken,
        'sections': SECTIONS_LIST,
        'manual_locks': request.session.get(f'manual_locks_{student_id}', []), # Gửi danh sách đã khóa để hiện badge
        'similar_students': [
            {'fullname': s['fullname'], 'username': s['username'], 'score': round(s['score']*100, 2)} 
            for s in top_similars
        ],
        'recommendations': sorted(recommendations, key=lambda x: x['priority'], reverse=True)[:3]
    })