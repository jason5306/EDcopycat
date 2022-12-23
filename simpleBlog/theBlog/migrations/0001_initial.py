# Generated by Django 4.1.1 on 2022-11-16 14:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Uncategorized', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField()),
                ('profile_img', models.ImageField(blank=True, null=True, upload_to='images/profile_img')),
                ('link1', models.CharField(blank=True, max_length=255, null=True)),
                ('link2', models.CharField(blank=True, max_length=255, null=True)),
                ('link3', models.CharField(blank=True, max_length=255, null=True)),
                ('link4', models.CharField(blank=True, max_length=255, null=True)),
                ('link5', models.CharField(blank=True, max_length=255, null=True)),
                ('link6', models.CharField(blank=True, max_length=255, null=True)),
                ('link1_name', models.CharField(blank=True, max_length=20, null=True)),
                ('link2_name', models.CharField(blank=True, max_length=20, null=True)),
                ('link3_name', models.CharField(blank=True, max_length=20, null=True)),
                ('link4_name', models.CharField(blank=True, max_length=20, null=True)),
                ('link5_name', models.CharField(blank=True, max_length=20, null=True)),
                ('link6_name', models.CharField(blank=True, max_length=20, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('body', mdeditor.fields.MDTextField(blank=True, null=True)),
                ('post_date', models.DateTimeField(auto_now_add=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
                ('category', models.CharField(default='Uncategorized', max_length=255)),
                ('total_views', models.PositiveIntegerField(default=0)),
                ('is_pin', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(related_name='blog_post', to=settings.AUTH_USER_MODEL)),
                ('read', models.ManyToManyField(default=False, related_name='read', to=settings.AUTH_USER_MODEL)),
                ('unique_views', models.ManyToManyField(related_name='unique_views', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('body', mdeditor.fields.MDTextField(null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='theBlog.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='theBlog.post')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
