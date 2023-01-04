from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Dados(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    chave_pix = models.CharField(max_length=50)
    limite_anuncio = models.IntegerField(default=3, editable=True)
    anuncios_atuais =  models.IntegerField( default=0,editable=True)
    data_criacao = models.DateField(auto_now_add=True, editable=False)
    Telefone = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.nome}:{self.sobrenome}+ {self.anuncios_atuais}/{self.limite_anuncio}'
    pass


class Produto(models.Model):
    nome = models.CharField(max_length=50)
    vendedor = models.ForeignKey(Dados, on_delete=models.CASCADE, editable=False)
    preco = models.DecimalField(decimal_places=2, max_digits=9)
    descricao = models.TextField(max_length=1500, default='')
    data_publicacao = models.DateField(auto_now_add=True, editable=False)
    tempo = models.TimeField(auto_now=True)
    categoria = models.CharField(max_length=20)
    subcategoria = models.CharField(max_length=20)
    destaquecategoria = models.IntegerField(default=0)
    destaquegeral = models.IntegerField(default=0)
    imagemprincipal = models.ImageField(upload_to='produtos/principal/%Y/%m', blank=True)
    def __str__(self):
        return f'{self.nome} : {self.vendedor} '
    pass



class Imagem(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    imagem = models.ImageField(upload_to='produtos/secundaria/%y/%m')
    primaria = models.BooleanField(default=False)
    pass
