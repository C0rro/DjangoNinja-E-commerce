
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django_extensions.db.fields import AutoSlugField
from django.db import models
import uuid


# Create your models here.
User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Utente"
    )

    address = models.CharField(max_length=255, verbose_name="Indirizzo 1")
    city = models.CharField(max_length=100, verbose_name="Città")
    province = models.CharField(max_length=2, verbose_name="Provincia")
    postal_code = models.CharField(max_length=20, verbose_name="Codice Postale")

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Numero di Telefono"
    )

    def __str__(self):
        return f"Profilo di {self.user.username}"


class Peperoncino(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=120, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    family = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='images/peperoncini/', null=True, blank=True)
    scoville = models.PositiveIntegerField(help_text="Unità Scoville di piccantezza")


    def __str__(self):
        return self.name


class ImmaginePeperoncino(models.Model):
    peperoncino = models.ForeignKey(
        Peperoncino,
        on_delete=models.CASCADE,
        related_name='galleria',
        verbose_name="Peperoncino Correlato"
    )

    file = models.ImageField(
        upload_to='images/peperoncini/galleria/',
        verbose_name="File Immagine Secondaria"
    )

    ordine = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Immagine Secondaria"
        verbose_name_plural = "Immagini Secondarie"
        ordering = ['ordine']

    def __str__(self):
        return f"Immagine Galleria per {self.peperoncino.name}"

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    peperoncino = models.ForeignKey(Peperoncino, on_delete=models.CASCADE, related_name='prodotti')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.peperoncino.name} - €{self.price}"

    class Meta:
        ordering = ['-date_added']


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING', 'In Attesa'
        PROCESSING = 'PROCESSING', 'In Elaborazione'
        SHIPPED = 'SHIPPED', 'Spedito'
        DELIVERED = 'DELIVERED', 'Consegnato'
        CANCELLED = 'CANCELLED', 'Cancellato'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='orders',
        null=True,
        blank=True,
    )

    email = models.EmailField(blank=True)

    shipping_name = models.CharField(max_length=255, verbose_name="Nome e Cognome Spedizione")
    shipping_address = models.CharField(max_length=255, verbose_name="Indirizzo Spedizione")
    shipping_city = models.CharField(max_length=100, verbose_name="Città Spedizione")
    shipping_province = models.CharField(max_length=100, verbose_name="Provincia")
    shipping_postal_code = models.CharField(max_length=20, verbose_name="Codice Postale Spedizione")
    shipping_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefono Spedizione")

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
        verbose_name="Stato Ordine"
    )

    total_price = models.DecimalField(max_digits=8, decimal_places=2)

    products = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ordine {self.id} - Stato: {self.status}"

