# Generated by Django 3.1.4 on 2021-02-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20201227_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post_category',
            options={'verbose_name': 'Post Category', 'verbose_name_plural': 'Post Category'},
        ),
        migrations.AddField(
            model_name='post',
            name='keyword',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='featured_image',
            field=models.ImageField(default='featured_image/default_image/featured_img_for_post.jpg', upload_to='featured_image'),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(blank=True, to='post.Tag'),
        ),
    ]
