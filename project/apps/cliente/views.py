from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from . import forms, models


def index(request):
    clientes_registros = models.Cliente.objects.all()
    contexto = {"clientes": clientes_registros}
    return render(request, "cliente/index.html", contexto)


def crear_clientes_predeterminados(request):
    from datetime import date

    # Crear instancias de países
    p1 = models.Pais.objects.create(nombre="Perú")
    p2 = models.Pais.objects.create(nombre="México")
    p3 = models.Pais.objects.create(nombre="El Salvador")

    # Crear instancias de clientes
    models.Cliente.objects.create(
        nombre="Almendra", apellido="Ruiseñor", nacimiento=date(2015, 1, 1), pais_origen_id=p1
    )
    models.Cliente.objects.create(
        nombre="Giordana", apellido="Tapello", nacimiento=date(2005, 2, 2), pais_origen_id=p2
    )
    models.Cliente.objects.create(nombre="Macarena", apellido="Litter", nacimiento=date(1990, 3, 3), pais_origen_id=p3)
    models.Cliente.objects.create(
        nombre="Jhiordana", apellido="Perez", nacimiento=date(2005, 2, 2), pais_origen_id=None
    )
    return redirect("cliente:index")


def prueba_búsqueda(request):
    from datetime import date

    # Búsqueda por nombre que contenga "dana"
    clientes_nombre = models.Cliente.objects.filter(nombre__contains="dana")

    # Búsqueda por fecha de nacimiento mayor a 2000
    clientes_nacimiento = models.Cliente.objects.filter(nacimiento__gt=date(2000, 1, 1))

    # Búsqueda por país de origen vacío
    clientes_pais = models.Cliente.objects.filter(pais_origen_id=None)

    contexto = {
        "clientes_nombre": clientes_nombre,
        "clientes_nacimiento": clientes_nacimiento,
        "clientes_pais": clientes_pais,
    }
    return render(request, "cliente/resultados_busqueda.html", contexto)


def crear_cliente(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = forms.Cliente(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("cliente:index"))
    else:
        form = models.Cliente()
    return render(request, "cliente/crear.html", {"form": form})
