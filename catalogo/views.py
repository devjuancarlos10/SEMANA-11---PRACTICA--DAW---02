import logging

from django.db import DatabaseError
from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import ListView

from .models import Producto

logger = logging.getLogger(__name__)


# VISTA BASADA EN FUNCIÓN (FBV)
def home(request):
    """Página de bienvenida con un resumen del catálogo."""
    contexto = {
        "titulo": "Bienvenido al Catálogo de Productos Tecnológicos",
        "total_productos": 0,
        "total_unidades": 0,
        "categorias": [],
        "destacados": [],
    }
    try:
        contexto["total_productos"] = Producto.objects.count()
        contexto["total_unidades"] = (
            Producto.objects.aggregate(total=Sum("stock"))["total"] or 0
        )
        contexto["categorias"] = (
            Producto.objects.values("categoria")
            .annotate(cantidad=Count("id"))
            .order_by("categoria")
        )
        contexto["destacados"] = Producto.objects.filter(stock__gt=0).order_by(
            "-precio"
        )[:3]
    except DatabaseError:
        # Si la base de datos no está migrada la página igual se muestra.
        logger.exception("No se pudo consultar la base de datos")
        contexto["error"] = (
            "No se pudo cargar la información del catálogo. "
            "Ejecute las migraciones e inténtelo de nuevo."
        )
    return render(request, "home.html", contexto)


# VISTA BASADA EN CLASE (CBV)
class ProductoListView(ListView):
    """Listado de productos con filtros por categoría y disponibilidad."""

    model = Producto
    template_name = "catalogo.html"
    context_object_name = "productos"

    def get_queryset(self):
        # QuerySet base ordenado por precio (aún no se ejecuta: es lazy).
        queryset = Producto.objects.order_by("precio")

        categoria = self.request.GET.get("categoria", "").strip()
        if categoria in Producto.Categoria.values:
            queryset = queryset.filter(categoria=categoria)

        if self.request.GET.get("disponibles") == "1":
            queryset = queryset.filter(stock__gt=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categorias"] = Producto.Categoria.values
        context["categoria_actual"] = self.request.GET.get("categoria", "")
        context["solo_disponibles"] = self.request.GET.get("disponibles") == "1"
        context["total_disponibles"] = Producto.objects.filter(stock__gt=0).count()
        context["total_agotados"] = Producto.objects.filter(stock=0).count()
        return context
