# Generated by Django 3.2.7 on 2021-10-27 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hotel', '0005_rename_guest_booking_author'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-pk',),
            },
        ),
        migrations.AddIndex(
            model_name='bookmark',
            index=models.Index(fields=['hotel', 'user'], name='bookmark_bo_hotel_i_1f087a_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='bookmark',
            unique_together={('hotel', 'user')},
        ),
    ]
