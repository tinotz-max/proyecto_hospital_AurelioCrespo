from django.db import migrations

def cargar_datos_hospitalarios(apps, schema_editor):
    Departamento = apps.get_model('inventario', 'Departamento')
    Laboratorio = apps.get_model('inventario', 'Laboratorio')
    Producto = apps.get_model('inventario', 'Producto')

    # 1. Inyectar Departamentos Clínicos (Punto 1)
    depto1 = Departamento.objects.create(nombre="Guardia Central / Shockroom", piso_ubicacion="Planta Baja")
    depto2 = Departamento.objects.create(nombre="Terapia Intensiva (UTI)", piso_ubicacion="Primer Piso")
    depto3 = Departamento.objects.create(nombre="Quirófano General", piso_ubicacion="Primer Piso")
    depto4 = Departamento.objects.create(nombre="Pediatría y Neonatología", piso_ubicacion="Planta Baja")

    # 2. Inyectar Laboratorios Farmacéuticos (Punto 3)
    lab1 = Laboratorio.objects.create(nombre="Laboratorio Roemmers", contacto="Dr. Martínez", email="roemmers@hospital.com", cod_barra="RM779")
    lab2 = Laboratorio.objects.create(nombre="Bayer S.A.", contacto="Dra. Lopez", email="bayer@hospital.com", cod_barra="BY779")
    lab3 = Laboratorio.objects.create(nombre="Gador", contacto="Farm. Gómez", email="gador@hospital.com", cod_barra="GD779")

    # 3. Inyectar Productos Médicos Base (Punto 3)
    Producto.objects.create(nombre="Amoxicilina 500mg (Comprimidos)", tipo_producto="MED", refrigeracion=False, nivel_riesgo="Bajo", codigo_ocasa="OC-AMX-01")
    Producto.objects.create(nombre="Insulina NPH (Frasco Ampolla)", tipo_producto="MED", refrigeracion=True, nivel_riesgo="Alto", codigo_ocasa="OC-INS-02")
    Producto.objects.create(nombre="Jeringas Descartables 5ml c/Aguja", tipo_producto="DES", refrigeracion=False, nivel_riesgo="Bajo", codigo_ocasa="OC-JER-03")
    Producto.objects.create(nombre="Guantes de Látex Estériles (Talla M)", tipo_producto="DES", refrigeracion=False, nivel_riesgo="Bajo", codigo_ocasa="OC-GUA-04")

class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0001_initial'), # Asegurate de que coincida con el nombre de tu primera migración
    ]

    operations = [
        migrations.RunPython(cargar_datos_hospitalarios),
    ]