# Generated by Django 4.0.1 on 2022-01-12 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0005_assignment_delete_scored_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='fib_question',
            name='assignment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Exam.assignment'),
        ),
    ]
