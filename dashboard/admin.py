from django.contrib import admin
from .models import KnowledgeMap, SystemConfig

@admin.register(KnowledgeMap)
class KnowledgeMapAdmin(admin.ModelAdmin):
    list_display = ('moodle_quiz_id', 'chapter_name', 'skill_tag', 'difficulty_level')

admin.site.register(SystemConfig)