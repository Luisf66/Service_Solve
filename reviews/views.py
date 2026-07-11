from django.shortcuts import render, redirect, get_object_or_404
from reviews.forms.review_form import ReviewForm
from services.models import Service, ServiceStatusHistory
# Create your views here.


def service_review(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)

    # Só quem é o client e só se o serviço estiver 'completed' pode avaliar
    #if service.status != 'scheduled' or service.client != request.user:
    #    return redirect('services:service_detail', pk=service_pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.save(commit=False)
            rating.service = service
            rating.reviewer = request.user
            rating.reviewee = service.provider

            rating.save()

            service.status = 'rated'
            service.save()

            ServiceStatusHistory.objects.create(
                service=service,
                previous_status='completed',
                new_status='rated',
                changed_by=request.user
            )
            return redirect('services:service_detail', pk=service_pk)
    else:
        form = ReviewForm()

    return render(request, 'review_create.html', {
        'service': service,
        'form': form,
    })