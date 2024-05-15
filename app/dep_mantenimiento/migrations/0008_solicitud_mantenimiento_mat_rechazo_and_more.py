# Generated by Django 4.2.4 on 2024-05-15 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep_mantenimiento', '0007_alter_historialsolicitud_nuevo_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud_mantenimiento',
            name='Mat_Rechazo',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='solicitud_mantenimiento',
            name='Mat_Resuelto',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AddField(
            model_name='solicitud_mantenimiento',
            name='des_Peticion_Mat',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='historialsolicitud',
            name='nuevo_status',
            field=models.CharField(choices=[('Solicitud_Firmada', 'Firmado'), ('Realizado', 'Realizado'), ('Rechazado', 'Rechazado'), ('Pendiente', 'Pendiente'), ('En_proceso', 'En proceso'), ('En_espera', 'En espera'), ('Enviado', 'Enviado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='status',
            field=models.CharField(blank=True, choices=[('Solicitud_Firmada', 'Firmado'), ('Realizado', 'Realizado'), ('Rechazado', 'Rechazado'), ('Pendiente', 'Pendiente'), ('En_proceso', 'En proceso'), ('En_espera', 'En espera'), ('Enviado', 'Enviado')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='tipo_servicio',
            field=models.CharField(blank=True, choices=[('Pintura', 'Pintura'), ('Otro', 'Otro'), ('Pintarrón', 'Pintarrón'), ('Electrica', 'Electrica'), ('Cañones', 'Cañones'), ('Cerrajería', 'Cerrajería'), ('Plomería', 'Plomería'), ('Herrería', 'Herrería')], max_length=100),
        ),
        migrations.AlterField(
            model_name='trabajadores',
            name='puesto',
            field=models.CharField(blank=True, choices=[('Subdirector', 'Subdirector/a'), ('Empleado', 'Empleado'), ('Secretario', 'Secretario/a'), ('Docente', 'Docente'), ('Jefe', 'Jefe')], max_length=100, null=True),
        ),
    ]
