from decimal import Decimal
from multiupload.fields import MultiImageField
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .categoriasprodutos import categorias, getcategorias

class Produtoform(forms.Form):

    nome = forms.CharField(max_length=40, label="Nome", min_length=4)
    preco = forms.DecimalField(decimal_places=2, label="Preço",validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(99999999)])
    descricao = forms.CharField(widget=forms.Textarea, label="Descrição", max_length=1500)
    choices = getcategorias(True)
    categoria = forms.CharField(widget=forms.Select(choices=choices))
    subcategoria = forms.CharField(widget=forms.Select(choices=[('Selecione um Item', "Selecione um Item")]))
    imagemprincipal = forms.ImageField(label='Imagem Principal', required=False)
    imagens =  MultiImageField( max_num=2, required=False)
    pass


class Contaform(forms.Form):
    Nome = forms.CharField(max_length=16,  min_length=3)
    Sobrenome = forms.CharField(max_length=56)
    Email = forms.EmailField()
    Pix = forms.CharField(max_length=30,min_length=6)
    Senha = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    RepetirSenha = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    Telefone = forms.CharField(min_length=11, max_length=11, label='Telefone/Whatsapp')
    pass

class editarconta(forms.Form):
    Senha = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)
    RepetirSenha = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=32)


    pass