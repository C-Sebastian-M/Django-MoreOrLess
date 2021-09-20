# Generated by Django 3.2.6 on 2021-09-20 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('metas', '0009_auto_20210920_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='amountmetas',
            options={'ordering': ['id'], 'verbose_name': 'AmountMeta', 'verbose_name_plural': 'AmountMetas'},
        ),
        migrations.AddField(
            model_name='amountmetas',
            name='meta_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='metas.metas'),
        ),
    ]
