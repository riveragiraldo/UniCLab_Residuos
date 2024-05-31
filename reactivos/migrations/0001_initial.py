# Generated by Django 5.0.4 on 2024-05-31 17:19

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracionSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiempo_solicitudes', models.PositiveIntegerField(default=90, verbose_name='Tiempo para depuración de solicitudes (días)')),
                ('tiempo_eventos', models.PositiveIntegerField(default=90, verbose_name='Tiempo para depuración de eventos (días)')),
                ('tiempo_vencimiento_reactivos', models.PositiveIntegerField(default=90, verbose_name='Tiempo para verificar vencimiento de reactivos (días)')),
                ('correo_administrador', models.EmailField(max_length=100, verbose_name='Correo del Administrador del Sistema')),
                ('intervalo_tiempo', models.PositiveIntegerField(verbose_name='Tiempo de revisión de fechas de vencimiento')),
                ('fecha_incio', models.DateTimeField(blank=True, null=True, verbose_name='Fecha y hora de inicio')),
                ('programacion_activa', models.BooleanField(default=False, verbose_name='Activar / Desactivar programación')),
                ('manual', models.FileField(blank=True, null=True, upload_to='manual/')),
                ('logo_institucional', models.ImageField(blank=True, null=True, upload_to='logo')),
                ('url', models.CharField(blank=True, default='https://manizales.unal.edu.co/', max_length=500, null=True, verbose_name='Url')),
            ],
            options={
                'verbose_name': 'Configuración del aplicativo',
                'verbose_name_plural': 'Configuraciones del aplicativo',
            },
        ),
        migrations.CreateModel(
            name='TipoEvento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre del tipo de evento')),
            ],
            options={
                'verbose_name': 'Tipo de evento',
                'verbose_name_plural': 'Tipos de eventos',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electrónico')),
                ('acceptDataProcessing', models.BooleanField(default=False, verbose_name='Acepta tratamiento de datos')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('id_number', models.BigIntegerField(blank=True, null=True, unique=True, verbose_name='Número de identificación')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Teléfono')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_User', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_User', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AlmacenamientoInterno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(max_length=1000, verbose_name='Descripción')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_respel', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Almacenamiento Interno',
                'verbose_name_plural': 'Almacenamiento Interno',
            },
        ),
        migrations.CreateModel(
            name='ClaseAlmacenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(max_length=1000, verbose_name='Descripción')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_by', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_storage_class', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Clase de Almacenamiento',
                'verbose_name_plural': 'Clases de almacenamiento',
            },
        ),
        migrations.CreateModel(
            name='Destinos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Destino')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Destinos', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Destino',
                'verbose_name_plural': 'Destinos',
            },
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Estado')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_states', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
            },
        ),
        migrations.CreateModel(
            name='Facultades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre Facultad')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Facultades', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Facultad',
                'verbose_name_plural': 'Facultades',
            },
        ),
        migrations.CreateModel(
            name='Laboratorios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre Laboratorio')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Lab', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Laboratorio',
                'verbose_name_plural': 'Laboratorios',
            },
        ),
        migrations.CreateModel(
            name='Almacenamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ubicación en almacen')),
                ('description', models.TextField(max_length=1000, verbose_name='Descripción')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Storage', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labrel', to='reactivos.laboratorios', verbose_name='Laboratorio')),
            ],
            options={
                'verbose_name': 'Ubicación en Almacén',
                'verbose_name_plural': 'Ubicación en Almacén',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='lab',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab_users', to='reactivos.laboratorios', verbose_name='laboratorio'),
        ),
        migrations.CreateModel(
            name='Marcas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Marca')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha Registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_trademarks', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
            },
        ),
        migrations.CreateModel(
            name='Reactivos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, unique=True, verbose_name='Código')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Nombre')),
                ('cas', models.CharField(max_length=20, verbose_name='Código CAS')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('almacenamiento_interno', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AlmacenamientoInterno', to='reactivos.almacenamientointerno', verbose_name='Almacenamiento Interno')),
                ('clase_almacenamiento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ClaseAlmacenamiento', to='reactivos.clasealmacenamiento', verbose_name='Clase Almacenamiento')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Reactivo', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='reactivos.estados', verbose_name='Presentación')),
            ],
            options={
                'verbose_name': 'Reactivo',
                'verbose_name_plural': 'Reactivos',
            },
        ),
        migrations.CreateModel(
            name='Inventarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Cantidad en inventario')),
                ('reference', models.CharField(max_length=20, verbose_name='Referencia')),
                ('edate', models.DateField(blank=True, null=True, verbose_name='Fecha de vencimiento')),
                ('visibility', models.BooleanField(default=True, verbose_name='Visibilidad')),
                ('minStockControl', models.BooleanField(default=True, verbose_name='Control de Stock Mínimo')),
                ('minstock', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Ingrese el stock mínimo (puede ser nulo).', max_digits=8, null=True, verbose_name='Stock mínimo')),
                ('is_active', models.BooleanField(default=True, verbose_name='Activo')),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Inventory', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('wlocation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wloc', to='reactivos.almacenamiento', verbose_name='Ubicación en Almacén')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='laboratorio', to='reactivos.laboratorios', verbose_name='Laboratorio')),
                ('trademark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.marcas', verbose_name='Marca')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.reactivos', verbose_name='Nombre del reactivo')),
            ],
            options={
                'verbose_name_plural': 'Inventarios',
            },
        ),
        migrations.CreateModel(
            name='Responsables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cc', models.BigIntegerField(verbose_name='Cédula')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre Responsable')),
                ('mail', models.EmailField(max_length=255, verbose_name='Email')),
                ('phone', models.CharField(max_length=15, verbose_name='Teléfono')),
                ('acceptDataProcessing', models.BooleanField(default=False, verbose_name='Acepta tratamiento de datos')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Manager', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Responsable',
                'verbose_name_plural': 'Responsables',
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Rol')),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Rol', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('user_create', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_Rol', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Rol',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='rol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rol_user', to='reactivos.rol', verbose_name='Rol'),
        ),
        migrations.CreateModel(
            name='SolicitudesExternas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator(message='El nombre y apellido debe incluir únicamente letras, máximo 50 caracteres.', regex='^[A-Za-z\\s]+$')], verbose_name='Nombres y apellidos')),
                ('subject', models.CharField(max_length=100, verbose_name='Asunto')),
                ('message', models.TextField(max_length=1000, verbose_name='Mensaje')),
                ('attach', models.FileField(blank=True, null=True, upload_to='solicitud_attachments/', verbose_name='Archivos adjunto')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator(allowlist=['@unal.edu.co'], message='El correo electrónico debe pertenecer al dominio @unal.edu.co.')], verbose_name='Correo Electrónico')),
                ('mobile_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='El número de móvil debe estar en el rango de 3000000000 a 3999999999.', regex='^[3-9]\\d{9}$')], verbose_name='Teléfono Móvil')),
                ('department', models.CharField(max_length=100, verbose_name='Departamento')),
                ('accept_politics', models.BooleanField(verbose_name='PTDP')),
                ('is_view', models.BooleanField(default=False, verbose_name='Visto')),
                ('has_answered', models.BooleanField(default=False, verbose_name='Respondido')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.laboratorios', verbose_name='Fecha y hora de solicitud')),
            ],
            options={
                'verbose_name_plural': 'Solicitudes Externas',
            },
        ),
        migrations.CreateModel(
            name='Eventos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_evento', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha evento')),
                ('usuario_evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario evento')),
                ('tipo_evento', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactivos.tipoevento', verbose_name='Tipo de evento')),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='TipoSolicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_TipoS', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Tipo de solicitud',
                'verbose_name_plural': 'Tipo de solicitud',
            },
        ),
        migrations.CreateModel(
            name='Solicitudes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='Asunto')),
                ('mensaje', models.TextField(max_length=1000)),
                ('archivos_adjuntos', models.FileField(blank=True, null=True, upload_to='archivos/')),
                ('tramitado', models.BooleanField(blank=True, default=False, null=True)),
                ('observaciones', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha_tramite', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de trámite')),
                ('is_active', models.BooleanField(blank=True, default=True, null=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, null=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_solicitudes', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('usuario_tramita', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='UserTramite', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Tramita')),
                ('tipo_solicitud', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='reactivos.tiposolicitud', verbose_name='Tipo de solicitud')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Ubicaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Ubicación/Asignaturas')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('facultad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='facultad', to='reactivos.facultades', verbose_name='Facultad')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Ubicaciones', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Ubicación/Asignaturas',
                'verbose_name_plural': 'Ubicaciones/Asignaturas',
            },
        ),
        migrations.CreateModel(
            name='Salidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255, verbose_name='Referencia')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Cantidad de salida')),
                ('observations', models.TextField(max_length=1000, verbose_name='Observaciones')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='reactivos.destinos', verbose_name='Destino')),
                ('inventario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inventory', to='reactivos.inventarios', verbose_name='Id_Inventario')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lab', to='reactivos.laboratorios', verbose_name='Laboratorio')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_Out', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='reactivos.responsables', verbose_name='Responsable')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_react', to='reactivos.reactivos', verbose_name='Nombre Reactivo')),
                ('trademark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_trademark', to='reactivos.marcas', verbose_name='Marca')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='location', to='reactivos.ubicaciones', verbose_name='Ubicación')),
            ],
            options={
                'verbose_name': 'Salida',
                'verbose_name_plural': 'Salidas',
            },
        ),
        migrations.CreateModel(
            name='Entradas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference', models.CharField(max_length=255, verbose_name='Referencia')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Cantidad de entrada')),
                ('order', models.CharField(max_length=255, verbose_name='Orden No.')),
                ('date_order', models.DateField(blank=True, null=True, verbose_name='Fecha de orden')),
                ('observations', models.TextField(max_length=1000, verbose_name='Observaciones')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Valor')),
                ('nproject', models.CharField(max_length=15, verbose_name='Número de proyecto')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reactivos.destinos', verbose_name='Destino')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_In', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
                ('inventario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inv', to='reactivos.inventarios', verbose_name='Id_Inventario')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='labs', to='reactivos.laboratorios', verbose_name='Laboratorio')),
                ('trademark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_marca', to='reactivos.marcas', verbose_name='Marca')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='name_reactivo', to='reactivos.reactivos', verbose_name='Nombre Reactivo')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responsable', to='reactivos.responsables', verbose_name='Responsable')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Ubicacion', to='reactivos.ubicaciones', verbose_name='Asignatura/Ubicación')),
            ],
            options={
                'verbose_name': 'Entrada',
                'verbose_name_plural': 'Entradas',
            },
        ),
        migrations.CreateModel(
            name='Unidades',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Unidad')),
                ('is_active', models.BooleanField(default=True)),
                ('date_create', models.DateTimeField(auto_now_add=True, verbose_name='Fecha registro')),
                ('last_update', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
                ('last_updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updateby_units', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado por')),
            ],
            options={
                'verbose_name': 'Unidad',
                'verbose_name_plural': 'Unidades',
            },
        ),
        migrations.AddField(
            model_name='reactivos',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reactive', to='reactivos.unidades', verbose_name='Unidad'),
        ),
    ]
