from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.catalog, name="catalog"),

    re_path(
        r"^category/(?P<slug>[-\w]+)/$",
        views.catalog,
        name="category",
    ),

    re_path(
        r"^product/(?P<slug>[-\w]+)/$",
        views.product_detail,
        name="product_detail",
    ),

    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path("checkout/", views.checkout, name="checkout"),
    path(
        "order/success/<int:order_id>/",
        views.order_success,
        name="order_success",
    ),
]
