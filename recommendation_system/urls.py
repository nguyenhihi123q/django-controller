from django.contrib import admin
from django.urls import path
from dashboard import views  # Import toàn bộ module views từ app dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.student_list, name='home'), # Trang chủ hiện danh sách
    path('student/<int:student_id>/', views.student_detail, name='student_detail'), # Trang chi tiết
    path('control/<int:student_id>/<int:group_id>/<str:action>/', views.manual_control, name='manual_control'),
]