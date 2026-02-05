from django.shortcuts import render, redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetails
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages

# Create your views here.

def manager_dahsboard(request):
    type = request.GET.get('type','all') 
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    counts = Task.objects.aggregate(
        total = Count('id'),
        completed = Count('id',filter=Q(status = 'COMPLETED')),
        in_progress = Count('id',filter=Q(status = 'IN_PROGRESS')),
        pending = Count('id',filter=Q(status = 'PENDING'))
    )
    

    base_query = Task.objects.select_related('details').prefetch_related('assigned_to')
    
    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in_progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()
    print(type)

    context = {
        'tasks':tasks,
        'counts':counts
    }

    return render(request,"dashboard/manager_dashboard.html",context)

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
    # tasks = Task.objects.filter(Q(title__icontains="me") | Q(status = "PENDING"))
    # task_count = Task.objects.aaggregate(num_task = Count('id'))
    tasks = TaskDetails.objects.all()
    return render(request,"show_task.html",{"tasks":tasks})

def update_task(request,id):
    task = Task.objects.get(id=id)
    assigned_to = Employee.objects.all()
    form = TaskModelForm(instance=task)

    if(request.method == 'POST'):
        form = TaskModelForm(request.POST,instance=task)
        if form.is_valid():
            """For ModelForm data"""
            form.save()
            messages.success(request, "Task Updated Successfully")
            return redirect('update_task',id)
    
    context = {"form":form}

    return render(request,"test_form.html",context)

def delete_task(request,id):
    if(request.method == 'POST'):
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request,"Event Deleted successfully")
        return redirect("manager_dashboard")
    else:
        messages.error(request,"Something went wrong")
        return redirect("manager_dashboard")