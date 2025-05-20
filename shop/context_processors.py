from django.db.models import Sum

def cart_item_count(request):
    from .models import Order
    pending_order = (
        Order.objects
             .filter(ordered_by=request.user, status='PENDING')
             .order_by('-ordered_on')
             .first()
    )
    if not pending_order:
        return {'cart_item_count': 0}
    
    total_qty = pending_order.items.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    return {'cart_item_count': total_qty}
