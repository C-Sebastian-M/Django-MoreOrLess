# Generated by Django 3.2.6 on 2021-09-20 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metas', '0010_auto_20210920_1048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='amountmetas',
            old_name='meta_id',
            new_name='meta',
        ),
    ]
