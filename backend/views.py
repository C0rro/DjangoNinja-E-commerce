import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import request

from backend.models import Peperoncino, Product


# Create your views here.
def home(request):
    return render(request, "home.html")

def shop(request):
    return render(request, "shop.html")

def peperoncini(request, id):
    return render(request, "product_detail.html", context={"id": id})


def aggiungi_al_carrello(request, id):
    if request.method == 'POST':

        id_str = str(id)

        if "cart" not in request.session:
            request.session['cart'] = {}

        list_item = request.session['cart']

        if id_str in list_item:
            list_item[id_str]['quantity'] += 1
        else:
            list_item[id_str] = {'quantity': 1}

        request.session.modified = True

        return JsonResponse({'message': 'Prodotto aggiunto al carrello con successo!'})

    return JsonResponse({'message': 'Metodo non consentito.'}, status=405)


def rimuovi_dal_carrello(request, id):

    if request.method == 'POST':
        if "cart" in request.session:
            list_item = request.session['cart']

            if id in list_item:
                list_item.pop(id)
                request.session.modified = True
                request.session['cart'] = list_item
                return  JsonResponse({'message': 'Prodotto rimosso dal carrello!'})
        else:
            return JsonResponse({'message': 'Errore carrello non trovato!'})

    return JsonResponse({'message': 'Metodo errato'})

def carrello(request):

    if "cart" in request.session:
        cart = request.session['cart']
        cart_json = json.dumps(cart)
        print(cart_json)
    else:
        cart_json = {}
    return render(request, "carrello.html", context={"cart": cart_json})

def login(request):
    return render(request, "login.html")

def checkout(request):
    if "cart" in request.session:
        cart = request.session['cart']
        cart_json = json.dumps(cart)
        print(cart_json)
    else:
        cart_json = {}
    return render(request, "checkout.html", context={"cart": cart_json})

def user_page(request):
    return render(request, "user_page.html")