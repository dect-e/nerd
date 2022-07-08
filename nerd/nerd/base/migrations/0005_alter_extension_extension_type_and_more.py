# Generated by Django 4.0 on 2022-05-24 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0004_callgroupmembership_unique_callgroup_membership_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extension',
            name='extension_type',
            field=models.CharField(choices=[('sip', 'Sip'), ('dect', 'Dect'), ('callgroup', 'Callgroup'), ('static', 'Static')], default='sip', max_length=255),
        ),
        migrations.AlterField(
            model_name='extension',
            name='number',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='extension',
            name='owner',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
        ),
    ]