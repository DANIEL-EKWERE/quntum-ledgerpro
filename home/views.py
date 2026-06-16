from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def crypto(request):
    return render(request, 'home/crypto.html')

def cookie_policy(request):
    return render(request, 'home/cookie-policy.html')

def privacy_policy(request):
    return render(request, 'home/privacy-policy.html')

def terms(request):
    return render(request, 'home/terms.html')

def trade_policy(request):
    return render(request, 'home/trade-policy.html')
