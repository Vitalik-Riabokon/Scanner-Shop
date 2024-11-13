from pathlib import Path
from typing import Any
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.

User = get_user_model()


def get_image_path(
    instance: Any, filename: str, subfolder: Path = Path("uploads")
) -> Path:
    """
    Генерує шлях для збереження зображення з унікальним ім'ям.

    Ця функція приймає ім'я файлу, генерує унікальне ім'я на основі
    початкового імені файлу, використовуючи slugification та UUID,
    а також визначає підкаталог для збереження зображення.

    Args:
        instance (Any): Екземпляр моделі, що викликає цю функцію.
                        Використовується для контексту (необхідно, але не використовується безпосередньо).
        filename (str): Початкове ім'я файлу зображення.
        subfolder (Path, optional): Підкаталог, в якому зберігатиметься зображення.
                                    За замовчуванням — "uploads".

    Returns:
        Path: Повний шлях до файлу зображення з новим унікальним іменем.
    """
    # Генерація нового імені файлу з унікальним UUID
    filename = (
        f"{slugify(filename.partition('.')[0])}_{uuid4()}" + Path(filename).suffix
    )
    # Повертаємо шлях до файлу
    return Path(subfolder) / filename


class Image(models.Model):
    image = models.ImageField(upload_to=get_image_path)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ["description"]


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="products")
    barcode = models.BigIntegerField(null=False)
    image = models.ForeignKey(Image, on_delete=models.PROTECT, related_name="products")
    product_name = models.CharField(null=False, max_length=150)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ["product_name"]


class PaymentProduct(models.Model):
    payment = models.ForeignKey(
        "Payment", on_delete=models.CASCADE, related_name="payment_products"
    )
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="payment_products"
    )
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} of {self.product.product_name} in payment {self.payment.id}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("готівка", "Готівка"),
        ("карта", "Карта"),
    ]

    products = models.ManyToManyField("Product", through="PaymentProduct")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHOD_CHOICES, null=False
    )
    payment_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.payment_date:
            self.payment_date = timezone.now().date()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Payment {self.id} - {self.payment_method} on {self.payment_date}"
