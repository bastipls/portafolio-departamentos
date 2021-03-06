from django.shortcuts import render,get_object_or_404,redirect
from departamentos.models import Departamento,Imagen,Inventario,Reserva,Arriendo,Tour,Check_out
from usuarios.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.urls import resolve
from datetime import date,datetime,timedelta
from django.utils.dateparse import parse_date


# Librerias para crear pdfs
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
# Librerias para oracle
from django.db import connection

#  Views correspondientes a vistas del cliente
def listar_departamentos(request):
    
    # Se es administrador o funcionario redirecciona al sitio administracion
    if request.user.is_staff:

        return redirect('Administracion departamentos')
    # De lo contrario al sitio normal
    else:
        # Solo los departamentos que no contengan reserva y no esten en mantencion seran mostrados
        departamentos = Departamento.objects.exclude(usuario__isnull=False).filter(estado_mantencion=False)
        context = {'departamentos':departamentos}

        return render(request,'departamentos/lista_departamentos.html',context)

def ver_departamento(request,id):
    # Objecto para guardarloo 
    departamento = get_object_or_404(Departamento,id=id)
    # Query para actuaslizar
    departamento_u = Departamento.objects.filter(id=id)
    imagenes = Imagen.objects.filter(departamento=id)
    
    context = {'departamento':departamento,
                'imagenes':imagenes}
    # Condicion si el usuario esta logeado verifica si contiene una reserva
    if request.user.is_active:
        tiene_reserva = Departamento.objects.filter(usuario=request.user.id).exists()
   
       

    if request.method == 'POST':
        #
        # Objetos arriendo y reserva
        reserva = Reserva()
        arriendo = Arriendo()

        usuario = get_object_or_404(User,id=request.user.id)
        user = User.objects.filter(id=usuario.id)
        reserva.usuario = usuario
        reserva.departamento = departamento
        reserva.dia_llegada = request.POST.get('diallegada')

        fecha_hoy_mas_2 = date.today()+timedelta(days=2)
        print("===============",request.POST.get('diallegada'))
        if datetime.strptime(request.POST.get('diallegada'), "%Y-%m-%d").date()  < fecha_hoy_mas_2:
            messages.error(request,'Reservar al menos dos dias a partir de hoy')
            return render(request,'departamentos/ver_departamento.html',context)
    

        if request.POST.get('acompanantes') == None or request.POST.get('acompanantes') == '':
            reserva.acompanantes = 0
        else:
            reserva.acompanantes = request.POST.get('acompanantes')
        
        reserva.dias_estadia = request.POST.get('diasestadia',True)
        abono = round((departamento.precio *float(request.POST.get('diasestadia'))) * 0.1)
        reserva.abono = abono
        # diferencia = round((departamento.precio *int(request.POST.get('diasestadia')) )- abono)
        # Atrapo errores relacionado al objeto reserva
        try:
            # Condicion si tiene una reserva no deja reservar
            if tiene_reserva:
                messages.error(request,'Lo sentimos usted ya tiene una reseva o un arriendo')
                return render(request,'departamentos/ver_departamento.html',context)
            user.update(reserva_activa=True)
            reserva.save()
            departamento_u.update(usuario=request.user)

            #Return si sale todo bien con reserva
            messages.success(request,'Depto {} reservado!!'.format(departamento.direccion))
            return redirect('Mis reservas')
        except Exception as err:
            print('Error al guardar Reserva ===',err)
            messages.error(request,'Lo sentimos no se realizo la reserva')
            return render(request,'departamentos/ver_departamento.html',context)
    return render(request,'departamentos/ver_departamento.html',context)


# Fin de vistas corrrespondientes a parte del cliente


# Vistas correspondientes parte del admin
# Regla de seguridad: Solo si es  admin puede entrar
@user_passes_test(lambda u:u.is_staff,login_url=('login'))  
def listar_departamentos_admin(request):

    # Variables de para listar en mi template 
    # If para diferenciar lo departamentos disponibles
    if request.resolver_match.url_name == 'Administracion departamentos':
        # Solo los departamentos que no contengan usuario con reserva activa y no esten en mantencion seran mostrados
        departamentos = Departamento.objects.exclude(usuario__isnull=False).filter(estado_mantencion=False)
    elif request.resolver_match.url_name == 'Administracion departamentos en mantención':
        departamentos = Departamento.objects.exclude(usuario__isnull=False).filter(estado_mantencion=True)
    elif request.resolver_match.url_name == 'Administracion departamentos reservados':
        departamentos = Departamento.objects.exclude(reserva__isnull=True).exclude(usuario__isnull=True).filter(estado_mantencion=False).filter(usuario__reserva_activa=True)
    elif request.resolver_match.url_name == 'Administracion departamentos arrendados':
        departamentos = Departamento.objects.filter(reserva__arriendo__isnull=True).filter(estado_mantencion=False).filter(usuario__arriendo_activo=True)
     
    inventarios = Inventario.objects.all()
    imagenes = Imagen.objects.all()
    tours = Tour.objects.all()
    context = {'departamentos':departamentos,
               'imagenes':imagenes,
               'inventarios':inventarios,
               'tours':tours}
               
    # Metodo post para agregar imagenes
    if request.method == 'POST' and 'btn-imagenes' in request.POST:
        imagen = Imagen()
        
        departamento = get_object_or_404(Departamento,id=request.POST.get('idDep'))

        imagen.departamento = departamento
        
        imagen.imagen = request.FILES.get('imagenDep')
        
        if request.FILES.get('imagenDep') == None:
            messages.error(request,'Verifique los campos porfavor')
           
            return redirect(request.resolver_match.url_name)
       

        try:
            imagen.save()
            messages.success(request,'Imagen añadida con exito')
            return redirect(request.resolver_match.url_name)
        except Exception as err:
            print(err)
            messages.error(request,'Lo sentimos hubo un error')
            return redirect(request.resolver_match.url_name)

    # Metodo post para agregar inventario
    if request.method == 'POST' and 'btn-inventario' in request.POST:
        inventario = Inventario()
        departamento = get_object_or_404(Departamento,id=request.POST.get('idInv'))
        inventario.departamento = departamento
        inventario.nombre = request.POST.get('nombreInv')
        inventario.precio = request.POST.get('precioInv')

        try:
            inventario.save()
            messages.success(request,'Inventario {} añadido con exito'.format(request.POST.get('nombreInv')))
            return redirect(request.resolver_match.url_name)

        except Exception as err:
            print(err)
            messages.error(request,'Verifique los campos porfavor')
            return redirect(request.resolver_match.url_name)
    #Metood post para agregar tours
    if request.method == 'POST' and 'btn-tour' in request.POST:
        tour = Tour()
        departamento = get_object_or_404(Departamento,id=request.POST.get('idTour'))
        tour.departamento = departamento
        tour.nombre = request.POST.get('nombretour')
        tour.dia = request.POST.get('dia')
        tour.direccion = request.POST.get('direcciontour')
        tour.duracion = request.POST. get('duraciontour')
        tour.precio = request.POST.get('preciotour')
        tour.descripcion = request.POST.get('descripciontour')
        try:
            tour.save()
            messages.success(request,'Tour {}'.format(request.POST.get('nombretour')))
            return redirect(request.resolver_match.url_name)
        except Exception as err:
            print('VAGREGARTOUR ===',err)
            messages.error(request,'Verifique los campos porfavor')
            return redirect(request.resolver_match.url_name)

    #Metodo POST para asginar dia de mantencion
    if request.method == 'POST' and 'btn-mantencion' in request.POST:
        # Condicion de fecha
        if parse_date(request.POST.get('fechamantencion')) < date.today():
            messages.error(request,'La fecha a asignar debe ser a partir de hoy')
            return redirect('Administracion departamentos')
        departamento = Departamento.objects.filter(id=request.POST.get('idDepMantencion'))
        try:
            
            departamento.update(mantencion=request.POST.get('fechamantencion'))
            messages.success(request,'Mantención programada')
            return redirect('Administracion departamentos')
        except Exception as err:
            print(err)
            messages.error(request,'No se pudo programar la mantencion')
            return redirect('Administracion departamentos')
    return render(request,'departamentos/lista_departamentos_admin.html',context)
# Regla de seguridad: Solo si esadmin puede eliminar
@user_passes_test(lambda u:u.is_superuser,login_url=('login')) 
def eliminar_departamento(request,id):
    
    departamento = Departamento.objects.exclude(reserva__isnull=False).filter(id=id,estado_mantencion=False)
    try:
        messages.success(request,'Departamento eliminado')
        departamento.delete()
        return redirect('Administracion departamentos')
    except Exception as err:
        print('Error VELIMINARDEPTO ==',err)
        messages.error(request,'No se pudo eliminar el departamento')
        return redirect('Administracion departamentos')

def actualizar_estado_mantencion(request,id):
    
    departamento = Departamento.objects.filter(id=id)
    # Esto lo hago para obtener los fields del model 
    check_estado =  Departamento.objects.get(id=id)
    # Para saber el nombre url_name de la url anterior
    if request.META.get('HTTP_REFERER') is not None:
        referer = request.META.get('HTTP_REFERER').split("/",3)[3]
        match = resolve('/'+referer)
    else:
        match="/"
    # If para saber si la mantencion no esta progarmada solo en url_name deptos disponibles
    if check_estado.mantencion is None and match.url_name == 'Administracion departamentos':
        messages.error(request,'Mantencion de Depto {} no programada para hoy'.format(check_estado.id))
        print('ERRROOR')
        return redirect(request.META.get('HTTP_REFERER'))


    if check_estado.estado_mantencion == True:
        try:
            if match.url_name == 'Administracion departamentos en mantención':
                departamento.update(estado_mantencion=False)
                departamento.update(mantencion=None)
            else:
                
                departamento.update(estado_mantencion=False)
            messages.success(request,'Estado de  {} actualizado'.format(check_estado.direccion))
            
            return redirect(request.META.get('HTTP_REFERER'))
            
        except Exception as err:

            messages.error(request,'No se pudo actualizar el estado')
            return redirect(request.META.get('HTTP_REFERER'))
            
    else:
        try:
          
            if match.url_name == 'Administracion departamentos en mantención':
                departamento.update(estado_mantencion=True)
                departamento.update(mantencion=None)
            else:
                departamento.update(estado_mantencion=True)
            messages.success(request,'Estado de  {} actualizado'.format(check_estado.direccion))
            return redirect(request.META.get('HTTP_REFERER'))

        except Exception as err:

            print(err)
            messages.error(request,'No se pudo actualizar el estado')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('Administracion departamentos') 
# Regla de seguirdad: Solo si es admin puede eliminar tours
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
def eliminar_tour_departamento(request,id):
    tour = Tour.objects.filter(id=id)
    try:
        messages.success(request,'Tour eliminado')
        tour.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as err:
        print('ERRVELIMINARTOUR ====',)
        messages.error(request,'No se pudo eliminar el tour')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

# Regla de seguridad: Solo si esadmin puede eliminar departamento
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
def eliminar_inventario_departamento(request,id):
    inventario = Inventario.objects.filter(id=id)

    try:
        messages.success(request,'Inventario eliminado ')
        inventario.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as err:
        print('ERRVELIMINARINVENTARIO ==== ',err)
        messages.error(request,'No se pudo eliminar el inventario')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))

# Regla de seguridad: Solo si es admin puede eliminar
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
def eliminar_imagen_departamento(request,id):
    imagen = Imagen.objects.filter(id=id)
    try:
        imagen.delete()
        # messages.success(request,'Imagen {} eliminada'.format(imagen.imagen.url))
        messages.success(request,'Imagen eliminada')
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as err:
        print(err)
        # messages.error(request,'No se pudo eliminar la imagen {} '.format(imagen.imagen.url))
        messages.error(request,'No se pudo eliminar la imagen ')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))


# Regla de seguridad: Solo si es admin puede actualizar estado
@user_passes_test(lambda u:u.is_staff,login_url=('login'))  
def actualizar_estado_inventario(request,id):  
    
    inventario = Inventario.objects.filter(id=id)
    # Esto lo hago para obtener los fields del model 
    check_estado =  Inventario.objects.get(id=id)

    if check_estado.estado == 'Buen estado':
        try:

            inventario.update(estado='Mal estado')
            messages.success(request,'Estado de  {} actualizado'.format(check_estado.nombre))
            return redirect(request.META.get('HTTP_REFERER'))
            
        except Exception as err:

            messages.error(request,'No se pudo actualizar el estado')
            return redirect(request.META.get('HTTP_REFERER'))
            
    else:
        try:

            inventario.update(estado='Buen estado')
            messages.success(request,'Estado de  {} actualizado'.format(check_estado.nombre))
            return redirect(request.META.get('HTTP_REFERER'))

        except Exception as err:

            print(err)
            messages.error(request,'No se pudo actualizar el estado')
            return redirect(request.META.get('HTTP_REFERER'))

    return redirect('Administracion departamentos')

def reportes_departamentos(request):
    
    if request.resolver_match.url_name == 'Reportes departamento reservas':
        departamentos = Departamento.objects.exclude(reserva__isnull=True)
    elif request.resolver_match.url_name == 'Reportes departamento arriendos':

        departamentos = Departamento.objects.exclude(reserva__arriendo__check_out=False).exclude(reserva__isnull=True)
    context = {'departamentos':departamentos}
    return render(request,'departamentos/lista_reportes.html',context)



def plsql_listar_reservas_informe_reserva_filtro(id):
     # PARTE PL/SQL
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('PL_LISTAR_RESERVAS_FILTRO',[id,out_cursor])
    nombre_columnas =  [x[0] for x in out_cursor.description]

    lista = []
    for fila in out_cursor:
        # Le agrego su respectiva columna y lo transformo a un diccionario
        lista.append(dict(zip(nombre_columnas,fila)))
    return lista



def generar_informe_reserva(request,id):
    try:
       
        fecha_hoy = datetime.now()
        departamento = Departamento.objects.get(id=id)

        usuarios = User.objects.all()
    
        total = 0
        for reserva in plsql_listar_reservas_informe_reserva_filtro(id):
            total += reserva['ABONO']
    
        context = { 'usuarios':usuarios,
                    'fecha_hoy':fecha_hoy,
                    'departamento':departamento,
                    'total':total,
                    'reservas':plsql_listar_reservas_informe_reserva_filtro(id)}
        template = get_template('departamentos/informe_reserva.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_reservas_dpto_{}.pdf"'.format(departamento.id)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
     
    except Exception as err:
        print('VERRORINFORMEGENERAR === ',err)
        messages.error(request,'No se pudo generar el informe')
        return redirect(request.META.get('HTTP_REFERER'))
    return response

def plsql_listar_checkouts_informe_arriendo(id):
     # PARTE PL/SQL
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('PL_LISTAR_CHECKOUTS',[out_cursor])
    nombre_columnas =  [x[0] for x in out_cursor.description]

    lista = []
    for fila in out_cursor:
        # Le agrego su respectiva columna y lo transformo a un diccionario
        lista.append(dict(zip(nombre_columnas,fila)))
    # Filtro la lista para q muestre solo las del depto
    lista_filtrada = []

    reservas = Reserva.objects.filter(departamento=id)
    lsita_reservas = [l['id'] for l in reservas.values('id')]
    lista_arriendos = Arriendo.objects.filter(reserva__in=lsita_reservas)
    lista_v_arriendos = [l['id'] for l in lista_arriendos.values('id')]

    for checkout in lista:
        if checkout['ARRIENDO_ID'] in lista_v_arriendos:
            lista_filtrada.append(checkout)
    return lista_filtrada


def generar_informe_arriendo(request,id):
    try:
        fecha_hoy = datetime.now()

        reservas = Reserva.objects.filter(departamento=id)
        arriendos = Arriendo.objects.all()
        lsita_reservas = [l['id'] for l in reservas.values('id')]
        lista_arriendos = Arriendo.objects.filter(reserva__in=lsita_reservas)
        lista_v_arriendos = [l['id'] for l in lista_arriendos.values('id')]
        departamento = Departamento.objects.get(id=id)
        check_outs=plsql_listar_checkouts_informe_arriendo(id)

        total = 0
        for checkout in plsql_listar_checkouts_informe_arriendo(id):
            total += checkout['TOTAL']
        context = {'check_outs':check_outs,
                    'arriendos':arriendos,
                    'fecha_hoy':fecha_hoy,
                    'departamento':departamento,
                    'total':total}
        template = get_template('departamentos/informe_arriendo.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Reporte_arriendos_dpto_{}.pdf"'.format(departamento.id)
        pisa_status = pisa.CreatePDF(
        html, dest=response)
     
    except Exception as err:
        print('VERRORINFORMEGENERAR === ',err)
        messages.error(request,'No se pudo generar el informe')
        return redirect(request.META.get('HTTP_REFERER'))
    return response

from django.db.models import Sum
def estadisticas(request):
    # Grafico de barras horizontal Cantidad de reservas por departamento
    departamentos = Departamento.objects.exclude(reserva__isnull=True)
    reservas = Reserva.objects.all()
    departamentos_reservados_label = departamentos.values_list('direccion',flat=True)
    departamentos_reservados_label = [ ]
    departamentos_reservados_cantidad_reservas = []
    # Esto para los totales del graficos ganancias
    departamentos_reservas_total_abono = []

    for deptos in departamentos:
        departamentos_reservados_cantidad_reservas.append(deptos.reserva.count())
        departamentos_reservados_label.append(deptos.direccion)
        total_reservas = 0
        departamentos_reservas_total_abono.append(deptos.reservas_total_abono)

      #FIN ========= Grafico de barras horizontal Cantidad de reservas por departamento
    #Grafico radar
    zonas_departamento = ['Norte','Sur','Este','Oeste']
    departamentos_zona_norte = Departamento.objects.filter(zona='Norte').count()
    departamentos_zona_sur = Departamento.objects.filter(zona='Sur').count()
    departamentos_zona_este = Departamento.objects.filter(zona='Este').count()
    departamentos_zona_oeste = Departamento.objects.filter(zona='Oeste').count()
    zonas_deptos = {'departamentos_zona_norte':departamentos_zona_norte,
                    'departamentos_zona_sur':departamentos_zona_sur,
                    'departamentos_zona_este':departamentos_zona_este,
                    'departamentos_zona_oeste':departamentos_zona_oeste}
    maximo_key = max(zonas_deptos.keys(), key=(lambda k: zonas_deptos[k]))
    minimo_key = min(zonas_deptos.keys(), key=(lambda k: zonas_deptos[k]))
    maximo_zona = zonas_deptos[maximo_key]
    minimo_zona = zonas_deptos[minimo_key]
    max_min = {'maximo_zona':maximo_zona,
                'minimo_zona':minimo_zona}
    # Fin graficos radar
    # Grafico ganancias por zona
    departamentos_ganancias_zona_norte = sum(Check_out.objects.filter(arriendo__reserva__departamento__zona ='Norte').values_list('total',flat=True))
    departamentos_ganancias_zona_sur = sum(Check_out.objects.filter(arriendo__reserva__departamento__zona ='Sur').values_list('total',flat=True))
    departamentos_ganancias_zona_este = sum(Check_out.objects.filter(arriendo__reserva__departamento__zona ='Este').values_list('total',flat=True))
    departamentos_ganancias_zona_oeste = sum(Check_out.objects.filter(arriendo__reserva__departamento__zona ='Oeste').values_list('total',flat=True))

    zonas_ganancias_deptos = {'departamentos_ganancias_zona_norte':departamentos_ganancias_zona_norte,
                    'departamentos_ganancias_zona_sur':departamentos_ganancias_zona_sur,
                    'departamentos_ganancias_zona_este':departamentos_ganancias_zona_este,
                    'departamentos_ganancias_zona_oeste':departamentos_ganancias_zona_oeste}
    #Fina ganancias por zona

    context = {'departamentos_reservados_label':departamentos_reservados_label,
                'departamentos_reservados_cantidad_reservas':departamentos_reservados_cantidad_reservas,
                'departamentos_reservas_total_abono':departamentos_reservas_total_abono,

                'zonas_departamento':zonas_departamento,
                'zonas_deptos':zonas_deptos,
                'max_min':max_min,
                
                'zonas_ganancias_deptos':zonas_ganancias_deptos,
                }
    return render(request,'departamentos/estadisticas.html',context) 
