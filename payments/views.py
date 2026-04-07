from django.shortcuts import render
from .services import import_payments


def import_payments_view(request):
    if request.method == "POST":
        file = request.FILES.get('file')

        import_payments(file)

        return render(request, 'payments/success.html')

    return render(request, 'payments/import.html')