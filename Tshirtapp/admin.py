from django.contrib import admin
from Tshirtapp.models import *

# Register your models here.
class SizeVarientConfiguration(admin.StackedInline):
    model=SizeVarient

class TshirtConfiguration(admin.ModelAdmin):
    inlines=[SizeVarientConfiguration]
    list_display=['name','slug']
    list_editable=['slug']

admin.site.register(Tshirt,TshirtConfiguration)
admin.site.register(Occasion)
admin.site.register(IdealFor)
admin.site.register(Sleeve)
admin.site.register(NeckType)
admin.site.register(Color)
admin.site.register(Brand)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)




