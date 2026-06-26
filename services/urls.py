from django.urls import path

'''
urlpatterns = [
    #--------------------------------------------------------------------------------------------#
    path('', ..., name='service-list'),                        # Listar Serviços
    path('create/', ..., name='service-create'),               # Criar Serviço
    path('<int:pk>/', ..., name='service-detail'),             # Visualizar Serviço Especifico
    #--------------------------------------------------------------------------------------------#
    path('<int:pk>/reject/', ..., name='service-reject'),      # Prestador Rejeitar Serviço
    path('<int:pk>/update/', ..., name='service-update'),      # Atualizar Dados do Serviço
    path('<int:pk>/cancel/', ..., name='service-cancel'),      # Cancelar Solicitação de Serviço
    path('<int:pk>/accept/', ..., name='service-accept'),      # Prestador Aceitar Serviço
    path('<int:pk>/schedule/', ..., name='service-schedule'),  # Agendar Serviço
    path('<int:pk>/displace/', ..., name='service-displace'),  # Deslocamento do Prestador
    path('<int:pk>/complete/', ..., name='service-complete'),  # Finalizar Serviço
    #--------------------------------------------------------------------------------------------#
    path('providers/', ..., name='provider-list'),             # Listar Prestadores de Serviço
    path('categories/', ..., name='category-list'),            # Listar Categorias de Serviço
    #--------------------------------------------------------------------------------------------#
]

'''