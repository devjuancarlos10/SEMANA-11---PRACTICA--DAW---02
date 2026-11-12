from django.test import TestCase
from django.urls import reverse

from .models import Producto


class CatalogoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Producto.objects.create(nombre="laptop pro", precio=3500, categoria="Laptops", stock=4)
        Producto.objects.create(nombre="mouse", precio=80, categoria="Accesorios", stock=0)
        Producto.objects.create(nombre="audífonos", precio=250, categoria="Audio", stock=10)

    def test_home_responde_200(self):
        respuesta = self.client.get(reverse("home"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "home.html")
        self.assertEqual(respuesta.context["total_productos"], 3)

    def test_catalogo_ordenado_por_precio(self):
        respuesta = self.client.get(reverse("catalogo"))
        self.assertEqual(respuesta.status_code, 200)
        precios = [p.precio for p in respuesta.context["productos"]]
        self.assertEqual(precios, sorted(precios))

    def test_catalogo_muestra_agotado(self):
        respuesta = self.client.get(reverse("catalogo"))
        self.assertContains(respuesta, "Agotado")
        self.assertContains(respuesta, "Laptop Pro")  # filtro |title
        self.assertContains(respuesta, "S/ 3,500.00")  # filtro |moneda

    def test_filtro_por_categoria(self):
        respuesta = self.client.get(reverse("catalogo"), {"categoria": "Audio"})
        self.assertEqual(len(respuesta.context["productos"]), 1)

    def test_filtro_solo_disponibles(self):
        respuesta = self.client.get(reverse("catalogo"), {"disponibles": "1"})
        self.assertTrue(all(p.stock > 0 for p in respuesta.context["productos"]))
        self.assertNotContains(respuesta, "Agotado")

    def test_categoria_invalida_se_ignora(self):
        respuesta = self.client.get(reverse("catalogo"), {"categoria": "xyz"})
        self.assertEqual(len(respuesta.context["productos"]), 3)
