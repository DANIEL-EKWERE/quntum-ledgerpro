from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import re


@require_POST
def subscribe(request):
    email = request.POST.get('email', '').strip()
    if not email or not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
    # TODO: save to DB or send to mailing list
    return JsonResponse({'success': True, 'message': 'Thank you for subscribing!'})


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
