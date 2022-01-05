# Generated by Django 4.0 on 2022-01-05 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_extension_public'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='callgroupmembership',
            constraint=models.UniqueConstraint(fields=('extension', 'callgroup'), name='unique_callgroup_membership'),
        ),
        migrations.AddConstraint(
            model_name='extension',
            constraint=models.UniqueConstraint(fields=('event', 'number'), name='unique_extension'),
        ),
    ]
