# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BackgroundTask(models.Model):
    task_name = models.CharField(max_length=190)
    task_params = models.TextField()
    task_hash = models.CharField(max_length=40)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField()
    run_at = models.DateTimeField()
    repeat = models.BigIntegerField()
    repeat_until = models.DateTimeField(blank=True, null=True)
    queue = models.CharField(max_length=190, blank=True, null=True)
    attempts = models.IntegerField()
    failed_at = models.DateTimeField(blank=True, null=True)
    last_error = models.TextField()
    locked_by = models.CharField(max_length=64, blank=True, null=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'background_task'


class BackgroundTaskCompletedtask(models.Model):
    task_name = models.CharField(max_length=190)
    task_params = models.TextField()
    task_hash = models.CharField(max_length=40)
    verbose_name = models.CharField(max_length=255, blank=True, null=True)
    priority = models.IntegerField()
    run_at = models.DateTimeField()
    repeat = models.BigIntegerField()
    repeat_until = models.DateTimeField(blank=True, null=True)
    queue = models.CharField(max_length=190, blank=True, null=True)
    attempts = models.IntegerField()
    failed_at = models.DateTimeField(blank=True, null=True)
    last_error = models.TextField()
    locked_by = models.CharField(max_length=64, blank=True, null=True)
    locked_at = models.DateTimeField(blank=True, null=True)
    creator_object_id = models.PositiveIntegerField(blank=True, null=True)
    creator_content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'background_task_completedtask'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoCeleryResultsChordcounter(models.Model):
    sub_tasks = models.TextField()
    count = models.PositiveIntegerField()
    group_id = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'django_celery_results_chordcounter'


class DjangoCeleryResultsGroupresult(models.Model):
    group_id = models.CharField(unique=True, max_length=255)
    date_created = models.DateTimeField()
    date_done = models.DateTimeField()
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_groupresult'


class DjangoCeleryResultsTaskresult(models.Model):
    task_id = models.CharField(unique=True, max_length=255)
    status = models.CharField(max_length=50)
    content_type = models.CharField(max_length=128)
    content_encoding = models.CharField(max_length=64)
    result = models.TextField(blank=True, null=True)
    date_done = models.DateTimeField()
    traceback = models.TextField(blank=True, null=True)
    meta = models.TextField(blank=True, null=True)
    task_args = models.TextField(blank=True, null=True)
    task_kwargs = models.TextField(blank=True, null=True)
    task_name = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField()
    worker = models.CharField(max_length=100, blank=True, null=True)
    periodic_task_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_celery_results_taskresult'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GoodsCategories(models.Model):
    name = models.CharField(unique=True, max_length=150)
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_categories'


class ParserParserstatus(models.Model):
    status = models.CharField(max_length=10)
    last_run = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parser_parserstatus'


class Product(models.Model):
    name = models.CharField(unique=True, max_length=150)
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    quantity = models.PositiveIntegerField()
    category = models.ForeignKey(GoodsCategories, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product'
