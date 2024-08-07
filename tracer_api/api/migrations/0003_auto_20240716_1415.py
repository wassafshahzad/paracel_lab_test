# Generated by Django 5.0.7 on 2024-07-15 23:05

from django.db import migrations, transaction
from django.apps.registry import Apps

class Migration(migrations.Migration):
    
    def populate_articles(apps: Apps, _):
        article = apps.get_model("api", "ArticleModel")
        data = [
            article(name="Laptop", price=800, sku="LP123"),
            article(name="Monitor", price=200, sku="MT789"),
            article(name="Mouse", price=25, sku="MO456"),
            article(name="Keyboard", price=50, sku="KB012"),
            article(name="Laptop", price=900, sku="LP345"),
            article(name="Headphones", price=100, sku="HP678"),

        ]
        with transaction.atomic():
            article.objects.bulk_create(data)

    def delete_article(apps: Apps, _):
        article = apps.get_model("api", "ArticleModel")
        article.objects.all().delete()

    dependencies = [
        ('api', '0002_auto_20240716_1415'),
    ]

    operations = [
         migrations.RunPython(populate_articles, delete_article),
    ]
