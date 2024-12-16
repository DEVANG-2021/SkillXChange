# Generated by Django 4.0.5 on 2024-10-30 19:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_order_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('experience_level', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.TextField(default='N/A'),
        ),
        migrations.AddField(
            model_name='customer',
            name='experience_years',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customer',
            name='facebook',
            field=models.URLField(blank=True, default='N/A'),
        ),
        migrations.AddField(
            model_name='customer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/users/images/'),
        ),
        migrations.AddField(
            model_name='customer',
            name='instagram',
            field=models.URLField(blank=True, default='N/A'),
        ),
        migrations.AddField(
            model_name='customer',
            name='linkedin',
            field=models.URLField(blank=True, default='N/A'),
        ),
        migrations.AddField(
            model_name='customer',
            name='position',
            field=models.CharField(default='N/A', max_length=100),
        ),
        migrations.AddField(
            model_name='customer',
            name='twitter',
            field=models.URLField(blank=True, default='N/A'),
        ),
        migrations.AddField(
            model_name='customer',
            name='skills',
            field=models.ManyToManyField(blank=True, to='store.skill'),
        ),
    ]
