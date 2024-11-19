from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Student
from .forms import StudentForm

# Create your views here.
def index(request):
    return render(request, 'students/index.html', {
        'students': Student.objects.all()
    })

def view_student(request, id):
    student = Student.objects.get(pk=id)
    # avoid hardcoding a url to a view
    return HttpResponseRedirect(reverse('index'))

def add(request):
    # if request is POST validate and save data
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            # clean the data and store it in the database
            new_student_number = form.cleaned_data['student_number']
            new_first_name = form.cleaned_data['first_name']
            new_last_name = form.cleaned_data['last_name']
            new_email = form.cleaned_data['email']
            new_college_program = form.cleaned_data['college_program']
            new_gpa = form.cleaned_data['gpa']

            # after cleaning data store it into the database
            new_student = Student(
                student_number = new_student_number,
                first_name = new_first_name,
                last_name = new_last_name,
                email = new_email,
                college_program = new_college_program,
                gpa = new_gpa
            )

            new_student.save()
            return render(request, 'students/add.html', {
                'form': StudentForm(),
                # if everything goes well, meaning form post method was a success
                'success': True
            })
    # if request isn't POST, generate form
    else:
        form = StudentForm()
        return render(request, 'students/add.html', {
            'form': StudentForm()
        })


def edit(request, id):
    if request.method == "POST":
        # get student with primary key of id in parameter
        student = Student.objects.get(pk=id)
        # the second argument is to ensure that we're editing the correct student
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return render(request, 'students/edit.html', {
                'form': form,
                'success': True
            })
    else:
        student = Student.objects.get(pk=id)
        form = StudentForm(instance=student)
        return render(request, 'students/edit.html', {
            'form': form
        })


def delete(request, id):
    if request.method == "POST":
        student = Student.objects.get(pk=id)
        student.delete()
    return HttpResponseRedirect(reverse('index'))
