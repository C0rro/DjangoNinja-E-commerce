from datetime import timezone, timedelta

from django.apps import AppConfig
from django.contrib.auth import authenticate, login, logout as django_logout
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.utils import timezone
from uuid import UUID

from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from django.shortcuts import get_object_or_404, redirect
from backend.models import Peperoncino, Product, Order
from backend.schemas import ProductSchema, PeperoncinoSchema, PeperoncinoUpdateSchema, OrderSchema, LoginSchema, UserSchema

from ninja.security import SessionAuth

app = NinjaAPI()

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        import backend.signals

@app.get("/products/", response=list[ProductSchema])
def get_products(request):
    return Product.objects.all()

@app.get("/products/", response=list[ProductSchema])
def get_products_filter(request, family):
    return Product.objects.filter(peperoncino__family=family)

@app.get("/products/new", response=list[ProductSchema])
def get_products_new(request):
    recent_products = []
    seven_days_ago = timezone.now() - timedelta(days=30)

    for product in Product.objects.all():
        if product.date_added > seven_days_ago:
            recent_products.append(product)

    return recent_products
@app.get("/peperoncini/{slug}/", response=PeperoncinoSchema)
def get_peperoncino(request, slug: str):
    peperoncino = get_object_or_404(Peperoncino, slug=slug)
    return peperoncino

@app.get("/products/{id}/", response=ProductSchema)
def get_product_by_id(request, id: str):
    product = get_object_or_404(Product, id=id)
    return product

@app.post("/peperoncini/modifica/{id}/", response=PeperoncinoSchema)
def update_peperoncino(request, id: UUID, data: PeperoncinoUpdateSchema):
    peperoncino = get_object_or_404(Peperoncino, id=id)

    for attr, value in data.dict(exclude_unset=True).items():
        setattr(peperoncino, attr, value)

    peperoncino.save()
    return peperoncino

@app.get("/peperoncini/", response=list[PeperoncinoSchema])
def get_peperoncini(request):
    return Peperoncino.objects.all()

@app.get("/protected", auth=SessionAuth(), response=UserSchema)
def protected_view(request):
    return request.auth


@app.post("/login/")
def user_login(request: HttpRequest, payload: LoginSchema):
    user = authenticate(request, username=payload.username, password=payload.password)

    if user is not None:
        login(request, user)
        response = HttpResponse('Login OK', status=200)

        return response
    else:
        return 401, {"message": "Nome utente o password non validi"}

@app.post("/logout/")
def logout(request):
    django_logout(request)
    return 200, { "message": "Logout con successo."}

@app.post("/shop/carrello/checkout", auth=[SessionAuth(), None])
@transaction.atomic
def crea_ordine(request: HttpRequest, payload: OrderSchema):

    user_fk = request.auth if request.auth else None

    ordine = Order.objects.create(
        user=user_fk,
        email=payload.email,
        total_price=payload.total_price,
        products=payload.products,
        status=Order.OrderStatus.PENDING,

        shipping_name=payload.shipping_name,
        shipping_address=payload.shipping_address,
        shipping_city=payload.shipping_city,
        shipping_province=payload.shipping_province,
        shipping_postal_code=payload.shipping_postal_code,
        shipping_phone=payload.shipping_phone,
    )

    return 200, {"id": ordine.id, "message": "Ordine creato con successo."}

