from services.models import ServiceCategory
from services.forms.category_form import ServiceCategoryForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class ServiceCategoryCreateView(CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'categories/category_form.html'
    success_url = '/services/categories/'  # Redireciona para a lista de categorias após a criação

class ServiceCategoryListView(ListView):
    model = ServiceCategory
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'