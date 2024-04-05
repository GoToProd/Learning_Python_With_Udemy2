from django.contrib import admin

from products.models import Product, ProductCategory, Basket



admin.site.register(ProductCategory)
admin.site.register(Basket)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'quantity')
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'category')
    readonly_fields = ('description',)
    search_fields = ('name',)
    ordering = ('name',)
    

class BasketAdmin(admin.TabularInline):
    model = Basket
    readonly_fields = ('created_timestamp',)
    fields = ('product', 'quantity', 'created_timestamp')
    extra = 0
    
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural ='корзины'
