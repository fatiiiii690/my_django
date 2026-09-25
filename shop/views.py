from decimal import Decimal

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderForm
from .models import Category, Order, OrderItem, Product


def _cart_items(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys()).select_related("category")
    result = []
    total = Decimal("0")
    for product in products:
        quantity = int(cart.get(str(product.id), 0))
        subtotal = product.price * quantity
        result.append({"product": product, "quantity": quantity, "subtotal": subtotal})
        total += subtotal
    return result, total


def home(request):
    products = Product.objects.filter(is_available=True)[:6]
    categories = Category.objects.all()
    return render(request, "shop/home.html", {"products": products, "categories": categories})


def catalog(request, slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).select_related("category")
    current_category = None

    if slug:
        current_category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=current_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, "shop/catalog.html", {
        "products": products,
        "categories": categories,
        "current_category": current_category,
        "query": query,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    return render(request, "shop/product_detail.html", {"product": product})


def cart_view(request):
    items, total = _cart_items(request)
    return render(request, "shop/cart.html", {"items": items, "total": total})


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = request.session.get("cart", {})
    key = str(product.id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    messages.success(request, f"«{product.name}» добавлен в корзину.")
    return redirect(request.META.get("HTTP_REFERER", "catalog"))


def cart_remove(request, product_id):
    cart = request.session.get("cart", {})
    key = str(product_id)
    if key in cart:
        del cart[key]
        request.session["cart"] = cart
    return redirect("cart")


def checkout(request):
    items, total = _cart_items(request)
    if not items:
        messages.info(request, "Корзина пуста.")
        return redirect("catalog")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.total = total
            order.save()
            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["product"].price,
                    quantity=item["quantity"],
                )
            request.session["cart"] = {}
            return redirect("order_success", order_id=order.id)
    else:
        form = OrderForm()

    return render(request, "shop/checkout.html", {"form": form, "items": items, "total": total})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "shop/order_success.html", {"order": order})
