from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.http import HttpResponse
from .forms import ProfileForm, UserForm
from .models import ValidateEmail, User
import re

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    

    if request.method == 'POST':
        if 'email' in request.POST:
            email = request.POST['email']
            password = request.POST['password']
            user_login = authenticate(username=email, password=password)
            email_validated = ValidateEmail.objects.filter(email=email)
            if user_login:
                login(request, user_login)
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('home')
            elif email_validated:
                messages.error(request, "El correo no ha sido validado. Revisa tu correo y da clic al enlace de validación")
            else:
                messages.error(request, "El email o la contraseña son incorrectos")

    return render(request, 'views/login.html', {})



def logout_view(request):
    logout(request)
    return redirect('home')



def register_view(request):
    try:
        if request.method == "POST":
            regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
            if 'email' in request.POST and not re.fullmatch(regex, request.POST['email']):
                messages.error(request, f'El correo ingresado es erroneo')
                return redirect('register')
            if 'password' not in request.POST or 'password_confirm' not in request.POST or not request.POST['password']:
                messages.error(request, f'No se recibió la contraseña')
                return redirect('register')
            if request.POST['password'] != request.POST['password_confirm']:
                messages.error(request, f'El campo contraseña y confirmar contraseña no coinciden')
                return redirect('register')
            if len(request.POST['password']) < 8: 
                messages.error(request, f'La contraseña es demasiado corta')
                return redirect('register')

            User.objects.create_user(
                email=request.POST['email'],
                password=request.POST['password']
            )

            messages.success(request, f"Nuevo usuario creado. Revisa tu correo para validar tu email")
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('home')
    except:
        messages.error(request, f'Algo ha salido mal. Intentelo más tarde')
    
    return render(request, 'views/register.html', {})



class ProfileView(View):

    def get(self, request):
        context = {
            'user_form': UserForm(instance=request.user),
            'profile_form': ProfileForm(instance=request.user.profile),
        }
        return render(request, 'views/profile.html', context)

    def post(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile Updated Successfully!")
        else:
            messages.error(request, "Error Updating Profile!")

        context = {
            'user_form': user_form,
            'profile_form': ProfileForm(instance=request.user.profile)
        }

        return render(request, 'views/profile.html', context)


def validate_email(request, id):
    validate = ValidateEmail.objects.get(id=id)
    validate.user.is_active = True
    validate.user.save()
    validate.delete()

    return HttpResponse("Su correo ha sido validado!")