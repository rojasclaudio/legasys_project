from datetime import date

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models import (
    IntegerField, CharField, DateField, CASCADE, OneToOneField, BooleanField, ForeignKey, FileField
)


# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


#
# BASE USER
#
class BaseUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True, default=None)
    first_name = models.CharField(max_length=30, verbose_name="nombre")
    last_name = models.CharField(max_length=50, blank=True, verbose_name="apellido")
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = 'Cambio Contraseña'
        verbose_name_plural = 'Cambio Contraseña'
    
    def _str_(self):
        return self.username

    


class Persona(BaseUser):
    per_cedula = IntegerField(verbose_name='Cédula', null=False)
    per_fecha_nacimiento = DateField(verbose_name='Fecha de nac.', null=False)
    per_telefono = IntegerField(verbose_name='Teléfono')
    per_fecha_registro = DateField(default=date.today, verbose_name='Fecha de registro')
    per_direccion = CharField(max_length=100, verbose_name='Dirección')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Facultad (models.Model):
    fac_descripcion = CharField(max_length=100, verbose_name=('Nombre de la Facultad'))
    fac_fecha_registro = DateField(default=date.today)

    def __str__(self):
        return f"{self.fac_descripcion}"

class Carrera (models.Model):
    facultad = ForeignKey(Facultad, on_delete=CASCADE, verbose_name='Facultad')
    crr_descripcion = CharField(max_length=100, verbose_name=('Carrera'))
    crr_fecha_registro = DateField(default=date.today)

    def __str__(self):
        return f"{self.crr_descripcion}"

class SedeFilial (models.Model):
    sed_descripcion = CharField(max_length=100, verbose_name='Nombre de Sede Filial')
    sed_fecha_registro = DateField(default=date.today)

    def __str__(self):
        return f"{self.sed_descripcion}"

#No puse las columnas nativas dentro de este modelo porque es una tabla detalle que sirve para hacer mucho a mucho
class DetalleSedeFilial(models.Model):
    carrera = ForeignKey(Carrera, on_delete=CASCADE, verbose_name='Carrera')
    sedefilial = ForeignKey(SedeFilial, on_delete=CASCADE, verbose_name='Sede Filial')

    def __str__(self):
        return f"{self.sedefilial}"

class Alumno(models.Model):
    persona = OneToOneField(Persona, on_delete=CASCADE, verbose_name='Alumno/a')
    detallesedefilial = ForeignKey(DetalleSedeFilial, on_delete=CASCADE, verbose_name='Sede Filial')
    alu_fecha_registro = DateField(default=date.today, verbose_name='Fecha de Registro')

    def __str__(self):
        return f"{self.persona}"

class Cargo(models.Model):
    car_descripcion = CharField(max_length=100, verbose_name='Nombre del Cargo')
    car_fecha_registro = DateField(default=date.today)

    def __str__(self):
        return f"{self.car_descripcion}"

class Funcionario(models.Model):
    persona = OneToOneField(Persona, on_delete=CASCADE, verbose_name='Funcionario')
    cargo = ForeignKey(Cargo, on_delete=CASCADE, verbose_name='Cargo del Funcionario')
    fun_firmante = BooleanField(default=False, verbose_name='Es firmante?', null=False)
    fun_fecha_registro = DateField(default=date.today)

    def __str__(self):
        return f"{self.persona}"


class LegajoAlumno(models.Model):
    DOC_CHOICES = (('Copia', 'Copia'),
                   ('Copia Autenticada', 'Copia Autenticada'),
                   ('Original', 'Original')
                   )
    alumno = OneToOneField(Alumno, on_delete=CASCADE, verbose_name='Alumno')
    leg_tipo = CharField(choices=DOC_CHOICES, verbose_name='Tipo de Documento', max_length=100)
    leg_ruta = CharField(max_length=500)
    leg_vencimiento = DateField(verbose_name='Vencimiento')
    leg_fecha_registro = DateField(verbose_name='Fecha de registro', null=False)

class TipoDocumento(models.Model):
    legajo_alumno = ForeignKey(LegajoAlumno, on_delete=CASCADE)
    doc_descripcion = CharField(max_length=100, verbose_name='Documento', null=False)
    doc_vencimiento = BooleanField(default=False, verbose_name='Vencimiento', null=False)
    doc_fecha_registro = DateField(default=date.today)
    doc_imagen = FileField(verbose_name='Imagen', null=True)

    def __str__(self):
        return f"{self.doc_descripcion}"

class Profesor(models.Model):
    persona = OneToOneField(Persona, on_delete=CASCADE, verbose_name='Profesor')
    pro_fecha_registro =DateField(default=date.today, verbose_name='Fecha de Registro',null=False)

    def __str__(self):
        return f"{self.persona}"

class Resolucion(models.Model):
    res_descripcion = CharField(max_length=100, verbose_name='Resolucion', null=False)
    res_numero_resolucionm = CharField(max_length=100, verbose_name='Numero de Resolucion', null=False)
    res_fecha_resolucion = DateField(verbose_name='Fecha de Resolucion', null=False)
    res_fecha_registro = DateField(default=date.today, verbose_name='Fecha de Registro', null=False)

    def __str__(self):
        return f"{self.res_descripcion} {self.res_numero_resolucionm} {self.res_fecha_resolucion}"

class Plan(models.Model):
    pln_descripcion = CharField(max_length=100, verbose_name='Nombre del Plan' , null=False)
    pln_fecha_registro = DateField(default=date.today, verbose_name='Fecha de Registro', null=False)

    def __str__(self):
        return f"{self.pln_descripcion}"

class Asignatura(models.Model):
    plan = ForeignKey(Plan, on_delete=CASCADE, verbose_name='Plan')
    asi_descripcion = CharField(max_length=100, verbose_name='Nombre de la Asignatura', null=False)
    asi_fecha_registro = DateField(default=date.today, verbose_name='Fecha de Registro', null=False)

    def __str__(self):
        return f"{self.asi_descripcion}"

class PeriodoLectivo(models.Model):
    per_descripcion = CharField(max_length=100, verbose_name='Nombre del Periodo Lectivo', null=False)
    per_fecha_registro = DateField(default=date.today, verbose_name='Fecha de Registro', null=False)

    def __str__(self):
        return f"{self.per_descripcion}"