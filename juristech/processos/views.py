from django.shortcuts import render, redirect, get_object_or_404
from .models import Processo, Documento
from clientes.models import Cliente
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from processos.models import Processo

@login_required(login_url='login')
def cadastrar_processo(request):
    if request.method == 'POST':
        numero = request.POST.get('numero')
        cliente_id = request.POST.get('cliente')
        tipo = request.POST.get('tipo')
        status = request.POST.get('status')
        descricao = request.POST.get('descricao')
        data_abertura = request.POST.get('data_abertura')

        if Processo.objects.filter(numero=numero).exists():
            messages.error(request, "Já existe um processo com esse número.")
        else:
            cliente = Cliente.objects.get(id=cliente_id)
            Processo.objects.create(
                numero=numero,
                cliente=cliente,
                tipo=tipo,
                status=status,
                descricao=descricao,
                data_abertura=data_abertura
            )
            messages.success(request, "Processo cadastrado com sucesso!")
            return redirect('cadastrar_processo')

    clientes = Cliente.objects.all()
    return render(request, 'processos/cadastrar_processo.html', {'clientes': clientes})

@login_required(login_url='login')
def listar_processos(request):
    processos = Processo.objects.select_related('cliente').all().order_by('-data_abertura')
    return render(request, 'processos/listar_processos.html', {'processos': processos})

@login_required(login_url='login')
def upload_documento(request, processo_id):
    processo = Processo.objects.get(id=processo_id)

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo')
        descricao = request.POST.get('descricao')

        if arquivo:
            Documento.objects.create(
                processo=processo,
                arquivo=arquivo,
                descricao=descricao
            )
            messages.success(request, 'Documento enviado com sucesso!')
            return redirect('detalhar_processo', processo_id=processo.id)
        
    return render(request, 'processos/upload_documento.html', {'processo': processo})

@login_required(login_url='login')
def detalhar_processo(request, processo_id):
    processo = Processo.objects.get(id=processo_id)
    documentos = processo.documentos.all()  # usa o related_name='documentos'

    return render(request, 'processos/detalhar_processo.html', {
        'processo': processo,
        'documentos': documentos
    })

@login_required(login_url='login')
def home_view(request):
    context = {
        'processos_count': Processo.objects.count(),
        'clientes_count': Cliente.objects.count(),
        'documentos_count': Documento.objects.count(),
    }
    return render(request, 'home.html', context)

def editar_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    clientes = Cliente.objects.all()  # Para o select de cliente

    if request.method == 'POST':
        processo.numero = request.POST.get('numero')
        processo.cliente = Cliente.objects.get(id=request.POST.get('cliente'))
        processo.tipo = request.POST.get('tipo')
        processo.status = request.POST.get('status')
        processo.descricao = request.POST.get('descricao')
        data_abertura_str = request.POST.get('data_abertura')

        processo.data_abertura = datetime.strptime(data_abertura_str, '%Y-%m-%d').date()
        processo.save()

        return redirect('detalhar_processo', processo_id=processo.id)

    return render(request, 'processos/editar_processo.html', {'processo': processo, 'clientes': clientes})