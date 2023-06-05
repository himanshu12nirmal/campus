from django import forms
from django.forms import ModelForm
from .models import Student

class StudentAddForm(ModelForm):
    class Meta:
        model = Student
        fields = ('enrollment','name','phone_no','tfws','profile','branch','sem','dob','passout_year','age','password')
        labels = {
            'enrollment': '',
            'name': '',
            'phone_no': '',
            'tfws': '',
            'profile':'',
            'branch': '',
            'sem': '',
            'dob': '',
            'passout_year': '',
            'age': '',
            'password': '',
        }
        tfws_choice =(
            ("1", "YES"),
            ("2", "NO"),
        )
        widgets = {
            'enrollment': forms.TextInput(attrs={'class':'form-control','placeholder':'Enrollment'}),
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Student Name'}),
            'phone_no': forms.TextInput(attrs={'class':'form-control','placeholder':'Phone No'}),
            'branch': forms.TextInput(attrs={'class':'form-control','placeholder':'Branch Name'}),
            'profile': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'dob': forms.DateInput(attrs={'class':'form-control','placeholder':'dob'}),
            'sem': forms.TextInput(attrs={'class':'form-control','placeholder':'Semester'}),
            'tfws': forms.Select(choices= tfws_choice,attrs={'class':'form-control form-select-lg'}),
            'passout_year': forms.TextInput(attrs={'class':'form-control','placeholder':'Passout Year'}),
            'age': forms.TextInput(attrs={'class':'form-control','placeholder':'Age'}),
            'password': forms.TextInput(attrs={'class':'form-control','placeholder':'Password'}),
        }