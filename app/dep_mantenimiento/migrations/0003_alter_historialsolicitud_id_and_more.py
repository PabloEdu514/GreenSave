# Generated by Django 4.2.4 on 2024-05-10 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dep_mantenimiento', '0002_alter_historialsolicitud_hora_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialsolicitud',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='historialsolicitud',
            name='nuevo_status',
            field=models.CharField(choices=[('Rechazado', 'Rechazado'), ('Solicitud_Firmada', 'Firmado'), ('En_espera', 'En espera'), ('Enviado', 'Enviado'), ('En_proceso', 'En proceso'), ('Realizado', 'Realizado'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='status',
            field=models.CharField(blank=True, choices=[('Rechazado', 'Rechazado'), ('Solicitud_Firmada', 'Firmado'), ('En_espera', 'En espera'), ('Enviado', 'Enviado'), ('En_proceso', 'En proceso'), ('Realizado', 'Realizado'), ('Pendiente', 'Pendiente')], max_length=50),
        ),
        migrations.AlterField(
            model_name='solicitud_mantenimiento',
            name='tipo_servicio',
            field=models.CharField(blank=True, choices=[('Cañones', 'Cañones'), ('Otro', 'Otro'), ('Pintarrón', 'Pintarrón'), ('Pintura', 'Pintura'), ('Herrería', 'Herrería'), ('Electrica', 'Electrica'), ('Cerrajería', 'Cerrajería'), ('Plomería', 'Plomería')], max_length=100),
        ),
        migrations.AlterField(
            model_name='trabajadores',
            name='puesto',
            field=models.CharField(blank=True, choices=[('Jefe', 'Jefe'), ('Empleado', 'Empleado'), ('Secretario', 'Secretario/a'), ('Subdirector', 'Subdirector/a'), ('Docente', 'Docente')], max_length=100, null=True),
        ),
    ]