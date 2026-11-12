from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    """Producto tecnológico disponible en el catálogo."""

    class Categoria(models.TextChoices):
        LAPTOPS = "Laptops", "Laptops"
        SMARTPHONES = "Smartphones", "Smartphones"
        AUDIO = "Audio", "Audio"
        MONITORES = "Monitores", "Monitores"
        ACCESORIOS = "Accesorios", "Accesorios"

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    categoria = models.CharField(max_length=50, choices=Categoria.choices)
    stock = models.PositiveIntegerField(default=0)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} ({self.categoria})"

    @property
    def disponible(self):
        return self.stock > 0

    @property
    def stock_bajo(self):
        return 0 < self.stock <= 5
