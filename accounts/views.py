from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from accounts.forms import SignUpForm
from django.contrib import messages


def user_logout(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER', '/'))  # zůstat na stejné stránce


class UserRegisterView(FormView):
    template_name = 'registration/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Registrace proběhla úspěšně. Přihlaš se.')
        return super().form_valid(form)