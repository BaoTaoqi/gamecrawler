from django.contrib import admin
from .models import Depository, ErrorCheck


# Register your models here.


class DepositoryAdmin(admin.ModelAdmin):
    model = Depository
    list_display = ('GameName', 'ID', 'Link', 'OriginalPrice', 'LastPrice', 'FinalPrice', 'LowestPrice')
    list_filter = ['DiscountPct', 'BundleBaseDiscount']
    search_fields = ['GameName', 'ID', 'Link', 'OriginalPrice', 'LastPrice', 'FinalPrice', 'LowestPrice', 'BundleBaseDiscount', 'DiscountPct']


class ErrorCheckAdmin(admin.ModelAdmin):
    model = ErrorCheck
    list_display = ('ID', 'Link', 'IfHandle')


admin.site.register(Depository, DepositoryAdmin)
admin.site.register(ErrorCheck, ErrorCheckAdmin)
