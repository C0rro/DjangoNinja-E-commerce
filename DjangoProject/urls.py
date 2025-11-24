from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from backend.api import app
from backend.views import home, shop, peperoncini, aggiungi_al_carrello, carrello, rimuovi_dal_carrello, login, \
    checkout, user_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', app.urls, name='api'),
    path('', home, name='home'),
    path('shop/', shop, name='shop'),
    path('shop/carrello', carrello, name='carrello'),
    path('shop/checkout', checkout, name='carrello'),
    path('login/', login, name='login'),
    path('user_page/', user_page, name='user'),

    path('shop/<str:id>/', peperoncini, name='product_detail'),
    path('shop/aggiungi_al_carrello/<str:id>', aggiungi_al_carrello, name='aggiungi al carrello'),
    path('shop/rimuovi_dal_carrello/<str:id>', rimuovi_dal_carrello, name='rimuovi dal carrello'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
