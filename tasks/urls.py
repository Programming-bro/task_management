from django.urls import path
from tasks.views import manager_dahsboard, user_dashboard, test, test_form, view_task, delete_task, update_task

urlpatterns = [
    path('manager_dashboard/',manager_dahsboard, name='manager_dashboard'),
    path('user_dashboard/',user_dashboard),
    path('test/',test),
    path('test_form/',test_form),
    path('view_task/',view_task),
    path('update_dast/<int:id>/',update_task,name='update_task'),
    path('delete_task/<int:id>/',delete_task,name='delete_task')
]