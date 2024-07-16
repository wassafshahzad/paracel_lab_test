# Generated by Django 5.0.7 on 2024-07-15 15:50

from django.db import migrations, transaction
from django.apps.registry import Apps



class Migration(migrations.Migration):

    def populate_carriers(apps:Apps, _):

        carrier = apps.get_model("api", "CarrierModel")
        model_list = []


        for x in ("DHL","FEDEX", "UPS", "DPD", "GLS"):
            model_list.append(carrier(name = x))
        
        with transaction.atomic():
            carrier.objects.bulk_create(model_list)


    def delete_all_carriers(apps: Apps, _):
        
        carrier = apps.get_model("api", "CarrierModel")
        carrier.objects.all().delete()



    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_carriers,delete_all_carriers),
    ]

