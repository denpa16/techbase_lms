# Generated by Django 4.1.3 on 2022-12-07 07:25

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ("drf_tracking", "0002_add_extentions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="apirequestlog",
            name="host",
            field=models.URLField(db_index=True, verbose_name="Хост"),
        ),
        migrations.AlterField(
            model_name="apirequestlog",
            name="method",
            field=models.CharField(db_index=True, max_length=10, verbose_name="Метод запроса"),
        ),
        migrations.AlterField(
            model_name="apirequestlog",
            name="remote_addr",
            field=models.GenericIPAddressField(
                db_index=True, verbose_name="IP-адрес источника запроса"
            ),
        ),
        migrations.AlterField(
            model_name="apirequestlog",
            name="username_persistent",
            field=models.CharField(
                blank=True,
                db_index=True,
                help_text="Поле сохраняется даже если объект пользователя удален",
                max_length=200,
                null=True,
                verbose_name="Имя пользователя",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(
                django.db.models.functions.text.Upper("username_persistent"),
                name="username_persistent_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["username_persistent"],
                name="username_persistent_gin_idx",
                opclasses=["gin_trgm_ops"],
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("username_persistent"),
                    name="gin_trgm_ops",
                ),
                name="username_persistent_up_gin_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(django.db.models.functions.text.Upper("path"), name="path_idx"),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["path"], name="path_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("path"), name="gin_trgm_ops"
                ),
                name="path_up_gin_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(django.db.models.functions.text.Upper("view"), name="view_idx"),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["view"], name="view_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("view"), name="gin_trgm_ops"
                ),
                name="view_upper_gin_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(
                django.db.models.functions.text.Upper("view_method"), name="view_method_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["view_method"], name="view_method_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("view_method"), name="gin_trgm_ops"
                ),
                name="view_method_upper_gin_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(django.db.models.functions.text.Upper("host"), name="host_idx"),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["host"], name="host_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("host"), name="gin_trgm_ops"
                ),
                name="host_upper_gin_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=models.Index(django.db.models.functions.text.Upper("method"), name="method_idx"),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["method"], name="method_gin_idx", opclasses=["gin_trgm_ops"]
            ),
        ),
        migrations.AddIndex(
            model_name="apirequestlog",
            index=django.contrib.postgres.indexes.GinIndex(
                django.contrib.postgres.indexes.OpClass(
                    django.db.models.functions.text.Upper("method"), name="gin_trgm_ops"
                ),
                name="method_upper_gin_idx",
            ),
        ),
    ]