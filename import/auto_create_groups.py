import requests

MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "b39e2c5a3e5df14a9701ab52ff6924e5"
COURSE_ID = 3

def create_moodle_groups():
    groups_to_create = []
    # Chuẩn bị dữ liệu cho 9 nhóm (từ Phần 2 đến Phần 10)
    for i in range(2, 11):
        groups_to_create.append({
            'courseid': COURSE_ID,
            'name': f'Mo_Khoa_Phan_{i}',
            'description': f'Nhóm tự động mở khóa Phần {i} dựa trên năng lực'
        })

    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_group_create_groups',
        'moodlewsrestformat': 'json',
    }

    # Chuyển đổi danh sách nhóm sang định dạng tham số Moodle yêu cầu
    for index, group in enumerate(groups_to_create):
        params[f'groups[{index}][courseid]'] = group['courseid']
        params[f'groups[{index}][name]'] = group['name']
        params[f'groups[{index}][description]'] = group['description']

    try:
        response = requests.post(MOODLE_URL, params=params).json()
        
        if isinstance(response, list):
            print(f"{'Tên Nhóm':<20} | {'ID Nhóm mới tạo':<15}")
            print("-" * 40)
            for res in response:
                print(f"{res['name']:<20} | {res['id']:<15}")
            print("-" * 40)
            print("✅ Đã tạo xong 9 nhóm thành công!")
        else:
            print("❌ Lỗi từ Moodle:", response)
            
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    create_moodle_groups()