from django.conf.urls.static import static
from django.urls import path

from .views import index,formadd, logout,registro, meusprodutos, produtos, verproduto, Editar, editarconta

urlpatterns = [
    path('',index, name='index'),
    path('add', formadd, name='add'),
    path('logout', logout, name='logout'),
    path('CriarConta', registro, name='criarconta'),
    path('meusprodutos', meusprodutos, name='meusprodutos'),
    path('produtos/<str:categoria>/<str:subcategoriaurl>/', produtos, name='produtos'),
    path('produtos/<str:categoria>', produtos, name='produtos'),
    path('produto/<int:id>',verproduto.as_view(), name='produto' ),
    path('<pk>/editarproduto', Editar.as_view(), name='editar'),
    path('editar/<int:id>', editarconta.as_view(), name='editarconta')
]
