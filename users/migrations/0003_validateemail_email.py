# Generated by Django 4.1.2 on 2023-04-30 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_is_admin_alter_user_is_active_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='validateemail',
            name='email',
            field=models.EmailField(default='Prueba', max_length=254),
            preserve_default=False,
        ),
    ]
