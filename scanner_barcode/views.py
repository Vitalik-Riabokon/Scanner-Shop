import json
from typing import Any, Dict, List

from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from main_statistic.models import Payment, PaymentProduct, Product


def scan_barcode(request: Any) -> JsonResponse:
    """
    Обробник запиту для сканування штрих-коду.

    Цей метод обробляє POST-запит, що містить штрих-код продукту. Якщо продукт
    з таким штрих-кодом існує в базі даних, повертається інформація про продукт
    у форматі JSON. У разі відсутності продукту повертається відповідь з помилкою.

    Args:
        request (HttpRequest): Запит, отриманий від клієнта.

    Returns:
        JsonResponse or render:
            - JsonResponse: Якщо запит POST, то повертає JSON з інформацією про продукти.
            - render: Якщо запит не POST, то повертає HTML-шаблон 'base_scan.html'.
    """
    if request.method == "POST":
        barcode: str = request.POST.get("barcode")  # Отримуємо штрих-код з POST-запиту.
        products: List[Product] = Product.objects.filter(
            barcode=barcode, is_active=True
        )  # Фільтруємо активні продукти за штрих-кодом.

        if products.exists():  # Перевіряємо, чи існують продукти з таким штрих-кодом.
            response_data: Dict[str, Any] = {
                "success": True,
                "products": [
                    {
                        "id": product.id,
                        "name": product.product_name,
                        "price": str(
                            product.price
                        ),  # Перетворюємо ціну на рядок для JSON.
                        "image": product.image.image.url,  # URL зображення продукту.
                    }
                    for product in products
                ],
            }
        else:
            response_data: Dict[str, Any] = {
                "success": False,
                "message": "Товар не знайдено",  # Повідомлення про відсутність продукту.
            }
        return JsonResponse(response_data)  # Повертаємо JSON-відповідь.
    return render(request, "base_scan.html")  # Повертаємо HTML-шаблон для GET-запиту.


@csrf_exempt
def confirm_purchase(request: Any) -> JsonResponse:
    """
    Обробник запиту для підтвердження покупки.

    Цей метод обробляє POST-запит, який містить дані про продукти та метод оплати.
    Він створює новий запис у базі даних для платежу та асоційованих з ним продуктів.

    Args:
        request (HttpRequest): Запит, отриманий від клієнта.

    Returns:
        JsonResponse: JSON з інформацією про успішність операції та ID платежу.
    """
    if request.method == "POST":
        products_data: List[Dict[str, Any]] = json.loads(
            request.POST.get("products_data")
        )  # Десеріалізація JSON.
        payment_method: str = request.POST.get(
            "payment_method"
        )  # Отримуємо метод оплати.

        # Створюємо новий запис для платежу
        payment: Payment = Payment(
            payment_method=payment_method, payment_date=timezone.now().date()
        )
        payment.save()  # Зберігаємо платіж у базі даних.

        # Проходимо через всі продукти і створюємо записи в PaymentProduct
        for product_data in products_data:
            product_id: int = product_data["id"]  # ID продукту.
            quantity: int = product_data["quantity"]  # Кількість продукту.

            try:
                product: Product = Product.objects.get(
                    id=product_id
                )  # Спробуємо отримати продукт за ID.
                # Створюємо запис про платіж для цього продукту.
                PaymentProduct.objects.create(
                    payment=payment, product=product, quantity=quantity
                )
            except Product.DoesNotExist:
                # Якщо продукт не знайдено, повертаємо помилку.
                return JsonResponse(
                    {
                        "success": False,
                        "message": f"Продукт з ID {product_id} не знайдено",
                    }
                )

        return JsonResponse(
            {"success": True, "payment_id": payment.id}
        )  # Повертаємо успішну відповідь з ID платежу.

    return JsonResponse(
        {"success": False, "error": "Invalid request method"}
    )  # Помилка для недійсного методу запиту.
