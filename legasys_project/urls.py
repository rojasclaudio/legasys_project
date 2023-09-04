"""
URL configuration for legasys_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from legasys_app import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generar_constancia/', views.generar_constancia, name='generar_constancia'),
    path('generar_nombramiento/', views.generar_nombramiento, name='generar_nombramiento'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_pdf/<int:student_id>/', views.generate_pdf, name='generate_pdf_with_id'),
    
    path('generate_pdf2/', views.generate_pdf2, name='generate_pdf2'),
    path('generate_pdf2/<int:sede_filial_id>/', views.generate_pdf2, name='generate_pdf2_by_sede'),
    path('generate_pdf2/<int:sede_filial_id>/<str:nom_numero_resolucion>/', views.generate_pdf2, name='generate_pdf2_by_sede_and_resolucion'),

    path('home/', views.home_view, name='home'),
    # ... Other URL patterns ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

