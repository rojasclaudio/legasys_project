import io
import os
from itertools import groupby
from tkinter import Frame

from django.shortcuts import render
from django.http import FileResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404  # Add this import
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.templatetags.static import static

from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4, landscape, letter, legal
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, BaseDocTemplate, Image, KeepTogether, PageBreak, PageTemplate, Frame
from reportlab.lib.units import cm, inch
from reportlab.pdfgen.canvas import Canvas

from .models import Alumno, Nombramiento, NombramientoDetalle, SedeFilial, TipoDocumentoDetalle, Funcionario, Cargo





# Create your views here.
def generar_constancia(request):
    return render (request, 'generar_constancia.html')

def generar_nombramiento(request):
    return render (request, 'generar_nombramiento.html')
    

#...............................................................................................................................
def generate_pdf(request):
    if request.method == "POST":
        student_id = request.POST.get('student_id')
        funcionario_id = request.POST.get('funcionario_id')
        
        student = None
        funcionario = None

        if student_id:
            student = get_object_or_404(Alumno, id=student_id)
            document_details = TipoDocumentoDetalle.objects.filter(legajoAlumno__alumno=student)
        else:
            document_details = TipoDocumentoDetalle.objects.all()

        if funcionario_id:
            funcionario = get_object_or_404(Funcionario, id=funcionario_id)
            

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Legajo.pdf"'

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)

        image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logoUnican.png')
        logo = Image(image_path)  # Adjust width and height as necessary

        right_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logoFacitec.png')
        right_logo = Image(right_image_path)  # Adjust width and height as necessary

        
        data = [["Documento", "Tipo de Documento", "Vencimiento"]]  # Table header
        for detail in document_details:
            data.append([
                detail.tipoDocumento.doc_descripcion,
                detail.tip_documento,
                detail.tip_vencimiento
            ])

        if student:
            student_name = f"{student.persona.first_name} {student.persona.last_name}"
            title_style = getSampleStyleSheet()['Title']
            title_style.fontName = "Times-Roman"
            title_style.fontSize = 15
            title_paragraph = Paragraph(student_name, title_style)
        else:
            title_style = getSampleStyleSheet()['Title']
            title_style.fontName = "Times-Roman"
            title_style.fontSize = 15
            title_paragraph = Paragraph("Student Report", title_style)

        table = Table(data, colWidths=[150, 150, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements = [title_paragraph, table]

        if funcionario:
            cargo_description = funcionario.cargo.car_descripcion  # Get the cargo description
            persona_name = f"{funcionario.persona.first_name} {funcionario.persona.last_name}"
            funcionario_paragraph = Paragraph(f" {persona_name} <br/> {cargo_description} <br/> Facultad de Ciencias y Tecnología", title_style)
            
            elements.append(Spacer(1, 100))
            elements.append(funcionario_paragraph)

        
        centered_text = "UNIVERSIDAD NACIONAL DE CANINDEYÚ <br/> Creada por Ley de la Nación Nº 3.985/10 <br/><br/> Consejo Superior Universitario"
        centered_style = getSampleStyleSheet()['Normal']
        centered_style.fontName = "Times-Roman"
        centered_style.fontSize = 12
        centered_style.alignment = 1  
        centered_paragraph = Paragraph(centered_text, centered_style)

        table_data = [[logo, centered_paragraph, right_logo]]
        header_table = Table(table_data, colWidths=[1*inch, 4*inch, 1*inch])
        header_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

        # Inserting the header_table at the beginning of the elements list
        elements.insert(0, header_table)
        elements.insert(1, Spacer(1, 50))

        
        additional_text = "Mision:<br/>Formar profesionales con estándares de calidad; producir conocimientos<br/>científicos útiles a la sociedad; conservar la cultura; promover y contribuir al desarrollo<br/>sostenible."
        normal_style = getSampleStyleSheet()['Normal']        
        normal_style.fontName = "Times-Roman"  
        normal_style.fontSize = 10
        additional_paragraph = Paragraph(additional_text, normal_style)
        elements.append(Spacer(1, 150))  
        elements.append(additional_paragraph)

        doc.build(elements)

        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response

    # For GET requests or any other method
    students = Alumno.objects.all()
    funcionarios = Funcionario.objects.all()
    context = {
        'students': students,
        'funcionarios': funcionarios
    }
    return render(request, 'generate_constancia.html', context)
#.............................................................................................................................




def generate_pdf2(request):
    sede_filial_id = request.GET.get('sede_filial_id')
    nom_numero_resolucion = request.GET.get('nom_numero_resolucion')

    # Create HttpResponse object with appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="professors.pdf"'

    # Create the PDF object
    p = SimpleDocTemplate(
        response,
        pagesize=A4,
    )
    image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logoUnican.png')
    logo = Image(image_path)  # Adjust width and height as necessary

    right_image_path = os.path.join(settings.STATICFILES_DIRS[0], 'img', 'logoFacitec.png')
    right_logo = Image(right_image_path)  # Adjust width and height as necessary

    # Set up styles and add paragraph to elements
    styles = getSampleStyleSheet()
    elements = []
    
    centered_text = """POR LA CUAL SE NOMBRA PROFESORES EN CARÁCTER DE ENCARGADOS Y <br/>
                        AUXILIARES DE CÁTEDRAS PARA LA CARRERA DE LICENCIATURA EN ANÁLISIS DE SISTEMAS DE LA FACULTAD DE CIENCIAS Y TECNOLOGÍA PARA<br/>
                        LA SEDE DE SAL TOS DEL GUAIRÁ Y LAS FILIALES DE KATUETÉ Y CURUGUATY. <br/><br/>"""
    centered_style = getSampleStyleSheet()['Normal']
    centered_style.fontName = "Times-Roman"
    centered_style.fontSize = 10
    centered_style.alignment = 1
    centered_paragraph = Paragraph(centered_text, centered_style)
    elements.append(centered_paragraph)

    filters = {}
    if sede_filial_id:
        filters['nombramiento__sede_filial_id'] = sede_filial_id
    if nom_numero_resolucion:
        filters['nombramiento__nom_numero_resolucion'] = nom_numero_resolucion

    nombramiento_details = NombramientoDetalle.objects.select_related(
        'profesor__persona', 'asignatura', 'nombramiento__sede_filial'
    ).filter(**filters).order_by('nombramiento__sede_filial')

    if sede_filial_id:
        for sede, group in groupby(nombramiento_details, lambda x: x.nombramiento.sede_filial):
            sede_object = SedeFilial.objects.get(id=sede.id)  # Replace SedeFilial with your actual model name
            elements.append(Paragraph(f"Sede Filial: {sede_object.sed_descripcion}", styles['Normal']))
            data = create_data_table(group)
            create_pdf_table(data, elements)
            # Add a spacer
            elements.append(Spacer(1, 12))
    elif nom_numero_resolucion:
        for sede, group in groupby(nombramiento_details, lambda x: x.nombramiento.sede_filial):
            sede_object = SedeFilial.objects.get(id=sede.id)  # Replace SedeFilial with your actual model name
            elements.append(Paragraph(f"Sede Filial: {sede_object.sed_descripcion}", styles['Normal']))
            data = create_data_table(group)
            create_pdf_table(data, elements)
            # Add a spacer
            elements.append(Spacer(1, 12))
    else:
        for sede, group in groupby(nombramiento_details, lambda x: x.nombramiento.sede_filial):
            sede_object = SedeFilial.objects.get(id=sede.id)  # Replace SedeFilial with your actual model name
            elements.append(Paragraph(f"Sede Filial: {sede_object.sed_descripcion}", styles['Normal']))
            data = create_data_table(group)
            create_pdf_table(data, elements)
            # Add a spacer
            elements.append(Spacer(1, 12))

    elements.append(Spacer(1, 12))

    texto_final = """Que, el Estatuto de la Universidad Nacional de Canindeyú en su Art. 19 establece que:
    "Son atribuciones del Consejo Superior Universitario", inc. j) Nombrar a los profesores titulares,
    adjuntos y asistentes que ganaren los concursos de oposición que serán convocados por el Rectorado de la Universidad. 
    Que, la Ley Nº 3.985/1 O de Creación de la Universidad Nacional de Canindeyú, la faculta a regirse por sus propios estatutos. <br/><br/>
    POR TANTO:<br/> 
    EN USO DE SUS ATRIBUCIONES ESTATUTARIAS Y LEGALES, EL CONSEJO 
    SUPERIOR UNIVERSITARIO DE LA UNIVERSIDAD NACIONAL DE CANINDEYÚ <br/><br/>
    RESUELVE: <br/><br/>
    Art. lro. NOMBRAR profesores en carácter de Encargados y Auxiliares de Cátedras, para los diferentes cursos,
    de la carrera de Licenciatura en Análisis de Sistemas para la sede de Saltos del Guairá y las filiales de Curuguaty y Katueté,
    conforme a la nómina inserta en el considerando de la presente resolución <br/><br/>
    Art. 2do. COMUNICAR a quienes corresponda, publicar y cumplido archivar"""
    final_estilo = getSampleStyleSheet()['Normal']
    final_estilo.fontName = "Times-Roman"
    final_estilo.fontSize = 10
    centered_paragraph = Paragraph(texto_final, final_estilo)
    elements.append(centered_paragraph)


    centered_text = "UNIVERSIDAD NACIONAL DE CANINDEYÚ <br/> Creada por Ley de la Nación Nº 3.985/10 <br/><br/> Consejo Superior Universitario"
    centered_style = getSampleStyleSheet()['Normal']
    centered_style.fontName = "Times-Roman"
    centered_style.fontSize = 12
    centered_style.alignment = 1  
    centered_paragraph = Paragraph(centered_text, centered_style)

    table_data = [[logo, centered_paragraph, right_logo]]
    header_table = Table(table_data, colWidths=[1*inch, 4*inch, 1*inch])
    header_table.setStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')])

    # Inserting the header_table at the beginning of the elements list
    elements.insert(0, header_table)
    elements.insert(1, Spacer(1, 50))

    # Generate PDF
    p.build(elements)

    return response



def initialize_pdf_response():
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="professors.pdf"'
    return response

def get_filters_from_request(request):
    filters = {}
    filters['sede_filial_id'] = request.GET.get('sede_filial_id')
    filters['nom_numero_resolucion'] = request.GET.get('nom_numero_resolucion')
    return filters

def get_filtered_data(filters):
    query = {}
    if filters['sede_filial_id']:
        query['nombramiento__sede_filial_id'] = filters['sede_filial_id']
    if filters['nom_numero_resolucion']:
        query['nombramiento__nom_numero_resolucion'] = filters['nom_numero_resolucion']
        
    return NombramientoDetalle.objects.select_related(
        'profesor__persona', 'asignatura', 'nombramiento__sede_filial'
    ).filter(**query).order_by('nombramiento__sede_filial')


def add_data_to_pdf(data, elements, filters):
    if filters['sede_filial_id']:
        # Assuming you have a model SedeFilial to fetch the sede description.
        sede_filial = SedeFilial.objects.get(id=filters['sede_filial_id'])
        elements.append(Paragraph(f"Sede Filial: {sede_filial.sed_descripcion}", getSampleStyleSheet()['Normal']))
        
    if filters['sede_filial_id'] or filters['nom_numero_resolucion']:
        table_data = create_data_table(data)
        create_pdf_table(table_data, elements)
    else:
        add_grouped_data_to_pdf(data, elements)

def add_grouped_data_to_pdf(data, elements):
    for sede, group in groupby(data, lambda x: x.nombramiento.sede_filial):
        elements.append(Paragraph(f"Sede Filial: {sede.sedefilial.sed_descripcion}", getSampleStyleSheet()['Normal']))
        table_data = create_data_table(group)
        create_pdf_table(table_data, elements)
        elements.append(Spacer(1, 12))

def create_data_table(nombramiento_details):
    # Prepare data for table
    data = [['Profesor', 'Cedula', 'Cargo', 'Categoria Cargo', 'Asignatura']]
    for detail in nombramiento_details:
        data.append([
            str(detail.profesor),
            str(detail.profesor.persona.per_cedula) if detail.profesor.persona else "",
            str(detail.cargo.cargo_profesor),
            str(detail.cargo.cargo_profesor_categoria),
            str(detail.asignatura)
        ])
    return data

def create_pdf_table(data, elements):
    # Create and style table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    # Add table to elements
    
    elements.append(Spacer(1, 10))
    elements.append(table)



#Retorna los datos al HTML
def generar_nombramiento(request):
    # Query the database for unique sede_filial and nom_numero_resolucion
    sede_filial_options = SedeFilial.objects.values('id', 'sed_descripcion')
    num_resolucion_options = NombramientoDetalle.objects.values_list('nombramiento__nom_numero_resolucion', flat=True).distinct()

    
    # Pass the data to your template
    return render(request, 'generar_nombramiento.html', {
        'sede_filial_options': sede_filial_options,
        'num_resolucion_options': num_resolucion_options
    })


# def generate_pdf(request, student_id=None, funcionario_id=None):
#     student = None
#     funcionario = None

#     if student_id:
#         student = get_object_or_404(Alumno, id=student_id)
#         document_details = TipoDocumentoDetalle.objects.filter(legajoAlumno__alumno=student)
#     else:
#         document_details = TipoDocumentoDetalle.objects.all()

#     if funcionario_id:
#         funcionario = get_object_or_404(Funcionario, id=funcionario_id)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)

#     data = [["Document Type", "Document", "Expiration"]]  # Table header
#     for detail in document_details:
#         data.append([
#             detail.tipoDocumento.doc_descripcion,
#             detail.tip_documento,
#             detail.tip_vencimiento
#         ])

#     if student:
#         student_name = f"{student.persona.first_name} {student.persona.last_name}"
#         title_style = getSampleStyleSheet()['Title']
#         title_paragraph = Paragraph(student_name, title_style)
#     else:
#         title_style = getSampleStyleSheet()['Title']
#         title_paragraph = Paragraph("Student Report", title_style)

#     table = Table(data, colWidths=[150, 150, 150])
#     table.setStyle(TableStyle([
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
#         ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
#         ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
#         ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
#         ('GRID', (0, 0), (-1, -1), 1, colors.black)
#     ]))

#     elements = [title_paragraph, table]

#     if funcionario:
#         cargo_description = funcionario.cargo.car_descripcion  # Get the cargo description
#         persona_name = f"{funcionario.persona.first_name} {funcionario.persona.last_name}"
#         funcionario_paragraph = Paragraph(f"Funcionario: {persona_name} (Cargo: {cargo_description})", title_style)
#         elements.append(funcionario_paragraph)

#     doc.build(elements)

#     pdf = buffer.getvalue()
#     buffer.close()

#     response.write(pdf)
#     return response




# def generate_pdf(request, student_id=None):
#     if student_id:
#         student = get_object_or_404(Alumno, id=student_id)
#         document_details = TipoDocumentoDetalle.objects.filter(legajoAlumno__alumno=student)
#     else:
#         document_details = TipoDocumentoDetalle.objects.all()

#     response = FileResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

#     buffer = io.BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)

#     y = 750  # Initial vertical position for text
#     for detail in document_details:
#         c.drawString(100, y, f"Document Type: {detail.tipoDocumento.doc_descripcion}")
#         y -= 20

#         c.drawString(100, y, f"Tipo de Documento: {detail.tip_documento}")
#         y -= 20

#         c.drawString(100, y, f"Vencimiento: {detail.tip_vencimiento}")
#         y -= 20

#         # Add more attributes here...

#         y -= 30  # Space between documents

#     c.save()

#     pdf = buffer.getvalue()
#     buffer.close()

#     # Set the PDF content to the response using the response's .write() method
#     response = FileResponse(io.BytesIO(pdf), content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

#     return response