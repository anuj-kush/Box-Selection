import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from .models import Product, Box
from .packing import select_box

MAX_UNITS = 50

def home(request):
    return render(request, "shipping/home.html", {"products": Product.objects.order_by("id"), "boxes": Box.objects.filter(active=True).order_by("cost", "id")})

@require_POST
def recommend(request):
    if request.content_type != "application/json":
        return JsonResponse({"error": "Use application/json."}, status=415)
    try:
        data = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    if not isinstance(data, dict) or set(data) != {"items"}:
        return JsonResponse({"error": "Provide an object containing only items."}, status=400)
    items = data["items"]
    if not isinstance(items, list) or not 1 <= len(items) <= MAX_UNITS:
        return JsonResponse({"error": "Provide 1–50 item rows."}, status=400)
    quantities = {}
    for row in items:
        if not isinstance(row, dict) or set(row) != {"product_id", "quantity"} or any(type(row[k]) is not int or row[k] <= 0 for k in ("product_id", "quantity")):
            return JsonResponse({"error": "Each row needs positive integer product_id and quantity."}, status=400)
        quantities[row["product_id"]] = quantities.get(row["product_id"], 0) + row["quantity"]
    if sum(quantities.values()) > MAX_UNITS:
        return JsonResponse({"error": "At most 50 total units per request."}, status=400)
    if any(pk > 9223372036854775807 for pk in quantities):
        return JsonResponse({"error": "Product ID out of range."}, status=400)
    products = Product.objects.in_bulk(quantities)
    missing = sorted(set(quantities) - set(products))
    if missing:
        return JsonResponse({"error": "Unknown products.", "product_ids": missing}, status=400)
    units = [{"product_id": pk, "unit": n+1, "size": products[pk].dimensions} for pk, qty in sorted(quantities.items()) for n in range(qty)]
    weight = sum(products[pk].weight_g * qty for pk, qty in quantities.items())
    return JsonResponse(select_box(units, weight, Box.objects.filter(active=True)))
