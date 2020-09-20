from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from datetime import date
from departamentos.models import Transporte,Reserva
from datetime import date,timedelta
class User(AbstractUser):
    telefono = models.IntegerField(null=True,blank=False)
    fecha_nacimiento = models.DateField( null=True,blank=False,auto_now=False, auto_now_add=False)
    N_tarjeta = models.IntegerField(null=True,blank=False)
    imagen = models.ImageField(upload_to='usuarios/%Y/%m',blank=True)
    
    # Metodo para obtener el transporte  actual del usuario
    @property
    def transporte(self):   
        reserva  =self.reserva.filter(usuario=self.id).last()
        transporte = Transporte.objects.get(reserva=reserva.id) 
        return transporte
    # Metood para saber reserva actual del usuario
    @property
    def reserva_actual(self):
        reserva = self.reserva.filter(usuario=self.id).last()
        reserva_obj = Reserva.objects.get(id=reserva.id)
        return reserva_obj

    # Metodo para saber si esta a 48h de su llegada su peticion se cancelaria segun la fecha de solicitud
    # TODO me falta enviar documento con la inforamcion del tranposrte
    @property
    def transporte_fecha(self):
        reserva  =self.reserva.filter(usuario=self.id).last()
        transporte = Transporte.objects.get(reserva=reserva.id) 
        dia_salida =  reserva.dia_llegada + timedelta(days=reserva.dias_estadia)
        return transporte.fecha_solicitud >= ( reserva.dia_llegada - timedelta(days=2))
       

        #Metodo para mostrar imagen en admin
    def mostrar_imagen(self):
        if self.imagen:
            return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.imagen))
        else:
            return mark_safe('<img src="/media/default.jpg" width="50" height="50" />')
    mostrar_imagen.short_description = 'imagen'
    
    def __str__(self):
        return "{} {} ".format(self.first_name,self.last_name)


    class Meta:
        # Nombres del modelo en singular y plural
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
