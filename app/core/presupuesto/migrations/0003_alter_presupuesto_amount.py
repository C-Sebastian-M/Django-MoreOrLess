# Generated by Django 3.2.5 on 2021-08-10 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('presupuesto', '0002_alter_presupuesto_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Monto'),
        ),
    ]
