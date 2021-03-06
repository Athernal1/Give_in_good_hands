# Generated by Django 3.2.12 on 2022-05-04 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_donation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='institution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.institution'),
        ),
        migrations.AlterField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
