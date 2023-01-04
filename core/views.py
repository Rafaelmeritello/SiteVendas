from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from .models import Produto, Dados, Imagem
from .forms import Produtoform, Contaform
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from .categoriasprodutos import getsubcategorias, categorias
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import UpdateView
# index
def index(request):

    # p = Produto(nome="nome", preco=20, descricao="descricao", vendedor=Dados.objects.all().get(user=request.user),
    #              categoria="informatica", subcategoria="Monitor")
    # p.save()

    tamanho = range(3)
    context = {

        'produtos': Produto.objects.all().order_by('destaquegeral').exclude(destaquegeral=0),
        'tamanho': tamanho
    }
    return render(request, 'index.html', context)
    pass


# adicionar produto
def formadd(request):

    #verificar se usuario é anonimo
    if request.user.id == None:
        return redirect('/')
    #fim- verificar se usuario é anonimo

    #variavel para definir se o produto vai ser criado
    criar = True
    # fim- variavel para definir se o produto vai ser criado

    # pegar subcategorias da categoria
    if request.is_ajax():
        categoria = request.GET.get('categoria')
        print(getsubcategorias(categoria))
        return JsonResponse({'subcategorias': getsubcategorias(categoria)}, status=200)
        pass
    # fim- pegar subcategorias da categoria

    # captar arquivos e imagens multiplas do formulario
    files = request.FILES
    imgprinc = dict(files).get('imagemprincipal')
    imgs = dict(files).get('imagens')

    # se houver multiplas imagens
    if imgs is not None:
        files = {}
        if len(imgs) > 2:
            messages.error(request, "Selecione no maximo 2 imagens")
            criar = False
    # fim- se houver multiplas imagens

    # fim - captar arquivos e imagens multiplas do formulario

    form = Produtoform(request.POST or None, files or None)

    # Dados do limite de anuncios
    dados = Dados.objects.all().get(user=request.user)
    limite = dados.limite_anuncio
    dados.anuncios_atuais =len(Produto.objects.all().filter(vendedor=dados))
    anunciado = dados.anuncios_atuais
    # fim -Dados do limite de anuncios
    if request.method == 'POST':
        if form.is_valid():

            nome = form.cleaned_data['nome']
            preco = str(form.cleaned_data['preco']).replace(',','.')
            descricao = form.cleaned_data['descricao']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']
            preco = float(preco)
            # verificando se o usuario escolheu uma subcategoria
            if subcategoria.lower() == "selecione um item" or categoria.lower() == "selecione um item":
                messages.error(request,"Selecione uma categoria e uma subcategoria")
                criar = False
            # fim- verificando se o usuario escolheu uma subcategoria
            if request.user.id is None:
                messages.error(request, "você precisa estar logado")
                criar = False
            else:

                if anunciado < limite and criar == True:

                    p = Produto(nome=nome, preco=preco,descricao=descricao, vendedor=Dados.objects.all().get(user=request.user), categoria = categoria, subcategoria = subcategoria,
                                imagemprincipal=imgprinc[0])
                    dados.anuncios_atuais += 1

                    dados.save()

                    p.save()
                    # criar multiplas imagens
                    if imgs is not None:

                        for img in imgs:
                            Imagem.objects.all().create(imagem=img, produto=p)
                    #fim criar multiplas imagens
                    return redirect('meusprodutos')
                elif anunciado >= limite:
                    messages.error(request,"Numero maximo de anuncios Realizados")

    context = {
        'form': form,
        'limite': limite,
        'atual': anunciado
    }
    return render(request, 'add.html', context)
    pass


# registrar usuario
def registro(request):
    tamanho = 48

    def erro(mensagem):
        messages.error(request, mensagem)
        pass
    form = Contaform(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # Autorização para criar usuario após validação
            criar = True
            # Fim - Autorização para criar usuario após validação

            # coletando dados
            dados = {
                'senha': form.cleaned_data['Senha'],
                'repetir': form.cleaned_data['RepetirSenha'],
                'nome': form.cleaned_data['Nome'],
                'email': form.cleaned_data['Email'],
                'pix': form.cleaned_data['Pix'],
                'sobrenome': form.cleaned_data['Sobrenome'],
                'telefone': form.cleaned_data['Telefone']
            }
            # fim - coletando dados de

            # validando dados

            if dados['senha'] != dados['repetir']:
                print(len(messages.get_messages(request)))
                erro("As senhas nao são iguais")
                tamanho+=4
                criar = False
                # verificando se a senha são apenas numeros
            try:
                a=int(dados['senha'])
                criar = False
                erro( "A senha deve conter letras e numeros.")
                tamanho +=4
            except:
                pass
            # Fim- verificando se a senha são apenas numeros

            # fim- validando dados

            # criando usuario
            if criar:
                try:
                    Usuario = User(username=dados['email'], email=dados['email'])
                    Usuario.set_password(dados['senha'])
                    print(Usuario.password)
                    print(Usuario.username)
                    dados_extras = Dados(user=Usuario, nome=dados['nome'], sobrenome=dados['sobrenome'],chave_pix=dados['pix'], Telefone=dados['telefone'] )
                    Usuario.save()
                    dados_extras.save()
                    messages.success(request, 'Usuario criado')
                    tamanho +=4
                except:
                    erro( 'Erro ao criar, verifique se o email ja esta cadastrado')
                    tamanho +=4
                pass

                # fim- criando usuario
        else:
            erro('Verifique as informações ')
            tamanho+=4
        pass
    pass

    context = {
        'form': form,
        'tamanho':tamanho,
    }
    return render(request, 'registro.html', context)
    pass


# logout
def logout(request):
    logout(request)
    pass

#meus produtos
def meusprodutos(request):

    if request.user.id is None:
        return redirect('/')
    dados = Dados.objects.all().get(user=request.user)
    limite = dados.limite_anuncio
    dados.anuncios_atuais =len(Produto.objects.all().filter(vendedor=dados))
    anunciado = dados.anuncios_atuais
    vendedor = Dados.objects.all().get(user=request.user)
    if request.method == 'POST':
        id = str(request.body).split('id=')[1].replace("'",'')
        Produto.objects.all().get(id=id).delete()
        return redirect('meusprodutos')
    produtos = Produto.objects.all().filter(vendedor=vendedor)
    tamanho = range(3)

    context={
        'produtos':produtos,
        'tamanho': tamanho,
        'atuais': anunciado,
        'limite': limite,
    }
    return render(request, 'meusprodutos.html',context)
    pass
#fim- meus produtos





#Produtos lista
def produtos(request,categoria, subcategoriaurl='destaques'):
    destaque = False

    #veirficar se é destaq ue
    if subcategoriaurl == 'destaques':
        destaque = True
    # fim- verificar se é destaque
    #verificar se subcategoria existe
    if not getsubcategorias(categoria).__contains__(subcategoriaurl):
        if subcategoriaurl != 'destaques':
            return redirect('/')

    #fim- verificar se subcategoria existe
    # verificar se categoria existe
    if categorias.get(categoria) is None:
        return redirect('/')

    produtos = Produto.objects.all().filter(categoria=categoria, subcategoria=subcategoriaurl)

    # fim-verificar se categoria existe

    #variaveis
    titulo = f'{str(categoria.capitalize()).capitalize()}/{subcategoriaurl.capitalize()}'
    pag = 1 if request.GET.get('page') is None else request.GET.get('page')
    tamanho = range(3)

    #fim -variaveis

    #filtrando
    if request.method == 'POST':
        sub = request.POST.get('subcategoria')
        if not sub.lower() == 'selecione':
            produtos = produtos.filter(subcategoria = sub)
            return redirect(f'/produtos/{categoria}/{sub}')
        else:
            return redirect(f'/produtos/{categoria}')
        pass
    #fim - filtrando

    #pegando subcategorias
    if request.is_ajax():
        categoria = request.GET.get('categoria')
        sub = getsubcategorias(categoria)
        return JsonResponse({'subcategorias': sub},status=200)
    #fim - pegando subcategorias



    pagin = Paginator(produtos.order_by('preco'), 28)
    if destaque:
        produtos = Produto.objects.all().filter(categoria=categoria)
        pagin = Paginator(produtos.order_by('destaquecategoria').exclude(destaquecategoria=0), 28)
    produtos = pagin.page(pag).object_list
    page = pagin.get_page(pag)
    context = {
    'categoria': categoria,
    'produtos':produtos,
    'tamanho':tamanho,
    'titulo':titulo,
    'page':page,
    }

    return render(request,'produtos.html',context)


    pass
#fim - produtos lista


#ver produtos
class verproduto(View):

    def get(self,request, id):

        p = Produto.objects.all().get(id=id)
        print(p.id)
        vendedor = p.vendedor
        context = {
        'produto': p,
        'imagens': Imagem.objects.all().filter(produto= p),
        'vendedor': vendedor,
        }
        return render(request, 'produto.html', context)
        pass
    pass
#fim- ver produto


# Editar produto
@method_decorator(login_required, name='dispatch')
class Editar(UpdateView):
    login_url = '/contas/login'
    model = Produto

    template_name = 'editar.html'
    fields = [
        'nome',
        'preco',
    ]

    success_url = '/meusprodutos'
    pass
# fim- editar produto


class editarconta(View):

    def get(self,request,**kwargs):
        return render(request,'editarconta.html')
        pass

    pass