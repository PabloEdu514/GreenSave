# Generated by Django 4.1.1 on 2023-02-28 18:28

import dep_alumnos.validators
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counters',
            fields=[
                ('idcounter', models.TextField(blank=True, max_length=45, primary_key=True, serialize=False)),
                ('counter', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'counters',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Dep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(verbose_name=django.contrib.auth.models.User)),
                ('department', models.CharField(max_length=100)),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='perfil/', verbose_name='Imagen de Perfil')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('carrera', models.CharField(blank=True, max_length=200, null=True, verbose_name='Carrera')),
                ('rol', models.CharField(max_length=40, verbose_name='Rol')),
            ],
            options={
                'db_table': 'userDep',
            },
        ),
        migrations.CreateModel(
            name='Precios',
            fields=[
                ('idprecio', models.TextField(blank=True, max_length=45, primary_key=True, serialize=False)),
                ('precio', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'precios',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('idstatus', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'status',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('idtipo', models.IntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
                ('proceso_activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tipo',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='tokens',
            fields=[
                ('idtoken', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(blank=True, max_length=45)),
                ('token_activo', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'tokens',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('idfolio', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('fechainicio', models.CharField(blank=True, max_length=100, null=True)),
                ('fechafinal', models.CharField(blank=True, max_length=100, null=True)),
                ('asunto', models.TextField(blank=True, null=True)),
                ('nocontrol', models.CharField(blank=True, max_length=9, null=True)),
                ('nombre', models.CharField(max_length=45)),
                ('carrera', models.CharField(blank=True, max_length=60, null=True)),
                ('especialidad', models.CharField(blank=True, max_length=45, null=True)),
                ('telefono', models.CharField(blank=True, max_length=45, null=True)),
                ('correo', models.CharField(blank=True, max_length=45, null=True)),
                ('sexo', models.CharField(blank=True, max_length=45, null=True)),
                ('primer_apellido', models.CharField(max_length=45)),
                ('segundo_apellido', models.CharField(blank=True, max_length=45, null=True)),
                ('semestre', models.IntegerField(blank=True, null=True)),
                ('referencia_pago_referencia', models.CharField(blank=True, max_length=45, null=True)),
                ('motivo', models.TextField(blank=True, null=True)),
                ('cancelacion', models.TextField(blank=True, null=True)),
                ('doc_solicitud', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('doc_kardex', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('doc_comprobante', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('doc_otro', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('doc_examen', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('doc_comba', models.FileField(blank=True, max_length=150, null=True, upload_to='', validators=[dep_alumnos.validators.validate_file_extension])),
                ('responsable', models.CharField(blank=True, max_length=45, null=True)),
                ('respuesta', models.CharField(blank=True, max_length=250, null=True)),
                ('fechalimite', models.DateField(blank=True, null=True)),
                ('status_referencia', models.CharField(blank=True, max_length=45, null=True)),
                ('carrera_destino', models.CharField(blank=True, max_length=60, null=True)),
                ('status_dictamen', models.CharField(blank=True, max_length=45, null=True)),
                ('folio_final', models.CharField(blank=True, max_length=45, null=True)),
                ('idstatus', models.ForeignKey(db_column='idstatus', on_delete=django.db.models.deletion.DO_NOTHING, to='dep.status')),
                ('idtipo', models.ForeignKey(db_column='idtipo', on_delete=django.db.models.deletion.DO_NOTHING, to='dep.tipo')),
            ],
            options={
                'db_table': 'solicitud',
                'managed': True,
            },
        ),
    ]
