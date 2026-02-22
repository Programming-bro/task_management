from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from users.forms import CustomRegisterFrorm, AssignRoleForm, CreateGroupForm, LoginForm
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.views.generic import FormView, TemplateView, ListView, UpdateView

from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='Admin').exists()

class SignUp(FormView):
    template_name = "registration/register.html"
    form_class = CustomRegisterFrorm
    success_url = reverse_lazy("sign_in")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get("password1"))
        user.is_active = False
        user.save()

        messages.success(
            self.request,
            "A Confirmation mail sent. Please check your email"
        )

        return super().form_valid(form)


class SignIn(LoginView):
    template_name = 'registration/signin.html'
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.POST.get('next') or self.request.GET.get('next')
        if next_url:
            return next_url
        return reverse_lazy('home')

class SignOut(LoginRequiredMixin, LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('sign_in')
    
def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found')
    
class AdminDashboard(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/dashboard.html'
    login_url = reverse_lazy('sign_in')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context
    
    def test_func(self):
        return is_admin(self.request.user)

class AssignRole(LoginRequiredMixin,UserPassesTestMixin,FormView):
    template_name = "admin/assign_role.html"
    form_class = AssignRoleForm
    success_url = reverse_lazy("admin_dashboard")

    def test_func(self):
        return is_admin(self.request.user)

    def handle_no_permission(self):
        from django.shortcuts import redirect
        return redirect("no-permission")

    def dispatch(self, request, *args, **kwargs):
        self.user_obj = get_object_or_404(User, id=kwargs["user_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        role = form.cleaned_data.get("role")

        self.user_obj.groups.clear() 
        self.user_obj.groups.add(role)

        messages.success(
            self.request,
            f"User {self.user_obj.username} has been assigned to the {role.name} role"
        )
        return super().form_valid(form)

class CreateGroup(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/create_group.html'
    login_url = 'no-permission'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', CreateGroupForm())
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create_group')
    def test_func(self):
        return is_admin(self.request.user)


class GroupList(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'admin/group_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.prefetch_related('permissions').all()
        return context
    def test_func(self):
        return is_admin(self.request.user)