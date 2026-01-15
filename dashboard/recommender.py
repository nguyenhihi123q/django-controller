import requests
import math
from .models import KnowledgeMap

# Cấu hình chung cho kết nối Moodle
MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "b39e2c5a3e5df14a9701ab52ff6924e5"

def fetch_student_grades(student_id):
    """Lấy bảng điểm chi tiết của sinh viên từ Moodle"""
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'gradereport_user_get_grade_items',
        'moodlewsrestformat': 'json',
        'courseid': 3,
        'userid': student_id
    }
    
    grades = {}
    try:
        response = requests.get(MOODLE_URL, params=params)
        data = response.json()
        if 'usergrades' in data and len(data['usergrades']) > 0:
            for item in data['usergrades'][0]['gradeitems']:
                if item.get('itemtype') == 'mod':
                    instance_id = item.get('iteminstance')
                    raw_grade = item.get('graderaw')
                    # Lưu điểm vào dict: {ID_bai_hoc: Diem_so}
                    grades[instance_id] = float(raw_grade) if raw_grade is not None else 0.0
    except Exception as e:
        print(f"Lỗi fetch_student_grades: {e}")
    return grades

def calculate_cosine_similarity(grades1, grades2):
    """Tính độ tương đồng giữa hai sinh viên dựa trên vector điểm số"""
    all_keys = set(grades1.keys()) | set(grades2.keys())
    if not all_keys: return 0.0
    
    dot_product = sum(grades1.get(k, 0) * grades2.get(k, 0) for k in all_keys)
    sum_sq1 = sum(v**2 for v in grades1.values())
    sum_sq2 = sum(v**2 for v in grades2.values())
    
    denominator = math.sqrt(sum_sq1) * math.sqrt(sum_sq2)
    return dot_product / denominator if denominator else 0.0

# --- CÁC HÀM TÁC ĐỘNG ĐIỀU KHIỂN (CONTROL ACTIONS) ---

def move_student_to_group(student_id, group_id):
    """HÀM MỞ KHÓA: Đưa sinh viên vào nhóm để hiện bài học"""
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_group_add_group_members',
        'moodlewsrestformat': 'json',
        'members[0][groupid]': group_id,
        'members[0][userid]': student_id,
    }
    try:
        response = requests.post(MOODLE_URL, params=params).json()
        
        # Moodle trả về None hoặc [] nếu thành công
        if response is None or response == []:
            print(f"✅ Moodle: Đã thêm SV {student_id} vào nhóm {group_id}")
            return True
            
        # Nếu có lỗi, Moodle trả về dict chứa 'exception'
        if isinstance(response, dict) and 'exception' in response:
            print(f"❌ LỖI MOODLE API: {response.get('message')}")
            return False
            
        return False
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {e}")
        return False

# Cập nhật tương tự cho hàm xóa
def remove_student_from_group(student_id, group_id):
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_group_delete_group_members',
        'moodlewsrestformat': 'json',
        'members[0][groupid]': group_id,
        'members[0][userid]': student_id,
    }
    try:
        response = requests.post(MOODLE_URL, params=params).json()
        if response is None or response == []:
            return True
        if isinstance(response, dict) and 'exception' in response:
            print(f"❌ LỖI MOODLE API: {response.get('message')}")
        return False
    except:
        return False