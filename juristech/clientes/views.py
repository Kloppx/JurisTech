from django.shortcuts import render, redirect
from .models import Cliente
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        if Cliente.objects.filter(cpf=cpf).exists():
            messages.error(request, "Já existe um cliente com esse CPF.")
        else:
            Cliente.objects.create(nome=nome, cpf=cpf, email=email, telefone=telefone)
            messages.success(request, "Cliente cadastrado com sucesso!")
            return redirect('cadastrar_cliente')
        
    return render(request, 'clientes/cadastrar_cliente.html')
