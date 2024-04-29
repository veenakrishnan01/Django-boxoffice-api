# Generated by Django 5.0.2 on 2024-04-14 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boxofficeapi', '0002_movie_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.IntegerField()),
                ('movieName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('seat_row', models.CharField(max_length=10)),
                ('seat_number', models.CharField(max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
