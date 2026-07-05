from django.urls import path
from services.views import service_views, category_views


app_name = 'services'

urlpatterns = [
    path('', service_views.ServiceListView.as_view(), name='service_list'),            # Listar Serviços
    path('create/', service_views.ServiceCreateView.as_view(), name='service_create'), # Criar Serviço
    #path('<int:pk>/', ..., name='service-detail'),             # Visualizar Serviço Especifico

    path('categories/', category_views.ServiceCategoryListView.as_view(), name='category_list'),                     # Listar Categorias
    path('categories/create/', category_views.ServiceCategoryCreateView.as_view(), name='category_create'),          # Criar Categoria
    path('categories/<int:pk>/update/', category_views.ServiceCategoryUpdateView.as_view(), name='category_update'), # Atualizar Categoria
    path('categories/<int:pk>/delete/', category_views.ServiceCategoryDeleteView.as_view(), name='category_delete'), # Deletar Categoria

#
    #path('<int:pk>/reject/', ..., name='service-reject'),      # Prestador Rejeitar Serviço
    #path('<int:pk>/update/', ..., name='service-update'),      # Atualizar Dados do Serviço
    #path('<int:pk>/cancel/', ..., name='service-cancel'),      # Cancelar Solicitação de Serviço
    #path('<int:pk>/accept/', ..., name='service-accept'),      # Prestador Aceitar Serviço
    #path('<int:pk>/schedule/', ..., name='service-schedule'),  # Agendar Serviço
    #path('<int:pk>/displace/', ..., name='service-displace'),  # Deslocamento do Prestador
    #path('<int:pk>/complete/', ..., name='service-complete'),  # Finalizar Serviço
#
    #path('providers/', ..., name='provider-list'),             # Listar Prestadores de Serviço
    #path('categories/', ..., name='category-list'),            # Listar Categorias de Serviço
]
