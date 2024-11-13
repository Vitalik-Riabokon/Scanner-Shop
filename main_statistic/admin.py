from django.contrib import admin

from main_statistic.models import Image, Payment, PaymentProduct, Product

from .models import Image, Payment, PaymentProduct, Product


# Додаємо проміжну модель PaymentProduct в адмінку
class PaymentProductInline(admin.TabularInline):
    model = PaymentProduct
    extra = 1  # Додаємо один порожній рядок для додавання нових продуктів


# Налаштовуємо адмінку для Payment, додаючи inline продукти
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    inlines = [PaymentProductInline]  # Включаємо PaymentProduct як inline форму
    list_display = [
        "id",
        "payment_method",
        "payment_date",
        "is_active",
    ]  # поля для відображення
    list_filter = [
        "payment_method",
        "is_active",
    ]  # фільтрація по методах оплати і статусу
    search_fields = ["id"]  # пошук по ID платежу


# Налаштовуємо адмінку для Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "product_name",
        "barcode",
        "price",
        "is_active",
        "owner",
    ]  # поля для відображення
    list_filter = ["is_active"]  # фільтр по активності
    search_fields = ["product_name", "barcode"]  # пошук по назві та штрих-коду


# Налаштовуємо адмінку для Image
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["description", "is_active"]  # поля для відображення
    list_filter = ["is_active"]  # фільтр по активності


# Реєстрація проміжної моделі PaymentProduct для окремого адміністрування (якщо потрібно)
@admin.register(PaymentProduct)
class PaymentProductAdmin(admin.ModelAdmin):
    list_display = ["payment", "product", "quantity"]  # відображення полів
    search_fields = [
        "payment__id",
        "product__product_name",
    ]  # пошук по ID платежу та назві продукту
