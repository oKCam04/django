from django.shortcuts import render
from django.db import Error   
from appPeliculas.models import Pelicula, Genero
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from django.shortcuts import render, redirect
from django.contrib import messages





# Create your views here.
# Genero ---------------------------------------------------------------------------------------
@csrf_exempt
def agregarGenero(request):
    try:
        #recibir el nombre del genero en una variable local
        nombre = request.POST['txtNombre']
        # crear objeto de tipo genero
        genero = Genero(genNombre=nombre)
        # salvar el objeto, lo que permite que sea
        # creado en la base de datos
        genero.save()
        mensaje = "Genero Agregado Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    return redirect('inicio')
   

@csrf_exempt
def vistaAgregarGenero(request):
    return render(request, "agregarGenero.html")

# pelicula ---------------------------------------------------------------------------------------
@csrf_exempt
def listarPeliculas(request):
    peliculas= Pelicula.objects.all().values()
    print(peliculas)
    retorno = {"peliculas": list(peliculas)} 
    return JsonResponse(retorno, content_type="application/json")   

@csrf_exempt
def vistaListarPelicula(request):
    peliculas= Pelicula.objects.all()
    retorno = {"peliculas": list(peliculas)} 
    return render(request, "listarPeliculas.html", retorno)   



@csrf_exempt
def agregarPelicula(request):
    try:
        codigo = request.POST['txtCodigo']
        titulo = request.POST['txtTitulo']
        protagonista = request.POST['txtProtagonista']
        duracion = int(request.POST['txtDuracion'])
        resumen = request.POST['txtResumen']
        foto = request.FILES['txtFoto']
        idGenero = int(request.POST['cbGenero'])
        genero = Genero.objects.get(pk=idGenero)
        # crear objeto pelicula
        pelicula = Pelicula(pelCodigo=codigo,
                            pelTitulo=titulo,
                            pelProtagonista=protagonista,
                            pelDuracion=duracion,
                            pelResumen=resumen,
                            pelFoto=foto,
                            Genero=genero)

        pelicula.save()
        messages.success(request, "Película agregada correctamente")
    except Error as error:
        messages.error(request, f"Error al agregar la película: {str(error)}")
    return redirect('listarPelicula')
    
@csrf_exempt
def vistaAgregarPelicula(request):
    generos = Genero.objects.all()
    retorno = {"generos": generos}
    return render(request, "agregarPelicula.html", retorno)


@csrf_exempt
def consultarPeliculaPorId(request, id):
    pelicula = Pelicula.objects.get(pk=id)
    generos = Genero.objects.all()
    #retornamos los generos porque se necesitan en la interfaz
    retorno = {"pelicula": pelicula, "generos": generos}
    return render(request, "actualizarPelicula.html", retorno)

@csrf_exempt
def actualizarPelicula(request):
    try:
        idPelicula = request.POST['idPelicula']
        # obtener la pelicula a partir de su id
        peliculaActualizar = Pelicula.objects.get(pk=idPelicula)
        # actualizar los campos
        peliculaActualizar.pelCodigo = request.POST['txtCodigo']
        peliculaActualizar.pelTitulo = request.POST['txtTitulo']
        peliculaActualizar.pelProtagonista = request.POST['txtProtagonista']
        peliculaActualizar.pelDuracion = int(request.POST['txtDuracion'])
        peliculaActualizar.pelResumen = request.POST['txtResumen']
        idGenero = int(request.POST['cbGenero'])
        # obtener el objeto Genero a partir de su id
        genero = Genero.objects.get(pk=idGenero)
        peliculaActualizar.pelGenero = genero
        foto = request.FILES.get('fileFoto')

        # si han enviado foto se actualiza el campo
        if (foto):
            # primero eliminamos la foto existente
            os.remove(os.path.join(settings.MEDIA_ROOT + "/" + 
                      str(peliculaActualizar.pelFoto)))
            # actualizamos con la nueva foto
            peliculaActualizar.pelFoto = foto
        #actualizar la pelicula en la base de datos
        peliculaActualizar.save()
        mensaje = "Pelicula Actualizada"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    return redirect('listarPelicula')
    

@csrf_exempt
def vistaActualizarPelicula(request, id):
    pelicula = Pelicula.objects.get(pk=id)
    generos = Genero.objects.all()
    return render(request, "actualizarPelicula.html", {"pelicula": pelicula, "generos": generos})

@csrf_exempt
def eliminarPelicula(request, id):
    try:
        # buscamos la pelicula por su id
        peliculaAEliminar = Pelicula.objects.get(pk=id)
        # Eliminamos la pelicula
        peliculaAEliminar.delete()
        mensaje = "Pelicula Eliminada Correctamente"
    except Error as error:
        mensaje = str(error)
    retorno = {"mensaje": mensaje}
    return redirect('listarPelicula')
    
@csrf_exempt
def vistaCrud(request):
    return render(request, "peliculas.html")


@csrf_exempt
def inicio(request):
    return render(request, "inicio.html")  
