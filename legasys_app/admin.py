
from django.contrib import admin
from .models import Alumno, Asignatura, PeriodoLectivo, Persona, LegajoAlumno, TipoDocumento, Facultad, Carrera, SedeFilial, DetalleSedeFilial, Cargo, Funcionario, Profesor, \
                    Resolucion, Plan


class PersonaAdmin(admin.ModelAdmin):
    model = Persona
    fields = ('first_name', 'last_name', 'per_cedula', 'email', 'per_fecha_nacimiento', 'per_telefono', 'per_direccion')
    list_display = ('first_name', 'last_name', 'per_cedula',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.username = str(obj.per_cedula)
        obj.save()

class FacultadAdmin(admin.ModelAdmin):
    model = Facultad

class CarreraAdmin(admin.ModelAdmin):
    model = Carrera

class SedeFilialAdmin(admin.ModelAdmin):
    model = SedeFilial

class DetalleSedeFilialAdmin(admin.ModelAdmin):
    model = DetalleSedeFilial

class AlumnoAdmin(admin.ModelAdmin):
    model = Alumno

class CargoAdmin(admin.ModelAdmin):
    model = Cargo

class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario
    

class TipoDocumentoAdmin(admin.ModelAdmin):
    model = TipoDocumento

#Esta clase genera una lista de documentos para pasarle a legajo
class TipoDeDocumentoInLine(admin.TabularInline):
    model = TipoDocumento
    #Esta configuracion es para limitar la cantidad de lineas de la lista
    extra = 0
    
class LegajoAlumnoAdmin(admin.ModelAdmin):
    inlines = [TipoDeDocumentoInLine]
    model = LegajoAlumno


class ProfesorAdmin(admin.ModelAdmin):
    model = Profesor

class ResolucionAdmin(admin.ModelAdmin):
    model = Resolucion

class PlanAdmin(admin.ModelAdmin):
    model = Plan

class AsignaturaAdmin(admin.ModelAdmin):
    model = Asignatura

class PeriodoLectivoAdmin(admin.ModelAdmin):
    model = PeriodoLectivo

# Register your models here.
admin.site.register(Facultad, FacultadAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(SedeFilial, SedeFilialAdmin)
admin.site.register(DetalleSedeFilial, DetalleSedeFilialAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(LegajoAlumno, LegajoAlumnoAdmin)
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Resolucion, ResolucionAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Asignatura, AlumnoAdmin)
admin.site.register(PeriodoLectivo, PeriodoLectivoAdmin)