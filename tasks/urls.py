from django.urls import path
from tasks.views import dashboard, ManagerDahsboard,EmployeeDashboard, CreateTask, ViewTask, UpdateTask, DeleteTask, TaskDetails

urlpatterns = [
    path('manager_dashboard/',ManagerDahsboard.as_view(), name='manager_dashboard'),
    path('employee_dashboard/',EmployeeDashboard.as_view(), name='employee-dashboard'),
    path('task_form/',CreateTask.as_view(), name='create-task'),
    path('view_task/',ViewTask.as_view(), name= 'view-task'),
    path('task_details/<int:id>/', TaskDetails.as_view(), name='task_details'),
    path('update_tast/<int:id>/',UpdateTask.as_view(),name='update_task'),
    path('delete_task/<int:id>/',DeleteTask.as_view(),name='delete_task'),
    path('dashboard', dashboard, name='dashboard')
]