from django.db import models
from clientes.models import Cliente

class Processo(models.Model):
    numero = models.CharField(max_length=25, unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=[
        ('andamento', 'Em andamento'),
        ('concluido', 'Concluído'),
        ('arquivado', 'Arquivado'),
    ])
    descricao = models.TextField(blank=True, null=True)
    data_abertura = models.DateTimeField()

    def __str__(self):
        return f"{self.numero} - {self.cliente.nome}"
    
class Documento(models.Model):
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='documentos')
    arquivo = models.FileField(upload_to='documentos/')
    descricao = models.CharField(max_length=100, blank=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.descricao} - {self.arquivo.name}"