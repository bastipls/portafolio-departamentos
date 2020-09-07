from django.shortcuts import render,get_object_or_404,redirect
from departamentos.models import Departamento,Imagen,Inventario,Reserva,Arriendo
from usuarios.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages


#  Views correspondientes a vistas del cliente
def listar_departamentos(request):
    # Se es administrador o funcionario redirecciona al sitio administracion
    if request.user.is_staff:

        return redirect('Administracion departamentos')
    # De lo contrario al sitio normal
    else:
        # Solo los departamentos que no contengan reserva y no esten en mantencion seran mostrados
        departamentos = Departamento.objects.exclude(reserva__isnull=False).filter(estado_mantencion=False)
        context = {'departamentos':departamentos}

        return render(request,'lista_departamentos.html',context)

def ver_departamento(request,id):

    departamento = get_object_or_404(Departamento,id=id)
   
    imagenes = Imagen.objects.filter(departamento=id)
    context = {'departamento':departamento,
                'imagenes':imagenes}
    # Condicion si el usuario esta logeado verifica si contiene una reserva
    if request.user.is_active:
        tiene_reserva = Reserva.objects.filter(usuario=request.user.id).exists()
       

    if request.method == 'POST':
        # Objetos arriendo y reserva
        reserva = Reserva()
        arriendo = Arriendo()

        usuario = get_object_or_404(User,id=request.user.id)
        reserva.usuario = usuario
        reserva.departamento = departamento
        reserva.dia_llegada = request.POST.get('diallegada')
        if request.POST.get('acompanantes') is None:
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
                messages.error(request,'Lo sentimos usted ya tiene una reseva')
                return render(request,'ver_departamento.html',context)

            reserva.save()
         

            #Return si sale todo bien con reserva
            messages.success(request,'Depto {} reservado!!'.format(departamento.direccion))
            return render(request,'ver_departamento.html',context)
        except Exception as err:
            print('Error al guardar Reserva ===',err)
            messages.error(request,'Lo sentimos no se realizo la reserva')
            return render(request,'ver_departamento.html',context)
    return render(request,'ver_departamento.html',context)


# Fin de vistas corrrespondientes a parte del cliente


# Vistas correspondientes parte del admin
# Regla de seguridad: Solo si es  admin puede entrar
@user_passes_test(lambda u:u.is_staff,login_url=('login'))  
def listar_departamentos_admin(request):

    # Variables de para listar en mi template 
    # If para diferenciar lo departamentos disponibles
    if request.resolver_match.url_name == 'Administracion departamentos':
        # Solo los departamentos que no contengan reserva y no esten en mantencion seran mostrados
        departamentos = Departamento.objects.exclude(reserva__isnull=False).filter(estado_mantencion=False)
    elif request.resolver_match.url_name == 'Administracion departamentos en mantención':
        departamentos = Departamento.objects.exclude(reserva__isnull=False).filter(estado_mantencion=True)
    inventarios = Inventario.objects.all()
    imagenes = Imagen.objects.all()

    context = {'departamentos':departamentos,
               'imagenes':imagenes,
               'inventarios':inventarios}
               
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


    return render(request,'lista_departamentos_admin.html',context)
# Regla de seguridad: Solo si esadmin puede eliminar
@user_passes_test(lambda u:u.is_superuser,login_url=('login')) 
def eliminar_departamento(request,id):
    
    departamento = Departamento.objects.exclude(reserva__isnull=False).filter(estado_mantencion=False)
    try:
        messages.success(request,'Departamento eliminado')
        departamento.delete()
        return redirect('Administracion departamentos')
    except Exception as err:
        print('Error VELIMINARDEPTO ==',err)
        messages.error(request,'No se pudo eliminar el departamento')
        return redirect('Administracion departamentos')

# Regla de seguridad: Solo si esadmin puede eliminar
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
def eliminar_inventario_departamento(request,id):
    inventario = Inventario.objects.filter(id=id)
    print(request.META.get('HTTP_REFERER'))

    try:
        messages.success(request,'Inventario eliminado ')
        inventario.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    except Exception as err:
        print(err)
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
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
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
    # Regla de seguridad: Solo si es admin puede ver usuarios
@user_passes_test(lambda u:u.is_staff,login_url=('login'))  
def listar_usuarios(request):
    usuarios = User.objects.all()
    context = {'usuarios':usuarios}
    return render(request,'listar_usuarios_admin.html',context)
    # Regla de seguridad: Solo si es admin puede actualizar usuarios
@user_passes_test(lambda u:u.is_superuser,login_url=('login'))  
def actualizar_estado_usuario(request,id):
    usuario = User.objects.filter(id=id)
    # Esto lo hago para obtener los fields del model 
    check_estado =  User.objects.get(id=id)
    if check_estado.is_active:
 
        try:

            usuario.update(is_active=False)
            messages.success(request,'Estado de {} {} actualizado'.format(check_estado.first_name,check_estado.last_name))
            return redirect('Administracion usuarios')
            
        except Exception as err:

            messages.error(request,'No se pudo actualizar el estado')
            return redirect('Administracion usuarios')
            
    else:
        try:

            usuario.update(is_active=True)
            messages.success(request,'Estado de {} {} actualizado'.format(check_estado.first_name,check_estado.last_name))
            return redirect('Administracion usuarios')

        except Exception as err:

            print(err)
            messages.error(request,'No se pudo actualizar el estado')
            return redirect('Administracion usuarios')

    return redirect('Administracion usuarios')
# Fin de vistas correspondientes a parte del admin