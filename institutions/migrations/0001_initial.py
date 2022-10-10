# Generated by Django 3.2.16 on 2022-10-08 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('system', '0001_initial'),
        ('advisers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsTypeRegistries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('deleted_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=50, null=True, verbose_name='Código')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('detail', models.CharField(blank=True, max_length=100, null=True, verbose_name='Detalle')),
                ('type', models.CharField(blank=True, choices=[('GRUPO', 'GRUPO'), ('ITEM', 'ITEM')], max_length=10, null=True, verbose_name='Tipo')),
                ('route', models.CharField(blank=True, editable=False, max_length=1024, null=True)),
                ('order', models.CharField(blank=True, editable=False, max_length=1024, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.instyperegistries', verbose_name='Principal')),
            ],
            options={
                'verbose_name': 'Tipo de Registro',
                'verbose_name_plural': 'Tipo de Registros',
                'ordering': ('created_at',),
            },
        ),
        migrations.CreateModel(
            name='Institutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(blank=True, editable=False, max_length=1024, null=True, verbose_name='Detalle')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('deleted_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('deleted_reason', models.CharField(blank=True, editable=False, max_length=250, null=True)),
                ('code', models.CharField(blank=True, max_length=3, null=True, verbose_name='Código')),
                ('number', models.CharField(blank=True, editable=False, max_length=10, null=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('alias', models.CharField(blank=True, max_length=20, null=True, verbose_name='Alias')),
                ('representative', models.CharField(blank=True, max_length=200, null=True, verbose_name='Representante')),
                ('identification', models.CharField(blank=True, max_length=20, null=True, verbose_name='Identificación')),
                ('address', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Dirección')),
                ('code_postal', models.CharField(blank=True, max_length=10, null=True, verbose_name='Cod. postal')),
                ('telephone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Teléfono')),
                ('email', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email')),
                ('email_alternate', models.CharField(blank=True, max_length=150, null=True, verbose_name='Email alterno')),
                ('web', models.CharField(blank=True, max_length=200, null=True, verbose_name='Web')),
                ('file_constitution', models.FileField(blank=True, max_length=1024, null=True, upload_to='institutions/constitution/%Y/%m/%d', verbose_name='Archivo constitución')),
                ('file_nomination', models.FileField(blank=True, max_length=1024, null=True, upload_to='institutions/nomination/%Y/%m/%d', verbose_name='Archivo Nominación')),
                ('file_title_academic', models.FileField(blank=True, max_length=1024, null=True, upload_to='institutions/title_academic/%Y/%m/%d', verbose_name='Titulo académico')),
                ('logo', models.ImageField(blank=True, max_length=1024, null=True, upload_to='institutions/logo/%Y/%m/%d')),
                ('adviser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='advisers.advisers', verbose_name='Asesor')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.syscountries', verbose_name='Pais')),
                ('type_registration', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='institutions.instyperegistries', verbose_name='Tipo de registro')),
            ],
            options={
                'verbose_name': 'Institución',
                'verbose_name_plural': 'Instituciones',
                'ordering': ('created_at',),
            },
        ),
    ]
