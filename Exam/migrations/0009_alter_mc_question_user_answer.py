# Generated by Django 4.0.1 on 2022-01-28 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0008_mc_question_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mc_question',
            name='user_answer',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
