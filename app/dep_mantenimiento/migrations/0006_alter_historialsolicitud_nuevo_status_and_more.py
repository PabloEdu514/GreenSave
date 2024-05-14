# Generated by Django 4.2.4 on 2024-05-10 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep_mantenimiento', '0005_rename_firma_jefe_mantenimiento_img_solicitud_mantenimiento_firma_jefe_vobo_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialsolicitud',
            name='nuevo_status',
            field=models.CharField(choices=[('En_espera', 'En espera'), ('En_proceso', 'En proceso'), ('Pendiente', 'Pendiente'), ('Realizado', 'Realizado'), ('Rechazado', 'Rechazado'), ('Enviado', 'Enviado'), ('Solicitud_Firmada', 'Firmado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='status',
            field=models.CharField(blank=True, choices=[('En_espera', 'En espera'), ('En_proceso', 'En proceso'), ('Pendiente', 'Pendiente'), ('Realizado', 'Realizado'), ('Rechazado', 'Rechazado'), ('Enviado', 'Enviado'), ('Solicitud_Firmada', 'Firmado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='tipo_servicio',
            field=models.CharField(blank=True, choices=[('Electrica', 'Electrica'), ('Cañones', 'Cañones'), ('Otro', 'Otro'), ('Herrería', 'Herrería'), ('Pintura', 'Pintura'), ('Pintarrón', 'Pintarrón'), ('Plomería', 'Plomería'), ('Cerrajería', 'Cerrajería')], max_length=100),
        ),
        migrations.AlterField(
            model_name='trabajadores',
            name='puesto',
            field=models.CharField(blank=True, choices=[('Secretario', 'Secretario/a'), ('Jefe', 'Jefe'), ('Subdirector', 'Subdirector/a'), ('Docente', 'Docente'), ('Empleado', 'Empleado')], max_length=100, null=True),
        ),
    ]
