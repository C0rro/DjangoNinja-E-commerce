from typing import Optional
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db.models.fields import UUIDField
from ninja import ModelSchema, Schema
from pydantic import Field

from backend.models import Peperoncino, Product, Order, UserProfile

User = get_user_model()

# Schema base Peperoncino
class PeperoncinoSchema(ModelSchema):
    class Config:
        model = Peperoncino
        model_fields = ['id', 'name', 'family', 'description', 'scoville', 'image', 'slug']

class ImmaginePeperoncinoSchema(Schema):
    id: UUID
    file: str
    ordine: Optional[int]

# Schema Product con nested Peperoncino
class ProductSchema(ModelSchema):
    peperoncino: PeperoncinoSchema
    class Config:
        model = Product
        model_fields = ['id', 'price', 'quantity', 'available', 'date_added', 'peperoncino']


class UserProfileSchema(ModelSchema):
    class Config:
        model = UserProfile
        model_fields = ['address', 'city', 'province', 'postal_code', 'phone_number']


class UserSchema(ModelSchema):
    profile: UserProfileSchema

    class Config:
        model = User
        model_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active']

class OrderSchema(ModelSchema):
    user: Optional[UserSchema] = None

    class Config:
        model = Order
        model_fields = [
            'id',
            'status',
            'email',
            'total_price',
            'products',
            'shipping_name',
            'shipping_address',
            'shipping_city',
            'shipping_province',
            'shipping_postal_code',
            'shipping_phone',
        ]


# Schema per la creazione
class PeperoncinoCreateSchema(Schema):
    name: str
    family: str
    description: str
    scoville: int
    image: str | None = None

# Schema per l'aggiornamento (PUT/PATCH)
class PeperoncinoUpdateSchema(Schema):
    name: str | None = None
    family: str | None = None
    description: str | None = None
    scoville: int | None = None
    image: str | None = None

class LoginSchema(Schema):
    username: str = Field(..., title="Nome Utente")
    password: str = Field(..., title="Password")