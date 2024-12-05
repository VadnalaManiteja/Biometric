# Generated by Django 5.1.3 on 2024-12-05 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstall', '0002_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('late_by_days', models.PositiveIntegerField(default=0, verbose_name='Late By Days')),
                ('early_going_by_days', models.PositiveIntegerField(default=0, verbose_name='Early Going By Days')),
                ('absent_count', models.PositiveIntegerField(default=0, verbose_name='Absent Count')),
                ('week_off_count', models.PositiveIntegerField(default=0, verbose_name='Week Off Count')),
                ('present_count', models.FloatField(default=0.0, verbose_name='Present Count')),
                ('record_date', models.DateField(auto_now_add=True, verbose_name='Record Date')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='bookstall.employee')),
            ],
        ),
    ]
