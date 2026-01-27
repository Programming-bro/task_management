from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

# Create your views here.

def manager_dahsboard(request):
    return render(request,"dashboard/manager_dashboard.html")
def user_dashboard(request):
    return render(request,"dashboard/user_dashboard.html")
def test(request):
    return render(request,"test.html")
def test_form(request):
    employees = Employee.objects.all()
    form = TaskModelForm()
    if(request.method == 'POST'):
        form = TaskModelForm(request.POST)
        if form.is_valid():
            """For ModelForm data"""
            form.save()

            return render(request,'test_form.html',{"form":form,"message":"Task Added Successfully"})
    
    context = {"form":form}
    return render(request,"test_form.html",context)

def view_task(request):
    tasks = Task.objects.all()
    task_3 = Task.objects.get(id=3)
    return render(request,"show_task.html",{"tasks":tasks,"task3":task_3})