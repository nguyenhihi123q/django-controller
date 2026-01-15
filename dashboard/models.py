from django.db import models

class KnowledgeMap(models.Model):
    # ID của bài Quiz hoặc Module trên Moodle
    moodle_quiz_id = models.IntegerField(unique=True, verbose_name="ID bài học Moodle")
    
    # Tên chương/phần để hiển thị
    chapter_name = models.CharField(max_length=200, verbose_name="Tên chương")
    
    # Kỹ năng trọng tâm (Dùng cho thuật toán CBF)
    skill_tag = models.CharField(max_length=100, verbose_name="Kỹ năng trọng tâm")
    
    # Mức độ khó (1: Dễ, 2: Vừa, 3: Khó)
    difficulty_level = models.IntegerField(default=1, verbose_name="Độ khó")

    def __str__(self):
        return f"{self.chapter_name} ({self.skill_tag})"

class SystemConfig(models.Model):
    # Trọng số Alpha cho mô hình Lai (Hybrid) 
    # Alpha * CF + (1 - Alpha) * CB [cite: 381]
    hybrid_alpha = models.FloatField(default=0.5, verbose_name="Trọng số Alpha")
    
    # Ngày cập nhật cuối cùng
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cấu hình hệ thống (Alpha={self.hybrid_alpha})"
    

class StudentBehavior(models.Model):
    student_id = models.IntegerField(verbose_name="ID Sinh viên")
    moodle_quiz_id = models.IntegerField(verbose_name="ID bài học")
    action_type = models.CharField(max_length=50, verbose_name="Hành động") # Ví dụ: 'view', 'click'
    time_spent = models.IntegerField(default=0, verbose_name="Thời gian học (giây)")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Thời điểm")

    def __str__(self):
        return f"SV {self.student_id} - {self.action_type} bài {self.moodle_quiz_id}"