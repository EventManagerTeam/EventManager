from django.shortcuts import render


def error_404_view(request):
    return render(request, 'custom_errors/404.html')
