from services.models import ServiceCategory
from services.forms.category_form import ServiceCategoryForm
from django.views.generic import ListView, CreateView, UpdateView, View
from django.shortcuts import redirect, render, get_object_or_404


class ServiceCategoryCreateView(CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'categories/category_form.html'
    success_url = '/services/categories/'  # Redireciona para a lista de categorias após a criação

class ServiceCategoryListView(ListView):
    model = ServiceCategory
    template_name = 'categories/category_list.html'
    context_object_name = 'categories'

class ServiceCategoryUpdateView(UpdateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'categories/category_form.html'
    success_url = '/services/categories/'  # Redireciona para a lista de categorias após a atualização

class ServiceCategoryDeleteView(View):

    def get(self, request, pk):
        category = ServiceCategory.objects.get(id=pk)
        return render(request, 'categories/category_delete.html', {'category': category})
    
    def post(self, request, pk):
        category_id = get_object_or_404(ServiceCategory, pk=pk).id
        category = ServiceCategory.objects.get(id=category_id)
        category.is_active = False  # Marca a categoria como inativa em vez de excluí-la permanentemente
        category.save()
        return redirect('/services/categories/')  # Redireciona para a lista de categorias após a exclusão