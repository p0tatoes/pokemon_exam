from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password",
        ]
