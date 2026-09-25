from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    help = "Создаёт демонстрационные категории и товары BioFlora"

    def handle(self, *args, **options):
        data = {
            "Букеты": [
                ("Нежная классика", "Букет из свежих роз в пастельных оттенках.", 2800),
                ("Весеннее настроение", "Яркая композиция из тюльпанов и зелени.", 2400),
                ("Белая мечта", "Элегантный белый букет для особенного события.", 3200),
            ],
            "Розы": [
                ("Розовый рассвет", "Букет нежно-розовых роз.", 3500),
                ("Красная страсть", "Классические красные розы.", 4200),
            ],
            "Подарки": [
                ("Цветы и сладости", "Букет с коробкой шоколадных конфет.", 3900),
                ("Флорариум", "Мини-сад в стильной стеклянной композиции.", 2600),
            ],
        }

        for category_name, products in data.items():
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": category_name.lower().replace(" ", "-")},
            )
            for name, description, price in products:
                slug = name.lower().replace(" ", "-")
                Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        "category": category,
                        "name": name,
                        "description": description,
                        "price": price,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Демо-данные BioFlora созданы."))
