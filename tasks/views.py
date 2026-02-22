from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task, TaskDetails
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from users.views import is_admin
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView, ListView, DeleteView, DetailView

# Create your views here.

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Employee').exists()

class ManagerDahsboard(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Task
    template_name = "dashboard/manager_dashboard.html"
    context_object_name = "tasks"

    def test_func(self):
        return is_manager(self.request.user)

    def get_queryset(self):
        type_filter = self.request.GET.get("type", "all")

        base_query = Task.objects.select_related(
            "details"
        ).prefetch_related("assigned_to")

        if type_filter == "completed":
            return base_query.filter(status="COMPLETED")
        elif type_filter == "in_progress":
            return base_query.filter(status="IN_PROGRESS")
        elif type_filter == "pending":
            return base_query.filter(status="PENDING")
        return base_query.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["counts"] = Task.objects.aggregate(
            total=Count("id"),
            completed=Count("id", filter=Q(status="COMPLETED")),
            in_progress=Count("id", filter=Q(status="IN_PROGRESS")),
            pending=Count("id", filter=Q(status="PENDING")),
        )

        context["type"] = self.request.GET.get("type", "all")
        print(context["type"])
        return context


class EmployeeDashboard(LoginRequiredMixin, UserPassesTestMixin,TemplateView):
    template_name = 'dashboard/employee_dashboard.html'
    login_url = reverse_lazy('sign_in')
    def test_func(self):
        return is_employee(self.request.user)

class CreateTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'tasks.add_task'
    login_url = 'sign_in'
    template_name = 'task_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = kwargs.get('task_form', TaskModelForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        task_form = TaskModelForm(request.POST)

        if task_form.is_valid():
            task = task_form.save()

            messages.success(request, "Task Created Successfully")
            context = self.get_context_data(task_form=task_form,)
            return render(request, self.template_name, context)



class ViewTask(ContextMixin,LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'tasks.view_task'
    login_url = 'sign_in'
    template_name = 'show_task.html'
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['tasks'] = Task.objects.all()
        return render(request, self.template_name, context)
        

class UpdateTask(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Task
    form_class = TaskModelForm
    template_name = "task_form.html"
    pk_url_kwarg = "id"
    permission_required = "tasks.change_task"
    login_url = "sign_in"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task_form'] = self.get_form()

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        task_form = TaskModelForm(request.POST, instance=self.object)

        if task_form.is_valid():
            task = task_form.save()

            messages.success(request, "Task Updated Successfully")
            return redirect('update_task', self.object.id)
        return redirect('update_task', self.object.id)
    
class DeleteTask(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Task
    template_name = "manager_dahsboard.html"
    pk_url_kwarg = "id"
    success_message = "Task was deleted successfully!"
    success_url = reverse_lazy('manager_dashboard')
    permission_required = "tasks.delete_task"

class TaskDetails(LoginRequiredMixin,PermissionRequiredMixin,DetailView):
    model = Task
    template_name = "task_details.html"
    pk_url_kwarg = "id"
    context_object_name = 'task'
    success_url = reverse_lazy('task_details')
    permission_required = "tasks.view_task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_choices"] = Task.STATUS_CHOICES
        return context
    def post(self, request,*args, **kwargs):
        task = self.get_object()
        selected_status = request.POST.get('task_status')
        task.status = selected_status
        task.save()
        return redirect('task_details', task.id)

@login_required
def dashboard(request):
    if is_manager(request.user):
        return redirect('manager_dashboard')
    elif is_employee(request.user):
        return redirect('employee-dashboard')
    elif is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('no-permission')