# Generated by Django 3.2.5 on 2021-10-06 16:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0010_alter_requested_booking_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='received_booking',
            name='owner',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='received_booking',
            name='requested_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='abash.user_details'),
        ),
    ]