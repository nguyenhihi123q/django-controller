import requests

# Thông tin kết nối
MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "4a8ef2f061286d224b4a9e8a42b6b415" # Token bạn vừa tạo

# Hàm muốn gọi: Lấy danh sách người dùng đã ghi danh vào khóa học ID 3
function = "core_enrol_get_enrolled_users"

# Tham số gửi đi
params = {
    'wstoken': TOKEN,
    'wsfunction': function,
    'moodlewsrestformat': 'json',
    'courseid': 3
}

print(">>> Đang gửi yêu cầu đến Moodle API...")

try:
    response = requests.get(MOODLE_URL, params=params)
    data = response.json()

    if isinstance(data, list):
        print(f"===> THÀNH CÔNG! Đã tìm thấy {len(data)} thành viên trong khóa học.")
        for user in data[:5]: # In thử 5 người đầu tiên
            print(f"- Sinh viên: {user['fullname']} (Username: {user['username']})")
    else:
        print(f"===> LỖI TỪ MOODLE: {data.get('message')}")

except Exception as e:
    print(f"===> LỖI KẾT NỐI: {e}")