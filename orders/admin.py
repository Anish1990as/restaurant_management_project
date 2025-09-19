from django.contrib import admin
from .models import Coupon
from .utils import generate_coupon_code

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_percent', 'valid_from', 'valid_to', 'active')
    search_fields = ('code',)
    list_filter = ('active', 'valid_from', 'valid_to')

    # Auto-generate code if not set
    def save_model(self, request, obj, form, change):
        if not obj.code:
            obj.code = generate_coupon_code()
        super().save_model(request, obj, form, change)