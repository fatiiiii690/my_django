from django.db import models
from django.urls import reverse
from transliterate import translit


class Category(models.Model):
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField("URL", max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория"
    )
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField(
        "URL",
        max_length=220,
        unique=True,
        blank=True
    )
    description = models.TextField("Описание")
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2
    )
    image = models.ImageField(
        "Изображение",
        upload_to="products/",
        blank=True,
        null=True
    )
    is_available = models.BooleanField(
        "В наличии",
        default=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = translit(
                self.name,
                "ru",
                reversed=True
            ).lower().replace(" ", "-")

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "product_detail",
            args=[self.slug]
        )


class Order(models.Model):
    STATUS_CHOICES = [
        ("new", "Новый"),
        ("confirmed", "Подтверждён"),
        ("delivery", "В доставке"),
        ("done", "Выполнен"),
        ("cancelled", "Отменён"),
    ]

    name = models.CharField(
        "Имя",
        max_length=100
    )
    phone = models.CharField(
        "Телефон",
        max_length=30
    )
    address = models.CharField(
        "Адрес доставки",
        max_length=255
    )
    comment = models.TextField(
        "Комментарий",
        blank=True
    )
    total = models.DecimalField(
        "Сумма",
        max_digits=10,
        decimal_places=2,
        default=0
    )
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    created_at = models.DateTimeField(
        "Создан",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ №{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Заказ"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name="Товар"
    )
    price = models.DecimalField(
        "Цена",
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        "Количество",
        default=1
    )

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
