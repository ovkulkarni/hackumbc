from django.shortcuts import render


def fourohfour_response_view(request):
    return render(request, 'errors/404.html', {})


def fivehundred_response_view(request):
    return render(request, 'errors/500.html', {})
