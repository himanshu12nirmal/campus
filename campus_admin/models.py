from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    
    def create_user(self,id,password,type,**other_fields):
        user = self.model(id =id,type=type,**other_fields)
        if type != 'student': 
            user.is_staff= True
            user.is_superuser = True
        else:
            user.is_staff= False
            user.is_superuser = False  
        user.set_password(password)
        user.save()
        return user;
    
    def create_superuser(self,id,password,type,**other_fields):
        print(make_password( password))
            
        return self.create_user(id,password,type,**other_fields)
    
class NewUser(AbstractBaseUser,PermissionsMixin):
    class Meta:
        db_table = 'NewUser'
    id = models.CharField(max_length=12,primary_key=True)
    type = models.CharField(max_length=12)
    is_staff = models.BooleanField(default=True)
    password = models.CharField(max_length=100)
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS =['type']
    
    def __str__(self):
        return self.type

class UserDetails(models.Model):
    class Meta:
        db_table = 'UserDetails'
    id = models.CharField(max_length=12,primary_key=True)
    password = models.CharField(max_length=50)
    type = models.CharField(max_length=12,blank=True,null=True)
    
    
    def __str__(self):
        return self.id
class Branch(models.Model):
    class Meta:
        db_table = 'Branch'
    branch_name = models.CharField(primary_key=True,max_length=20)

    def __str__(self):
        return str(self.branch_name)

class Semester(models.Model):
    class Meta:
        db_table = 'Semester'
    sem = models.CharField(max_length=1,primary_key=True)
    branch_name = models.ForeignKey(Branch,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.sem)

class Div(models.Model):
    class Meta:
        db_table = 'Div'
    div = models.CharField(null=True,blank=True,max_length=2)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
       return str(self.div)

class Student(models.Model):
    class Meta:
        db_table = 'Student'
    tfws_choice = (
        ('1','Yes'),
        ('2','No'),

    )
    enrollment = models.CharField(primary_key=True,max_length=14)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    tfws = models.CharField(max_length=4,choices=tfws_choice)
    profile = models.ImageField(null=True,blank=True,upload_to='images/student/profile/')
    # div = models.CharField(null=True,blank=True,max_length=2)
    div = models.ForeignKey(Div,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    address = models.CharField(max_length=120)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)
    dob = models.DateField()
    age = models.IntegerField()
    password = models.CharField(max_length=25)

    def __str__(self):
        return '%s' % (self.enrollment)

class Faculty(models.Model):
    class Meta:
        db_table = 'Faculty'
    faculty_id = models.CharField(primary_key=True,max_length=10)
    name = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    profile = models.ImageField(null=True,blank=True,upload_to='images/faculty/')
    dob = models.DateField()
    age = models.IntegerField()
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.name

class HOD(models.Model):
    class Meta:
        db_table = 'HOD'
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=40)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    
    def __str__(self):
       return self.name
       
class Course(models.Model):
    class Meta:
        db_table = 'Course'
    code = models.CharField(primary_key=True,max_length=10)
    subject = models.CharField(max_length=30)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE)
    lecture = models.IntegerField(null=True,blank=True,)
    tutorial = models.IntegerField(null=True,blank=True,)
    practical = models.IntegerField(null=True,blank=True,)
    urlAdd = models.CharField(max_length=300,null=True,blank=True)
    def __str__(self):
       return self.subject

class Room(models.Model):
    class Meta:
        db_table = 'Room'
    roomNo = models.CharField(max_length=10,blank=True,null=True)
    roomType = models.CharField(max_length=10,blank=True,null=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    
class Timetable(models.Model):
    class Meta:
        db_table = 'Timetable'
    Branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    sem = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    div = models.ForeignKey(Div,on_delete=models.CASCADE,null=True,blank=True)
    day = models.CharField(max_length=20,null=True,blank=True)
    start_time = models.CharField(max_length=20)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    faculty = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
    room = models.CharField(max_length=20,null=True,blank=True)
    def __str__(self):
       return str(self.Branch.branch_name + self.sem.sem + self.div.div + self.day)

class Fees(models.Model):
    class Meta:
        db_table = 'Fees'
    enrollment = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=20)
    status = models.BooleanField()
    amount = models.IntegerField()

    def __str__(self):
        return str(self.enrollment)

class Attendance(models.Model):
    class Meta:
        db_table = 'Attendance'
    faculty_id = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    div = models.ForeignKey(Div,on_delete=models.CASCADE,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    enrollment = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    
    
    def __str__(self):
        return str(self.enrollment)
    
class TempAttendance(models.Model):
    class Meta:
        db_table = 'TempAttendance'
    faculty_id = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    div = models.ForeignKey(Div,on_delete=models.CASCADE,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    enrollment = models.ForeignKey(Student,on_delete=models.CASCADE,null=True,blank=True)
    
    
    def __str__(self):
        return str(self.enrollment)
    
class TeacherQR(models.Model):
    class Meta:
        db_table = 'TeacherQR'
    faculty_id = models.ForeignKey(Faculty,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    subject = models.ForeignKey(Course,on_delete=models.CASCADE,null=True,blank=True)
    div = models.ForeignKey(Div,on_delete=models.CASCADE,null=True,blank=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,null=True,blank=True)
    branch = models.ForeignKey(Branch,on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return str(self.faculty_id)
        