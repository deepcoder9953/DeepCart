# Generated by Django 5.0.7 on 2024-10-10 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_showproduct_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='img',
            field=models.ImageField(default='img.jpg', upload_to='image/'),
        ),
    ]
