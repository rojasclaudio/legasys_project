
from django.contrib import admin
from .models import Alumno, Asignatura, CargoProfesor, CargoProfesorCategoria, CargoProfesorDetalle, NombramientoDetalle, PeriodoLectivo, Persona, LegajoAlumno, TipoDocumento, Facultad, Carrera, SedeFilial, DetalleSedeFilial, Cargo, Funcionario, Profesor, \
                    Nombramiento, Plan, TipoDocumentoDetalle

#PARTE ALUMNO

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

    list_display = ['crr_descripcion', 'get_fac_descripcion']

    def get_fac_descripcion(self, obj):
        return obj.facultad.fac_descripcion
    
    get_fac_descripcion.short_description = 'Facultad'

class SedeFilialAdmin(admin.ModelAdmin):
    model = SedeFilial

class DetalleSedeFilialAdmin(admin.ModelAdmin):
    model = DetalleSedeFilial


class AlumnoAdmin(admin.ModelAdmin):
    model = Alumno
    #Aqui se pasa la lista de las cosas que se quiere mostrar en el reporte
    list_display = ['get_first_name', 'get_last_name', 'get_per_cedula']

    #aqui se crea una funcion para retornar el campo que se quiere mostrar
    def get_first_name(self, obj):
        return obj.persona.first_name
    
    def get_last_name(self, obj):
        return obj.persona.last_name
    
    def get_per_cedula(self, obj):
        return obj.persona.per_cedula
    
    #Aqui se cambia de nombre el nombre de la cabecera del reporte
    get_first_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    get_per_cedula.short_description = 'Cedula'

class CargoAdmin(admin.ModelAdmin):
    model = Cargo


class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario

    #Aqui se pasa la lista de las cosas que se quiere mostrar en el reporte
    list_display = ['get_first_name', 'get_last_name', 'get_per_cedula', 'get_car_descripcion', 'fun_firmante']

    #aqui se crea una funcion para retornar el campo que se quiere mostrar proveniente de un foreingkey
    def get_first_name(self, obj):
        return obj.persona.first_name
    
    def get_last_name(self, obj):
        return obj.persona.last_name
    
    def get_per_cedula(self, obj):
        return obj.persona.per_cedula
    
    def get_car_descripcion(self, obj):
        return obj.cargo.car_descripcion
    

    #Aqui se cambia de nombre el nombre de la cabecera del reporte
    get_first_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    get_per_cedula.short_description = 'Cedula'
    get_car_descripcion.short_description = 'Cargo'

class TipoDocumentoAdmin(admin.ModelAdmin):
    model = TipoDocumento

class TipoDocumentoDetalleAdmin(admin.ModelAdmin):
    model = TipoDocumentoDetalle

#Esta clase genera una lista de documentos para pasarle a legajo
class TipoDeDocumentoDetalleInLine(admin.TabularInline):
    model = TipoDocumentoDetalle
    #Esta configuracion es para limitar la cantidad de lineas de la lista
    extra = 0
    
class LegajoAlumnoAdmin(admin.ModelAdmin):
    inlines = [TipoDeDocumentoDetalleInLine]
    model = LegajoAlumno

    list_display = ['get_first_name', 'get_last_name', 'get_per_cedula']

    def get_first_name(self, obj):
        return obj.alumno.persona.first_name
    
    def get_last_name(self, obj):
        return obj.alumno.persona.last_name
    
    def get_per_cedula(self, obj):
        return obj.alumno.persona.per_cedula
    
    get_first_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    get_per_cedula.short_description = 'Cedula'

#PARTE PROFESOR

class ProfesorAdmin(admin.ModelAdmin):
    model = Profesor

    #Aqui se pasa la lista de las cosas que se quiere mostrar en el reporte
    list_display = ['get_first_name', 'get_last_name', 'get_per_cedula']

    #aqui se crea una funcion para retornar el campo que se quiere mostrar
    def get_first_name(self, obj):
        return obj.persona.first_name
    
    def get_last_name(self, obj):
        return obj.persona.last_name
    
    def get_per_cedula(self, obj):
        return obj.persona.per_cedula
    
    #Aqui se cambia de nombre el nombre de la cabecera del reporte
    get_first_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    get_per_cedula.short_description = 'Cedula'

class PlanAdmin(admin.ModelAdmin):
    model = Plan

class AsignaturaAdmin(admin.ModelAdmin):
    model = Asignatura

    list_display = ['asi_descripcion', 'get_pln_descripcion']

    def get_pln_descripcion(self, obj):
        return obj.plan.pln_descripcion
    
    get_pln_descripcion.shor_description = 'Plan'

class CargoProfesorCategoriaAdmin(admin.ModelAdmin):
    model = CargoProfesorCategoria

class CargoProfesorAdmin(admin.ModelAdmin):
    model = CargoProfesor

class CargoProfesorDetalleAdmin(admin.ModelAdmin):
    model = CargoProfesorDetalle

class PeriodoLectivoAdmin(admin.ModelAdmin):
    model = PeriodoLectivo

class NombramientoDetalleInLine(admin.TabularInline):
    model = NombramientoDetalle
    extra = 0

class NombramientoDetalleAdmin(admin.ModelAdmin):
    model = NombramientoDetalle

    list_display = ['get_first_name', 'get_last_name', 'get_nombramiento']

    def get_first_name(self, obj):
        return obj.profesor.persona.first_name
    
    def get_last_name(self, obj):
        return obj.profesor.persona.last_name
    
    def get_nombramiento(self, obj):
        return obj.nombramiento
    
    get_first_name.short_description = 'Nombre'
    get_last_name.short_description = 'Apellido'
    get_nombramiento.short_description = 'Nombramiento'

class NombramientoAdmin(admin.ModelAdmin):
    inlines = [NombramientoDetalleInLine]
    model = Nombramiento
    

# Register your models here.

#PARTE ALUMNO
admin.site.register(Facultad, FacultadAdmin)
admin.site.register(Carrera, CarreraAdmin)
admin.site.register(SedeFilial, SedeFilialAdmin)
admin.site.register(DetalleSedeFilial, DetalleSedeFilialAdmin)
admin.site.register(Persona, PersonaAdmin)
admin.site.register(Cargo, CargoAdmin)
admin.site.register(Funcionario, FuncionarioAdmin)
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)
#admin.site.register(TipoDocumentoDetalle, TipoDocumentoDetalleAdmin)
admin.site.register(LegajoAlumno, LegajoAlumnoAdmin)

#PARTE PROFESOR
admin.site.register(Profesor, ProfesorAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Asignatura, AsignaturaAdmin)
admin.site.register(PeriodoLectivo, PeriodoLectivoAdmin)
admin.site.register(CargoProfesorCategoria, CargoProfesorCategoriaAdmin)
admin.site.register(CargoProfesor, CargoProfesorAdmin)
admin.site.register(CargoProfesorDetalle, CargoProfesorDetalleAdmin)
admin.site.register(Nombramiento, NombramientoAdmin)
admin.site.register(NombramientoDetalle, NombramientoDetalleAdmin)