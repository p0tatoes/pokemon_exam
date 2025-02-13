from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from examproject.forms import RegisterUserForm

User = get_user_model()


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterUserForm
    template_name = "auth/user-form.html"
    success_url = reverse_lazy("pokemon-list")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("pokemon-list")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_type"] = "register"

        return context


class LoginUserView(LoginView):
    redirect_authenticated_user = True
    template_name = "auth/user-form.html"
    next_page = reverse_lazy("pokemon-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_type"] = "login"

        return context
