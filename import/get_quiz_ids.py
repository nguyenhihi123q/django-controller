import requests

# Cấu hình thông tin Moodle của bạn
MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
TOKEN = "b39e2c5a3e5df14a9701ab52ff6924e5"
COURSE_ID = 3  # ID khóa học của bạn

def get_all_quiz_ids():
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'mod_quiz_get_quizzes_by_courses',
        'moodlewsrestformat': 'json',
        'courseids[0]': COURSE_ID
    }

    try:
        response = requests.get(MOODLE_URL, params=params)
        data = response.json()

        if 'quizzes' in data:
            print(f"{'ID':<10} | {'Tên bài kiểm tra':<50}")
            print("-" * 65)
            # Sắp xếp theo ID để bạn dễ quản lý
            quizzes = sorted(data['quizzes'], key=lambda x: x['id'])
            
            for quiz in quizzes:
                # 'id' là ID để điều khiển, 'name' là tên hiển thị
                print(f"{quiz['id']:<10} | {quiz['name']:<50}")
            
            print("-" * 65)
            print(f"Tổng cộng tìm thấy: {len(quizzes)} bài kiểm tra.")
        else:
            print("Không tìm thấy bài kiểm tra nào hoặc lỗi API.")
            print(data)
            
    except Exception as e:
        print(f"Lỗi kết nối: {e}")

if __name__ == "__main__":
    get_all_quiz_ids()