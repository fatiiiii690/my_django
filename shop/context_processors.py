def cart(request):
    data = request.session.get("cart", {})
    count = sum(int(qty) for qty in data.values())
    return {"cart_count": count}
