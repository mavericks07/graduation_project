from django.contrib import admin
from .models import Consumable, Classification, Stock, PickList, Pick


class ConsumableAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'consumable', 'number', 'storagesite', 'supplier')


class PickAdmin(admin.ModelAdmin):
    list_display = ('id', 'stock', 'number', 'lab')


class PickListAdmin(admin.ModelAdmin):
    list_display = ('id',)


admin.site.register(Consumable, ConsumableAdmin)
admin.site.register(Classification, ClassificationAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Pick, PickAdmin)
admin.site.register(PickList, PickListAdmin)
