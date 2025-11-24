from decimal import Decimal
from django.contrib import admin
from backend.models import Peperoncino, Product, ImmaginePeperoncino, UserProfile, Order

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Informazioni Aggiuntive Profilo'
    fields = ('address', 'city', 'province', 'postal_code', 'phone_number')


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    inlines = (UserProfileInline,)

    list_display = BaseUserAdmin.list_display + ('get_phone_number', 'is_active')

    def get_phone_number(self, obj):
        return obj.profile.phone_number

    get_phone_number.short_description = 'Telefono'


def product_available(modeladmin, request, queryset):
    queryset.update(available=True)

def product_10_percent_sale(modeladmin, request, queryset):
    for each in queryset:
        each.price = each.price - (each.price * Decimal('0.10'))
        each.save()

class ImmaginePeperoncinoInline(admin.TabularInline):
    model = ImmaginePeperoncino
    extra = 1
    fields = ('file', 'ordine')

class ProductAdmin(ModelAdmin):
    list_display = ["peperoncino", "price", "quantity", "available"]
    actions = [product_available, product_10_percent_sale]


class PeperoncinoAdmin(ModelAdmin):
    inlines = [ImmaginePeperoncinoInline]
    list_display = ['name', 'family', 'description', 'scoville']

class OrderAdmin(ModelAdmin):
    list_display = ["user", "email", "status", "products", "created_at", "total_price"]


admin.site.register(Order, OrderAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Peperoncino, PeperoncinoAdmin)


