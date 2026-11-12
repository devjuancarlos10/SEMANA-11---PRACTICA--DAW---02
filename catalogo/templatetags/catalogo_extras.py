from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def moneda(valor, simbolo="S/"):
    """Formatea un número como moneda: 1299.9 -> 'S/ 1,299.90'."""
    try:
        cantidad = Decimal(str(valor))
    except (InvalidOperation, TypeError, ValueError):
        return valor
    return f"{simbolo} {cantidad:,.2f}"
