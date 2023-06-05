from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import Branch,NewUser,Semester,Student,Faculty,Course,HOD,Timetable,Div,Fees,UserDetails,TeacherQR,TempAttendance,Attendance
import pyqrcode
import png
from datetime import date
from django.core.paginator import Paginator

def generate_dob(request):
    today = date.today()
    bdate = request.POST.get('dob').split("-")
    birthDate = date(int(bdate[0]),int(bdate[1]),int(bdate[2]))
    return (today.year - birthDate.year -((today.month, today.day) < (birthDate.month, birthDate.day)))
# Create your views here.

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = NewUser.objects.filter(id=request.POST['username']).first()
        if str(user) == str("hod") :
            userAuth = authenticate(request,username=username,password=password)
            print('in first')
            if userAuth is not None:
                print('in second')
                login(request,userAuth)
                return render(request,'campus_admin/teacher_home.html')
            else:
                return render(request,'campus_admin/home.html')
        elif str(user) == str("principal") :
            userAuth = authenticate(request,username=username,password=password)
            if userAuth is not None:
                login(request,userAuth)
                return render(request,'campus_admin/base.html')
            else:
                return render(request,'campus_admin/home.html')
        elif str(user) == str("teacher") :
            userAuth = authenticate(request,username=username,password=password)
            print('in first')
            if userAuth is not None:
                print('in second')
                login(request,userAuth)
                return render(request,'campus_admin/teacher_home.html')
            else:
                return render(request,'campus_admin/home.html')
        else:
            return render(request,'campus_admin/home.html')
            
    else:
        return render(request,'campus_admin/home.html')

def add_student(request):
    if request.method == "POST":
        #This if will exicute if the student already exits
        if  Student.objects.filter(enrollment = request.POST.get('enrollment')).exists():
            print('exits')
            return render(request,'campus_admin/base.html')
        else:
            ##Part to generate Age
            Age = generate_dob(request)
            
            ##Part to generate QR Code
            en_no = request.POST.get('enrollment')
            url = pyqrcode.create(en_no)
            url.png('media/qr/'+en_no+'.png', scale = 6)

            #This is check if the Div exits or not if not than add div to Div table
            if Div.objects.filter(div = request.POST.get('div')).exists():
                pass
            else:
                div_data = Div(
                    sem = Semester.objects.get(sem= request.POST.get('semester')),
                    div = request.POST.get('div'),
                )
                div_data.save()
            student_data = Student(
            enrollment = request.POST.get('enrollment'),
            name = request.POST.get('name'),
            phone_no = request.POST.get('phone_no'),
            tfws = request.POST.get('tfws'),
            profile = request.POST.get('photo'),
            branch = Branch.objects.get(branch_name =request.POST.get('branch_name')),
            sem = Semester.objects.get(sem= request.POST.get('semester')),
            address = request.POST.get('address'),
            dob = request.POST.get('dob'),
            div = Div.objects.get(div = request.POST.get('div')),
            age = Age,
            password = request.POST.get('password'))
            student_data.save()
            user = UserDetails(
                id=request.POST.get('enrollment'),
                password=request.POST.get('password'),
                type='student'
            )
            user.save()
            return render(request,'campus_admin/base.html')
    else:
        branch=Branch.objects.all()
        semester = Semester.objects.all()
        student_choice = {
            'Yes':'Yes',
            'No':'No',
            'BranchName':branch,
            'Semester':semester,
        }

        return render(request,'campus_admin/add_details/add_student.html',student_choice)

def add_faculty(request):


    if request.method == "POST":
        #This if will exicute if the student already exits
        if  Faculty.objects.filter(faculty_id = request.POST.get('faculty_id')).exists():
            print('exits')
            return render(request,'campus_admin/base.html')
        else:
            ##Part to generate Age
            Age = generate_dob(request)
            
            faculty_data = Faculty(
            faculty_id = request.POST.get('faculty_id'),
            name = request.POST.get('name'),
            phone_no = request.POST.get('phone_no'),
            profile = request.POST.get('photo'),
            branch = Branch.objects.get(branch_name =request.POST.get('branch_name')),
            address = request.POST.get('address'),
            dob = request.POST.get('dob'),
            age = Age,
            password = request.POST.get('password'))
            faculty_data.save()
            
            user = NewUser.objects.create_user(id=request.POST.get('faculty_id'),password=request.POST.get('password'),type='teacher')
            user.save()
            user = UserDetails(
                id=request.POST.get('faculty_id'),
                password=request.POST.get('password'),
                type='teacher'
            )
            user.save()
            return render(request,'campus_admin/base.html')
    else:
        branch=Branch.objects.all()
        faculty_choice = {
            'BranchName':branch,
        }
        return render(request,'campus_admin/add_details/add_faculty.html',faculty_choice)

def add_hod(request):
    branch=Branch.objects.all()
    branch_choice = {
        'BranchName':branch,
    }
    if request.method == 'POST':
        hod_details = HOD(
            id= request.POST.get('id'),
            name = request.POST.get('name'),
            branch = Branch.objects.get(branch_name =request.POST.get('branch_name')),
        )
        hod_details.save()
        
        user = NewUser.objects.create_user(id=request.POST.get('id'),password=request.POST.get('password'),type='hod')
        user.save()
        user = UserDetails(
            id=request.POST.get('id'),
            password=request.POST.get('password'),
            type='hod'
        )
        user.save()
        return render(request,'campus_admin/add_details/add_hod.html',branch_choice)
        
    else:
        return render(request,'campus_admin/add_details/add_hod.html',branch_choice)

"""def add_timetable(request):
    count = list(range(1,9))
    stat="start_time{st}"
    endt="end_time{et}"
    rname="room{nt}"
    rtype="type{rt}"
    course="course{ct}"
    fac ="fac{fc}"
    branch=Branch.objects.all()
    semester = Semester.objects.all()
    div=Div.objects.all()
    timetable_choice = {
        'BranchName':branch,
        'Semester':semester,
        'div':div,
        'count':count,
        'fac': Faculty.objects.all(),
        'course':Course.objects.all(),
        'Day':
    }
    if request.method == "POST":
        for count in count:
            timetable_data = Timetable(
                Branch=Branch.objects.get(branch_name =request.POST.get('branch_name')),
                sem=Semester.objects.get(sem=request.POST.get('semester')),
                div=Div.objects.get(div=request.POST.get('div')),
                day=request.POST.get('day'),
                start_time=request.POST.get(stat.format(st=count)),
                end_time=request.POST.get(endt.format(et=count)),
                course =request.POST.get(course.format(ct=count)),
                faculty = request.POST.get(fac.format(fc=count)),
                room=request.POST.get(rname.format(nt=count)),
                type=request.POST.get(rtype.format(rt=count)),
            )
            timetable_data.save()        
        
        return render(request,'campus_admin/add_timetable.html',timetable_choice)
    else:
        return render(request,'campus_admin/add_timetable.html',timetable_choice)
"""
def add_timetable(request):
    count = list(('MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY'))
    branch=Branch.objects.all()
    semester = Semester.objects.all()
    div=Div.objects.all()
    timetable_choice = {
        'BranchName':branch,
        'Semester':semester,
        'count':count,
    }
    if request.method == "POST":
        branch_name=request.POST.get('branch_name') 
        sem = request.POST.get('semester')
        
        timetableExist = Timetable.objects.filter(Branch=branch_name,sem=sem).exists()
        if timetableExist:
            return render(request,'campus_admin/add_timetable.html',timetable_choice)  
        return redirect('add_timetable2',branch=branch_name,sem=sem)
    else:
        return render(request,'campus_admin/add_timetable.html',timetable_choice)

def add_timetable2(request,branch,sem):
    print("this")
    print(branch)
    rname="room{day}{sr}{div}"
    course="course{day}{sr}{div}"
    fac ="faculty{day}{sr}{div}"
    division ="div{div}"
    divi = "{num}"
    srNo = "sr{day}{num}"
    sr = "{num}"
    count = list(('Monday','Tuesday','Wednesday','Thursday','Friday'))
    branch_name=Branch.objects.all()
    semester = Semester.objects.all()
    div=Div.objects.all()
    timetable_choice = {
        'selectedBranch':branch,
        'selectedSem':sem,
        'BranchName':branch_name,
        'Semester':semester,
        'div':div,
        'count':count,
        'fac': Faculty.objects.all(),
        'course':Course.objects.all(),
        'div':Div.objects.filter(branch=branch,sem=sem).order_by('div')
    }
    if request.method == 'POST': 
        
        numberDiv = Div.objects.filter(branch=branch,sem=sem).order_by('div')
        for day in count:
            for div in numberDiv:
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='9:30 to 10:30',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=1),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=1),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=1),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='10:30 to 11:30',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=2),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=2),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=2),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='11:30 to 12:30',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=3),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=3),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=3),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='12:30 to 1:30',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=4),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=4),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=4),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='2:00 to 3:00',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=5),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=5),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=5),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='3:00 to 4:00',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=6),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=6),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=6),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='4:00 to 5:00',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=7),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=7),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=7),div=divi.format(num=div))),
                )
                timetable_data.save()
                timetable_data = Timetable(
                    Branch=Branch.objects.get(branch_name =branch),
                    sem=Semester.objects.get(sem= sem),
                    div=Div.objects.get(div = div,sem=sem,branch=branch),
                    day=day,
                    start_time='5:00 to 6:00',
                    course=Course.objects.get(code= request.POST.get(course.format(day=day,sr=sr.format(num=8),div=divi.format(num=div)))),
                    faculty=Faculty.objects.get(name= request.POST.get(fac.format(day=day,sr=sr.format(num=8),div=divi.format(num=div)))),
                    room=request.POST.get(rname.format(day=day,sr=sr.format(num=8),div=divi.format(num=div))),
                )
                timetable_data.save()
                
        return render(request,'campus_admin/timetable_report/list_report.html')
    else:
        print(branch)
        print(sem)
        print(Div.objects.filter(branch=branch,sem=sem).order_by('div'))
        return render(request,'campus_admin/add_timetable2.html',timetable_choice)
        
def add_course(request):
    if request.method == 'POST':
        if  Course.objects.filter(code = request.POST.get('code')).exists():
            print('exits')
            return render(request,'campus_admin/base.html')
        
        course_data = Course(
            code = request.POST.get('code'),
            subject = request.POST.get('name'),
            sem = Semester.objects.get(sem= request.POST.get('sem')),
            branch = Branch.objects.get(branch_name =request.POST.get('branch_name')),
            lecture = request.POST.get('lecture'),
            tutorial = request.POST.get('tutorial'),
            practical = request.POST.get('practical'),
            urlAdd = request.POST.get('URL'),
            )
        course_data.save()
        return render(request,'campus_admin/base.html')

    else :
        branch=Branch.objects.all()
        course_choice = {
            'BranchName':branch,
        }
        return render(request,'campus_admin/add_details/add_course.html',course_choice)
#Student Report
def student_report_list(request):
    students = Student.objects.all()
    if request.GET.get('search') == None:
    #set up pagination
        p = Paginator(Student.objects.all().order_by('enrollment'),2)
    else:
        stuId = Student.objects.all()
        stuIdPresent = False
        for stu in stuId:
            if stu.enrollment == request.GET.get('search'):
                stuIdPresent=True
                break
        if stuIdPresent == True:
            p = Paginator(Student.objects.filter(enrollment__contains=request.GET.get('search')).order_by('enrollment'),2)
        else:
            p = Paginator(Student.objects.filter(name__contains=request.GET.get('search')).order_by('enrollment'),2)

    page = request.GET.get('page')
    stud = p.get_page(page)
    student_list = {
        'students':students,
        'stud':stud,
    }
    return render(request,'campus_admin/student_report/list_report.html',student_list)

def student_report_delete(request,enroll):
    
    Student.objects.filter(enrollment=enroll).delete()
    return HttpResponseRedirect('/student_list_report/')

def student_report_update(request,enroll):

    if request.method == "POST":
        student = Student.objects.get(enrollment=enroll)
        Age = generate_dob(request)

        #This is check if the Div exits or not if not than add div to Div table
        if Div.objects.filter(div = request.POST.get('div')).exists():
            pass
        else:
            div_data = Div(
            sem = Semester.objects.get(sem= request.POST.get('semester')),
            div = request.POST.get('div'),
            )
            div_data.save()
        
        
        student.name = request.POST.get('name')
        student.phone_no = request.POST.get('phone_no')
        student.tfws = request.POST.get('tfws')
        student.branch = Branch.objects.get(branch_name =request.POST.get('branch_name'))
        student.sem = Semester.objects.get(sem= request.POST.get('semester'))
        student.address = request.POST.get('address')
        student.dob = request.POST.get('dob')
        student.div = Div.objects.get(div = request.POST.get('div'))
        student.age = Age
        student.password = request.POST.get('password')
        student.save()
        return HttpResponseRedirect('/student_report_list/')
    else:
        student = Student.objects.get(enrollment=enroll)
        semester = Semester.objects.exclude(sem=student.sem)
        branch=Branch.objects.exclude(branch_name=student.branch)
        tfws= list(('Yes','No'))
        if getattr(student, 'tfws') == '2':
            tfws.remove('No')
        else:
            tfws.remove('Yes')
        student_list = {
        'dob':str(student.dob),
        'tfws':tfws[0],
        'BranchName':branch,
        'Semester':semester,
        'student':student,
        }
        return render(request,'campus_admin/student_report/update_report.html',student_list)
        
def student_report_result(request,enroll):
    students = Student.objects.get(pk=enroll)
    student_list = {
        'students':students,
    }
    return render(request,'campus_admin/student_report/report_result.html',student_list)

def faculty_report_list(request):
    if request.GET.get('search') == None:
        p = Paginator(Faculty.objects.all().order_by('faculty_id'),2)
    else:
        facId = Faculty.objects.all()
        facIdPresent = False
        for fac in facId:
            if fac.faculty_id == request.GET.get('search'):
                facIdPresent=True
                break
        if facIdPresent == True:
            p = Paginator(Faculty.objects.filter(faculty_id__contains=request.GET.get('search')).order_by('faculty_id'),2)
        else:
            p = Paginator(Faculty.objects.filter(name__contains=request.GET.get('search')).order_by('faculty_id'),2)

    page = request.GET.get('page')
    faculty = p.get_page(page)
    faculty_list = {
        'faculty':faculty,
    }
    return render(request,'campus_admin/faculty_report/list_report.html',faculty_list)
 
def faculty_report_delete(request,faculty_id):
    
    Faculty.objects.filter(faculty_id=faculty_id).delete()
    return HttpResponseRedirect('/faculty_list_report/')

def faculty_report_update(request,faculty_id):
    if request.method == "POST":
        Age = generate_dob(request)
        faculty = Faculty.objects.filter(faculty_id=faculty_id)
    else:
        faculty = Faculty.objects.get(faculty_id=faculty_id)
        branch=Branch.objects.exclude(branch_name=faculty.branch)
        faculty_list = {
            'dob':str(faculty.dob),
            'BranchName':branch,
            'faculty':faculty,
        }
        return render(request,'campus_admin/faculty_report/update_report.html',faculty_list)

def faculty_report_result(request,faculty_id):
    faculty = Faculty.objects.get(pk=faculty_id)
    faculty_list = {
        'faculty':faculty,
    }
    return render(request,'campus_admin/faculty_report/report_result.html',faculty_list)

def add_branch(request):
    if request.method == "POST":
        branch_data = Branch(
            branch_name =request.POST.get('branch'),
        )
        branch_data.save()
        return render(request,'campus_admin/add_details/add_branch.html')
    else:
        return render(request,'campus_admin/add_details/add_branch.html')


def add_semester(request):
    branch=Branch.objects.all()
    course_choice = {
        'BranchName':branch,
    }
    if request.method == "POST":
        semester_data = Semester(
            sem = request.POST.get('sem'),
            branch_name=Branch.objects.get(branch_name=request.POST.get('branch_name'))
        )
        semester_data.save()
        return render(request,'campus_admin/add_details/add_sem.html',course_choice)
    else:
        return render(request,'campus_admin/add_details/add_sem.html',course_choice)

def faculty_reports_list(request):
    # students = Student.objects.filter(faculty_id__contains=search)
    facId = Faculty.objects.all()
    facIdPresent = False
    for fac in facId:
        if fac.faculty_id == request.GET.get('search'):
            facIdPresent=True
            break
    if facIdPresent == True:
        p = Paginator(Faculty.objects.filter(faculty_id__contains=request.GET.get('search')).order_by('faculty_id'),2)
    else:
        p = Paginator(Faculty.objects.filter(name__contains=request.GET.get('search')).order_by('faculty_id'),2)

    page = request.GET.get('page')
    faculty = p.get_page(page)
    faculty_list = {
        'faculty':faculty,
    }
    return render(request,'campus_admin/faculty_report/list_report.html',faculty_list)
def lecture_report_list(request):
    pass
    # p = Paginator(TeacherQR.objects.all(),2)

    # page = request.GET.get('page')
    # lec = p.get_page(page)
    # lecture_list = {
    #     'lec':lec,
    # }
    # return render(request,'campus_admin/lecture_report/list_report.html',lecture_list)

def lecture_report_result(request,date,stime,etime,branch,sem,div,sub,fac):
    pass
    # p = Paginator(Attendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac),2)
    
    # page = request.GET.get('page')
    # lec = p.get_page(page)
    # student_list = {
    #     'sr':0,
    #     'lec':lec,
    # }
    # return render(request,'campus_admin/lecture_report/list_result.html',student_list)

def lecture_outside(request,date,stime,etime,branch,sem,div,sub,fac):
    pass
    # p = Paginator(TempAttendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac),2)
    
    # page = request.GET.get('page')
    # lec = p.get_page(page)
    # student_list = {
    #     'sr':0,
    #     'lec':lec,
    # }
    # return render(request,'campus_admin/lecture_report/lecture_outside.html',student_list)

def lecture_outside_delete(request,date,stime,etime,branch,sem,div,sub,fac,en):
    pass
    # TempAttendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac,enrollment_id=en).delete()
    # return HttpResponseRedirect('/lecture_report/'+date+'/'+stime+'/'+etime+'/'+branch+'/'+sem+'/'+div+'/'+sub+'/'+fac+'/')

def lecture_outside_submit(request,date,stime,etime,branch,sem,div,sub,fac):
    # exits = TempAttendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac).exists()
    # if exits:
    #     at = TempAttendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac).values('enrollment_id')
    #     for count in at:
    #         count.get('enrollment_id')
    #         att_data =Attendance(
    #             faculty_id=Faculty.objects.get(faculty_id=fac),
    #             date=date,
    #             start_time=stime,
    #             end_time=etime,
    #             subject=Course.objects.get(code=sub),
    #             div=Div.objects.get(div=div),
    #             semester=Semester.objects.get(sem=sem),
    #             branch=Branch.objects.get(branch_name=branch),
    #             enrollment=Student.objects.get(enrollment=count.get('enrollment_id')),
    #         )
    #         att_data.save()
    #         TempAttendance.objects.filter(date=date,start_time=stime,end_time=etime,branch_id=branch,div_id=div,semester_id=sem,subject_id=sub,faculty_id_id=fac).delete()
            
    #     return HttpResponse("Your data has been submitted.")
    # else:
    #     return HttpResponse("Your data has been already submitted or doesn't exits.")
    # return render(request,'campus_admin/lecture_report/lecture_outside.html',student_list)
    pass

#TimeTable Report
def timetable_report_list(request):
    
    return render(request,'campus_admin/timetable_report/list_report.html')

def timetable_report_delete(request,enroll):
    
    Student.objects.filter(enrollment=enroll).delete()
    return HttpResponseRedirect('/student_list_report/')


def timetable_report_update(request,enroll):

    if request.method == "POST":
        return HttpResponseRedirect('/timetable_report_list/')
    else:
        return render(request,'campus_admin/faculty_report/update_report.html')
        

def timetable_report_result(request,enroll):
    return render(request,'campus_admin/faculty_report/report_result.html')
    
    
def get_semester(request):
    div = request.GET['division']
    print(div)
    semester = Semester.objects.all()
    return JsonResponse({'semester':list(semester.values())})

def get_div(request,sem):
    div = Div.objects.filter(branch = 'ce',sem =sem)
    course_choice = {
        'Semester':sem,
        'Division':div
    }
    return JsonResponse(course_choice)