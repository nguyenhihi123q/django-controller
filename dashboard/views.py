from django.shortcuts import render
import requests

def student_list(request):
    # Cấu hình API (Giống file test lúc nãy)
    MOODLE_URL = "http://localhost/lophocthaynguyendhs/webservice/rest/server.php"
    TOKEN = "4a8ef2f061286d224b4a9e8a42b6b415"
    
    params = {
        'wstoken': TOKEN,
        'wsfunction': 'core_enrol_get_enrolled_users',
        'moodlewsrestformat': 'json',
        'courseid': 3
    }
    
    try:
        response = requests.get(MOODLE_URL, params=params)
        students = response.json()
    except:
        students = []

    return render(request, 'dashboard/index.html', {'students': students})