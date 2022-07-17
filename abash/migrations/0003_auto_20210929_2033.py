# Generated by Django 3.2.5 on 2021-09-29 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abash', '0002_auto_20210929_1102'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='dining_no',
            new_name='drawing_dining_no',
        ),
        migrations.RemoveField(
            model_name='room',
            name='drawing_no',
        ),
        migrations.AddField(
            model_name='property',
            name='rental_type',
            field=models.CharField(blank=True, choices=[('FF', 'Family Flat'), ('BF', 'Bachelor Flat'), ('FS', 'Family Sublet'), ('BS', 'Bachelor Sublet')], max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='home_type',
            field=models.CharField(blank=True, choices=[('F', 'Furnished'), ('N', 'Non-Furnished')], max_length=1, null=True),
        ),
    ]