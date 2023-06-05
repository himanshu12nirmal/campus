from django.contrib import admin
from .models import Branch,Semester,Student,Faculty,Course,Timetable,Fees,Div,Room,HOD
# Register your models here.
admin.site.register(Branch)
admin.site.register(Semester)
admin.site.register(Student)
admin.site.register(HOD)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Timetable)
admin.site.register(Div)
admin.site.register(Fees)
admin.site.register(Room)