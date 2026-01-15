import requests
import json

URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "b39e2c5a3e5df14a9701ab52ff6924e5"

def get_grade_items():
    # Gọi hàm lấy điểm cho khóa học ID 3
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'gradereport_user_get_grade_items',
        'moodlewsrestformat': 'json',
        'courseid': 3,
        'userid': 2 # Check thử trên chính tài khoản admin của bạn
    }
    
    try:
        response = requests.get(URL, params=params).json()
        
        if 'usergrades' in response:
            print(f"--- DANH SÁCH BÀI TẬP TRONG KHÓA C++ (ID: 3) ---")
            grade_items = response['usergrades'][0].get('gradeitems', [])
            
            for item in grade_items:
                # Chỉ lấy các bài tập thực tế (itemtype là mod)
                if item.get('itemtype') == 'mod':
                    name = item.get('itemname')
                    # ID quan trọng nhất để khớp với Django là iteminstance
                    instance_id = item.get('iteminstance')
                    print(f"Tên bài: {name} | ID thực tế: {instance_id}")
        else:
            print("--- LỖI PHẢN HỒI ---")
            print(json.dumps(response, indent=2, ensure_ascii=False))
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    get_grade_items()