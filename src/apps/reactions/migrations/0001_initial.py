# Generated by Django 3.2.16 on 2023-01-23 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('like', models.BooleanField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
        ),
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['owner'], name='reactions_l_owner_i_71e1f6_idx'),
        ),
        migrations.AddIndex(
            model_name='like',
            index=models.Index(fields=['owner', 'object_id'], name='reactions_l_owner_i_25ab77_idx'),
        ),
    ]
