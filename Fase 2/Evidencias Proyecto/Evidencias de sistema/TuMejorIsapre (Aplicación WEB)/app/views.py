
import re
#Render: Sirve para renderizar una plantilla HTML con el contexto proporcionado.
#Redirect: Redirige al usuario a otra URL, necesaria para las navegaciones despues de ciertas acciones (como el envio de un formulario)
#get_object_or_404: Se recupera un objeto desde la base de datos según lo que se pida. Si no se encuentra, en lugar de fallar sin dar aviso, se da un error 404.
from django.shortcuts import render, redirect, get_object_or_404
#Responde a una solicitud HTTP devolviendo datos en formato JSON, adecuado para APIs o cuando se necesita una respuesta en formato JSON para solicitudes AJAX.
from django.http import JsonResponse
from .models import FormularioDatos, Carga, Region, Comunas, Asesor
from .forms import AsesorForm, RegistroUsuarioForm  
#login_required: Decorador que se usa para proteger ciertas vistas permitiendo el acceso solo a usuarios autenticados.
from django.contrib.auth.decorators import login_required
#Login: Función que inicia sesión para el usuario.
from django.contrib.auth import login
#User: Modelo incorporado de Django para manejar datos de usuarios, como nombre de usuario, correo electrónico, contraseña, y otros datos de autenticación.
from django.contrib.auth.models import User
#Paginator: Clase de Django para dividir un conjunto de datos grande en páginas. Permite crear una navegación paginada, útil cuando se necesita mostrar muchos registros en una vista sin sobrecargar la página.
from django.core.paginator import Paginator
#require_http_methods: Decorador que restringe los métodos HTTP permitidos para una vista. Por ejemplo, se puede restringir a métodos POST o DELETE para controlar el acceso y evitar que la vista se ejecute con otros métodos no autorizados.
from django.views.decorators.http import require_http_methods



def index(request):

    #Verifica si la solicitud es un POST y que provenga de una solicitud AJAX (mediante la cabecera x-requested-with), asegurando que esta parte del código solo se ejecute en esos casos.
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':

        #Captura datos específicos enviados desde el formulario, extrayendo valores con request.POST.get(). Esto toma los datos proporcionados por el usuario y los asigna a variables.
        nombre_apellido = request.POST.get('nombre_apellido')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', nombre_apellido):
            return JsonResponse({'success': False, 'message': 'El nombre solo puede contener letras y espacios.'})
        rut = request.POST.get('rut')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        renta_imponible = request.POST.get('renta_imponible')
        num_cargas = request.POST.get('num_cargas')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        region_id = request.POST.get('region')
        comuna_id = request.POST.get('comuna')
        prevision_actual = request.POST.get('prevision_actual')
        cambio_preferente = request.POST.get('cambio_preferente')
        valor_uf = request.POST.get('valor_uf')
        resultado_final = int(float(request.POST.get('resultado_final', 0)))
        monto_dispuesto = int(float(request.POST.get('monto_dispuesto', 0)))

        #Recupera las instancias correspondientes de Region y Comunas usando las IDs enviadas desde el formulario. Esto asegura que los datos guardados en la base de datos tengan referencias correctas a las tablas relacionadas.
        region_instance = Region.objects.get(pk=region_id)  
        comuna_instance = Comunas.objects.get(pk=comuna_id)

        #Guardar datos dentro de la BBDD
        formulario = FormularioDatos(
            nombre_apellido=nombre_apellido,
            rut=rut,
            fecha_nacimiento=fecha_nacimiento,
            renta_imponible=renta_imponible,
            num_cargas=num_cargas,
            telefono=telefono,
            correo=correo,
            region=region_instance,       
            comuna=comuna_instance,
            prevision_actual=prevision_actual,
            cambio_preferente=cambio_preferente,
            valor_uf=valor_uf,
            resultado_final=resultado_final,
            monto_dispuesto=monto_dispuesto
        )
        formulario.save()

        #Itera tantas veces como el número de cargas (num_cargas), recuperando cada fecha de nacimiento usando el índice i.
        num_cargas = int(request.POST.get('num_cargas', 0))  
        for i in range(1, num_cargas + 1):

            #Si se proporciona la fecha de nacimiento (fecha_nacimiento_carga), se crea una entrada en la tabla Carga, vinculando la carga con la instancia formulario.
            fecha_nacimiento_carga = request.POST.get(f'fecha_nacimiento_carga_{i}')
            if fecha_nacimiento_carga:
                Carga.objects.create(
                    fecha_nacimiento=fecha_nacimiento_carga,
                    formulario=formulario
                )

    
        return JsonResponse({'success': True, 'message': 'Se han enviado sus datos correctamente.'})

    return render(request, 'app/index.html')


def informacion(request):
    return render(request, 'app/informacion.html')

def servicios(request):
    return render(request, 'app/servicios.html' )

#Creación de API con las regiones y comunas correspondientes.
def obtener_regiones_comunas(request):
    regiones = Region.objects.all()
    data = {
        "regiones": [
            {
                "id": region.reg_id,
                "nombre": region.reg_nombre,
                "comunas": list(region.comunas.values("com_id", "com_nombre"))
            } for region in regiones
        ]
    }
    return JsonResponse(data)


#@login_required para entrar a esta vista logeado.
#
@login_required
def lista_asesores(request):

    #Consulta a la base de datos para obtener todas las instancias de Asesor. Esto permite cargar la lista completa de asesores para mostrarlos en la plantilla lista_asesores.html.
    asesores = Asesor.objects.all()
    #Verifica si la solicitud es de tipo POST, indicando que el usuario está enviando datos desde el formulario para agregar un nuevo asesor.
    if request.method == 'POST':
        #Crea una instancia del formulario AsesorForm usando los datos de request.POST, que contiene toda la información enviada por el usuario en el formulario.
        form = AsesorForm(request.POST)
        #Valida el formulario usando form.is_valid(), que verifica que todos los campos requeridos están completos y que la información sigue las reglas establecidas (como el formato del número de teléfono).
        if form.is_valid():
            form.save()
            return redirect('lista_asesores')
        #Si la solicitud no es de tipo POST (es decir, es GET), significa que el usuario simplemente quiere ver la lista de asesores y el formulario vacío para agregar un nuevo asesor.
    else:
        #En este caso, se crea una instancia vacía de AsesorForm, que se pasará al template.
        form = AsesorForm()

    return render(request, 'app/lista_asesores.html', {'asesores': asesores, 'form': form})


#Login_required: con esta etiqueta se evita que se ingrese a la vista.
@login_required
def mostrar_datos_formularios(request):
    #datos obtiene todas las instancias de FormularioDatos usando prefetch_related('cargas'), lo cual optimiza la consulta al cargar en memoria las cargas (es decir, dependientes) asociadas con cada formulario, reduciendo el número de consultas a la base de datos.
    datos = FormularioDatos.objects.prefetch_related('cargas').all()
    #asesores obtiene todas las instancias de Asesor, necesarias para asignar un asesor a un formulario desde el formulario de selección.
    asesores = Asesor.objects.all()
    paginator = Paginator(datos, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    datos = paginator.get_page(page_number)

    if request.method == 'POST':
        formulario_id = request.POST.get('formulario_id')
        asesor_id = request.POST.get('asesor_id')
        #Recupera el formulario correspondiente a formulario_id y el asesor correspondiente a asesor_id usando get() para obtener instancias únicas de cada objeto.
        formulario = FormularioDatos.objects.get(id=formulario_id)
        asesor = Asesor.objects.get(id=asesor_id)
        #Se asigna el asesor al formulario, almacenándolo en el campo asesor del formulario, y guarda los cambios en la base de datos usando formulario.save().
        formulario.asesor = asesor
        formulario.save()
        return redirect('mostrar_datos_formularios')

    return render(request, 'app/tabla_datos.html', {'datos': datos, 'asesores': asesores})

@login_required
def asignar_asesor(request):
    if request.method == 'POST':
        formulario_id = request.POST.get('formulario_id')
        asesor_id = request.POST.get('asesor_id')
        formulario = FormularioDatos.objects.get(id=formulario_id)
        asesor = Asesor.objects.get(id=asesor_id)
        formulario.asesor = asesor
        formulario.save()
        return redirect('mostrar_datos_formularios')  


@login_required
#Se obtiene el id del asesor con asesor_id para asegurarse del asesor del que se quiere editar.
def editar_asesor(request, asesor_id):
    #Usa get_object_or_404 para intentar obtener la instancia de Asesor con el asesor_id proporcionado. Si el asesor no existe, get_object_or_404 devuelve una página de error 404, evitando que la aplicación falle con un error de búsqueda.
    asesor = get_object_or_404(Asesor, id=asesor_id)
    #Verifica si la solicitud es de tipo POST (es decir, si se han enviado datos desde el formulario de edición).
    if request.method == 'POST':
        form = AsesorForm(request.POST, instance=asesor)
        if form.is_valid():
            form.save()
            return redirect('lista_asesores')
    else:
        form = AsesorForm(instance=asesor)
    return render(request, 'app/editar_asesor.html', {'form': form, 'asesor': asesor})

@require_http_methods(["DELETE"])
def eliminar_asesor(request, asesor_id):
    try:
        asesor = Asesor.objects.get(id=asesor_id)
        asesor.delete()
        return JsonResponse({"success": True})
    except Asesor.DoesNotExist:
        return JsonResponse({"success": False}, status=404)


@require_http_methods(["DELETE"])
def eliminar_formulario(request, formulario_id):
    try:
        formulario = FormularioDatos.objects.get(id=formulario_id)
        formulario.delete()
        return JsonResponse({"success": True})
    except FormularioDatos.DoesNotExist:
        return JsonResponse({"sucess: false"}, status=404)



def generar_nombre_usuario(nombre, apellido):
    #Para crear el usuario se combina el nombre del usuario utilizando el nombre y apellido del usuario.
    base_username = f"{nombre}{apellido}".lower()
    #En primer lugar se le asigna el nombre de usuario sin ningún numero.
    username = base_username
    contador = 1
    #Y luego se utiliza un while para verificar si existe el usuario para asignarle un numero para identificarlo.
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{contador}"
        contador += 1

    return username


#@login_required
def registro(request):
    if request.method == 'POST':
        #Crea una instancia de RegistroUsuarioForm creada en forms.py con los datos enviados.
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre'].capitalize()
            apellido = form.cleaned_data['apellido'].capitalize()
            username = generar_nombre_usuario(nombre, apellido)

            # Crear el usuario con el nombre de usuario único
            user = User.objects.create_user(
                username=username,
                first_name=nombre,
                last_name=apellido,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)  
            return redirect('mostrar_datos_formularios')  
    else:
        form = RegistroUsuarioForm()
    return render(request, 'app/registro.html', {'form': form})