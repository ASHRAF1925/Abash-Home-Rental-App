# Generated by Django 3.2.5 on 2021-10-07 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0011_auto_20211006_2217'),
    ]

    operations = [
        migrations.RenameField(
            model_name='requested_booking',
            old_name='deleted',
            new_name='rejected',
        ),
        migrations.RemoveField(
            model_name='received_booking',
            name='deleted',
        ),
        migrations.CreateModel(
            name='Rented_Property',
            fields=[
                ('property', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='abash.property')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='abash.user_details')),
            ],
        ),
    ]
