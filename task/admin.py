from django.contrib import admin
from task.models import Task, SubTask, SubTaskItem

# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_name',
        'task_date',
        'task_description',
        'task_category',
        'task_priority',
        'task_status',
        'task_id',
    )

class SubTaskAdmin(admin.ModelAdmin):
    list_display = (
       'name',
       'id',
    )

class SubTaskItemAdmin(admin.ModelAdmin):
    list_display = (
        'item',
        'done',
        'id'
    )

admin.site.register(Task, TaskAdmin)
admin.site.register(SubTask, SubTaskAdmin)
admin.site.register(SubTaskItem, SubTaskItemAdmin)

