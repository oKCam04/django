from django.shortcuts import render
from appPeliculas.models import Genero, Pelicula
from django.http import JsonResponse
from django.db import Error
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# def inicio(request):
#     return render(request, "AgregarGenero.html")
# Genero -----------------------------------------------------------------------------------------------------------------
@csrf_exempt
def agregarGenero(request):
    try:
        nombre=request.POST['txtNombre']
        genero=Genero(genNombre=nombre)
        genero.save()
        mensaje="Genero guardado"
    except Error as e:
        mensaje=str(e)
    retorno={"mensaje":mensaje}
    #return JsonResponse(retorno)
    return render(request, "AgregarGenero.html", retorno)

def vistaAgregarGenero(request):
    return render(request, "AgregarGenero.html")


def listarGeneros(request):
    try:
        generos=Genero.objects.all().values()
        print(generos)
        mensaje=None
    except Error as e:
        mensaje=str(e)
    retorno={"mensaje":mensaje, "generos":list(generos)}
    return JsonResponse(retorno, content_type='application/json')


# ----------------------------------------------------------------------------------------------------------

@csrf_exempt

def agregarPelicula(request):
    try:
        codigo=request.POST['txtCodigo']
        titulo=request.POST['txtTitulo']
        protagonista=request.POST['txtProtagonista']
        duracion=int(request.POST['txtDuracion'])
        resumen=request.POST['txtResumen']
        foto=request.FILES['filefoto']
        idGenero=int(request.POST['cbGenero'])
        genero=Genero.objects.get(pk=idGenero)
        pelicula=Pelicula(pelCodigo=codigo, pelTitulo=titulo,pelProtagonista=protagonista, pelDuracion=duracion,
                          pelResumen=resumen,pelFoto=foto, pelGenero=genero)
        pelicula.save()
        mensaje="pelicula agregada correctamente"
    except Error as e:
        mensaje=str(e)
    retorno={"mensaje":mensaje, "idPelicula":pelicula.id}
    return JsonResponse(retorno)

def listarPeliculas(request):
    peliculas=Pelicula.objects.all().values()
    print(peliculas)
    retorno={"peliculas":list(peliculas)}
    return JsonResponse(retorno, content_type='application/json')