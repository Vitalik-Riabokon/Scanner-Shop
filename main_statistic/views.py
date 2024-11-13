from datetime import timedelta
from typing import Any

from django.db.models import F, Sum
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from main_statistic.forms import CalendarForm

from .models import Payment, PaymentProduct


@csrf_exempt
@require_POST
def update_quantity(request: Any) -> JsonResponse:
    """
    Обробник запиту для оновлення кількості продукту у платіжному записі.

    Цей метод обробляє POST-запит, що містить ID продукту платіжної інформації
    та нову кількість. Якщо нова кількість більше 0, оновлює кількість; якщо
    кількість 0 або менше, видаляє продукт з платежу. Якщо після видалення
    залишилися продукти, платіж залишається активним; інакше він позначається
    як неактивний.

    Args:
        request (HttpRequest): Запит, отриманий від клієнта.

    Returns:
        JsonResponse: JSON з інформацією про статус операції.
    """
    payment_product_id: str = request.POST.get(
        "payment_product_id"
    )  # ID продукту платіжної інформації.
    new_quantity: int = int(request.POST.get("quantity", 0))  # Нова кількість продукту.

    try:
        payment_product: PaymentProduct = PaymentProduct.objects.get(
            id=payment_product_id
        )  # Отримуємо продукт платіжної інформації.
        payment: Payment = payment_product.payment  # Отримуємо пов'язаний платіж.

        if new_quantity > 0:  # Якщо нова кількість більше 0, оновлюємо.
            payment_product.quantity = new_quantity
            payment_product.save()
            return JsonResponse(
                {"status": "success", "action": "updated"}
            )  # Повертаємо успішний статус.
        else:  # Якщо нова кількість 0 або менше, видаляємо продукт.
            payment_product.delete()

            # Перевіряємо, чи залишилися продукти в платіжному записі.
            if not payment.payment_products.exists():
                payment.is_active = False  # Позначаємо платіж як неактивний.
                payment.save()

            return JsonResponse(
                {"status": "success", "action": "deleted"}
            )  # Повертаємо статус видалення.

    except PaymentProduct.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Payment product not found"}, status=404
        )  # Помилка, якщо продукт не знайдено.
    except ValueError:
        return JsonResponse(
            {"status": "error", "message": "Invalid quantity"}, status=400
        )  # Помилка для недійсної кількості.


class PaymentListView(ListView):
    model = Payment
    template_name = "statistic/main_page.html"
    context_object_name = "payments"
    paginate_by = 9

    def get_queryset(self) -> list[Payment]:
        """
        Повертає запит для отримання активних платежів.

        Фільтрує активні платежі за датою, якщо вона вказана в запиті.

        Returns:
            List[Payment]: Список активних платежів.
        """
        queryset = Payment.objects.filter(is_active=True).prefetch_related(
            "payment_products__product"
        )

        date: str = self.request.GET.get("date")  # Отримуємо дату з запиту.
        if date:
            queryset = queryset.filter(payment_date=date)  # Фільтруємо за датою.

        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Додає додаткові контекстні дані до шаблону.

        Включає форму для вибору дати та обчислює дохід за день, тиждень
        і місяць на основі вибраної дати.

        Args:
            **kwargs: Додаткові контекстні дані.

        Returns:
            Dict[str, Any]: Контекстні дані для шаблону.
        """
        context = super().get_context_data(**kwargs)
        payments = context["payments"]

        # Отримуємо форму календаря
        if self.request.GET.get("date"):
            form = CalendarForm(self.request.GET)
        else:
            form = CalendarForm()

        context["form"] = form

        if form.is_valid():
            selected_date = form.cleaned_data["date"]  # Вибрана дата з форми.
        else:
            selected_date = timezone.now().date()  # Поточна дата, якщо форма недійсна.

        # Обчислюємо дохід
        context["daily_income"] = self.calculate_daily_income(selected_date)
        context["weekly_income"] = self.calculate_weekly_income(selected_date)
        context["monthly_income"] = self.calculate_monthly_income(selected_date)

        if form.is_valid():
            date = form.cleaned_data["date"]
            purchases = Payment.objects.filter(
                payment_date=date, is_active=True
            )  # Фільтруємо покупки за датою.
            context["purchases"] = purchases

        for payment in payments:
            total_payment_sum: float = sum(
                payment_product.quantity * payment_product.product.price
                for payment_product in payment.payment_products.all()
            )
            payment.total_payment_sum = (
                total_payment_sum  # Додаємо загальну суму платежу до об'єкта.
            )

        return context

    @staticmethod
    def calculate_daily_income(date: Any) -> float:
        """
        Обчислює щоденний дохід.

        Args:
            date (Any): Дата для обчислення.

        Returns:
            float: Загальна сума доходу за день.
        """
        return (
            Payment.objects.filter(payment_date=date, is_active=True).aggregate(
                total=Sum(
                    F("payment_products__quantity")
                    * F("payment_products__product__price")
                )
            )["total"]
            or 0.0
        )  # Повертаємо загальний дохід або 0, якщо даних немає.

    @staticmethod
    def calculate_weekly_income(date: Any) -> float:
        """
        Обчислює щотижневий дохід.

        Args:
            date (Any): Дата для обчислення.

        Returns:
            float: Загальна сума доходу за тиждень.
        """
        start_of_week: Any = date - timedelta(days=date.weekday())  # Початок тижня.
        end_of_week: Any = start_of_week + timedelta(days=6)  # Кінець тижня.
        return (
            Payment.objects.filter(
                payment_date__range=[start_of_week, end_of_week], is_active=True
            ).aggregate(
                total=Sum(
                    F("payment_products__quantity")
                    * F("payment_products__product__price")
                )
            )[
                "total"
            ]
            or 0.0
        )  # Повертаємо загальний дохід або 0, якщо даних немає.

    @staticmethod
    def calculate_monthly_income(date: Any) -> float:
        """
        Обчислює щомісячний дохід.

        Args:
            date (Any): Дата для обчислення.

        Returns:
            float: Загальна сума доходу за місяць.
        """
        return (
            Payment.objects.filter(
                payment_date__year=date.year,
                payment_date__month=date.month,
                is_active=True,
            ).aggregate(
                total=Sum(
                    F("payment_products__quantity")
                    * F("payment_products__product__price")
                )
            )[
                "total"
            ]
            or 0.0
        )  # Повертаємо загальний дохід або 0, якщо даних немає.
