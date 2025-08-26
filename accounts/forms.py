from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django import forms

from accounts.models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'email', 'password1', 'password2']

    @atomic
    def save(self, commit=True):
        user = super().save(commit)
        user.email = self.cleaned_data.get('email')

        profile = Profile(user=user, email=user.email)
        if commit:
            profile.save()
        return user
