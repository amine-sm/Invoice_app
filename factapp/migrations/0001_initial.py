# Generated by Django 4.2.4 on 2023-08-24 00:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=132)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=132)),
                ('address', models.CharField(max_length=132)),
                ('sex', models.CharField(choices=[('M', 'masculin'), ('F', 'feminin')], max_length=1)),
                ('age', models.CharField(max_length=12)),
                ('city', models.CharField(max_length=32)),
                ('zip_code', models.CharField(max_length=16)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('saved_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Facture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facture_date', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('last_updated_date', models.DateTimeField(blank=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('facture_type', models.CharField(choices=[('R', 'RECU'), ('P', 'PROFOMAT'), ('F', 'FACTURE')], max_length=1)),
                ('commenter', models.TextField(blank=True, max_length=1000, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='factapp.customer')),
                ('saved_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Facture',
                'verbose_name_plural': 'Factures',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('quantite', models.IntegerField()),
                ('prix_unite', models.DecimalField(decimal_places=2, max_digits=10000)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10000)),
                ('facture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='factapp.facture')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
    ]
