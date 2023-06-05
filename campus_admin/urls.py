from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),

    #Add Details
    path('add_student/', views.add_student,name='add-student'),
    path('add_faculty/', views.add_faculty,name='add-faculty'),
    path('add_hod/', views.add_hod,name='add-hod'),
    path('add_timetable/', views.add_timetable,name='add-timetable'),
    path('add_timetable2/<branch>/<sem>', views.add_timetable2,name='add_timetable2'),
    path('add_branch/',views.add_branch,name='add-branch'),
    path('add_semester/',views.add_semester,name='add-semester'),
    path('add_course/',views.add_course,name='add-course'),

    #Student Report 
    path('student_report_list/',views.student_report_list,name='student-report-list'),
    path('student_report_delete/<enroll>',views.student_report_delete,name='student-report-delete'),
    path('student_report_update/<enroll>',views.student_report_update,name='student-report-update'),
    path('student_report_result/<enroll>',views.student_report_result,name='student-report-result'),
    
    
    #Faculty Report
    path('faculty_list_report/',views.faculty_report_list,name='faculty-report-list'),
    path('faculty_report_delete/<faculty_id>',views.faculty_report_delete,name='faculty-report-delete'),
    path('faculty_report_update/<faculty_id>',views.faculty_report_update,name='faculty-report-update'),
    path('faculty_report_result/<faculty_id>',views.faculty_report_result,name='faculty-report-result'),

    #TimeTable Report
    path('timetable_report_list/',views.timetable_report_list,name='timetable-report-list'),
    path('timetable_report_delete/<enroll>',views.timetable_report_delete,name='timetable-report-delete'),
    path('timetable_report_update/<enroll>',views.timetable_report_update,name='timetable-report-update'),
    path('timetable_report_result/<enroll>',views.timetable_report_result,name='timetable-report-result'),
    
    #Lecture Report
    path('lecture_report_list/',views.lecture_report_list,name='lecture-report-list'),
    # path('lecture_report_delete/<enroll>',views.lecture_report_delete,name='lecture-report-delete'),
    # path('lecture_report_update/<enroll>',views.lecture_report_update,name='lecture-report-update'),
    path('lecture_report_result/<date>/<stime>/<etime>/<branch>/<sem>/<div>/<sub>/<fac>/',views.lecture_report_result,name='lecture-report-result'),
    
    path('lecture_report/<date>/<stime>/<etime>/<branch>/<sem>/<div>/<sub>/<fac>/',views.lecture_outside,name="lecture-outside"),
    path('lecture_report_delete/<date>/<stime>/<etime>/<branch>/<sem>/<div>/<sub>/<fac>/<en>/',views.lecture_outside_delete,name="lecture-outside_delete"),
    path('lecture_report_submit/<date>/<stime>/<etime>/<branch>/<sem>/<div>/<sub>/<fac>/',views.lecture_outside_submit,name="lecture_outside_submit"),

    path('get_semester',views.get_semester,name='get-semester'),
    path('get_div/<sem>',views.get_div,name='get-div'),
    
]