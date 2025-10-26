from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contas/', views.ContaListView.as_view(), name='conta_list'),
    path('conta/<int:pk>/', views.ContaDetailView.as_view(), name='conta_detail'),
    path('conta/criar/', views.criar_conta, name='criar_conta'),
    path('conta/<int:pk>/deposito/', views.efetuar_deposito, name='efetuar_deposito'),
    path('conta/<int:pk>/saque/', views.efetuar_saque, name='efetuar_saque'),
    path('conta/<int:pk>/transferencia/', views.efetuar_transferencia, name='efetuar_transferencia'),
    # URLs PIX
    path('conta/<int:pk>/pix/', views.efetuar_pix, name='efetuar_pix'),
    path('conta/<int:pk>/pix/cadastrar/', views.cadastrar_chave_pix, name='cadastrar_chave_pix'),
    path('conta/<int:pk>/pix/chaves/', views.listar_chaves_pix, name='listar_chaves_pix'),
    path('conta/<int:pk>/pix/chave/<int:chave_id>/desativar/', views.desativar_chave_pix, name='desativar_chave_pix'),
]
