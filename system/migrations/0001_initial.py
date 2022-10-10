# Generated by Django 3.2.16 on 2022-10-08 23:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SysCountries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('deleted_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('name_short', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre corto')),
            ],
            options={
                'verbose_name': 'Pais',
                'verbose_name_plural': 'Paises',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SysNationality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('created_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('update_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('deleted_by', models.CharField(blank=True, editable=False, max_length=100, null=True)),
                ('code', models.CharField(blank=True, max_length=10, null=True, verbose_name='Código')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('name_short', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nombre corto')),
            ],
            options={
                'verbose_name': 'Nacionalidad',
                'verbose_name_plural': 'Nacionalidades',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SysParameters',
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
                ('name', models.CharField(max_length=200, verbose_name='Nombre')),
                ('type_parameter', models.CharField(choices=[('LIST', 'LIST'), ('LISTITEM', 'LISTITEM'), ('PARAMETER', 'PARAMETER'), ('TREE', 'TREE'), ('TREENODE', 'TREENODE')], max_length=10, verbose_name='Tipo parametro')),
                ('value', models.CharField(blank=True, max_length=100, null=True, verbose_name='Valor')),
                ('status', models.BooleanField(default=False, verbose_name='Estado')),
                ('extra_data', models.CharField(blank=True, max_length=1024, null=True, verbose_name='Extra datos')),
                ('route', models.CharField(blank=True, editable=False, max_length=1024, null=True)),
                ('order', models.CharField(blank=True, editable=False, max_length=1024, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='system.sysparameters')),
            ],
            options={
                'verbose_name': 'Parametro',
                'verbose_name_plural': 'Parametros',
                'ordering': ['name'],
            },
        ),
    ]
