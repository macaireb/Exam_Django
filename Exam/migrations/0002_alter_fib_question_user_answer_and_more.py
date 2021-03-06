# Generated by Django 4.0 on 2021-12-30 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Exam', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fib_question',
            name='user_answer',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mc_question',
            name='correct_answer',
            field=models.IntegerField(blank=True, choices=[(1, 'One'), (2, 'Two'), (3, 'Three'), (4, 'Four'), (5, 'Five')], null=True),
        ),
        migrations.AlterField(
            model_name='tf_question',
            name='user_answer',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
