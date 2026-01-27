from django.urls import path
from tasks.views import manager_dahsboard, user_dashboard, test, test_form, view_task

urlpatterns = [
    path('manager_dashboard/',manager_dahsboard),
    path('user_dashboard/',user_dashboard),
    path('test',test),
    path('test_form',test_form),
    path('view_task',view_task)
]