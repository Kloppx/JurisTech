from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('listar_processos')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'usuarios/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if senha != confirmar_senha:
            messages.error(request, 'As senhas não coincidem.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já em uso.')
        else:
            User.objects.create_user(username=username, password=senha)
            messages.success(request, 'Usuário criado com sucesso! Faça o login.')
            return redirect('login')
        
    return render(request, 'usuarios/register.html')
