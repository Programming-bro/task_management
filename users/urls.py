from django.urls import path
from users.views import SignUp, SignIn, SignOut, activate_user, AdminDashboard, AssignRole, CreateGroup, GroupList
from core.views import no_permission

urlpatterns = [
    path("sign_up/",SignUp.as_view(), name = "sign_up"),
    path("sign_in/",SignIn.as_view(), name = "sign_in"),
    path("sign_out/",SignOut.as_view(), name = "sign_out"),
    path('activate/<int:user_id>/<str:token>/', activate_user),
    path('admin/dashboard/',AdminDashboard.as_view(), name="admin_dashboard"),
    path('admin/<int:user_id>/assign_role/', AssignRole.as_view(), name='assign_role'),
    path('admin/create_group/', CreateGroup.as_view(), name='create_group'),
    path('admin/group_list/', GroupList.as_view(), name='group_list'),
    path('no_permission/',no_permission,name='no-permission')
    
]
