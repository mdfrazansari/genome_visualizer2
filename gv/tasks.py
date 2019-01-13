from celery import shared_task
from django.core import serializers
from .models import PatientGenomeVariation


@shared_task
def pre_process_vcf(queryset):
    print(queryset)
    for obj in serializers.deserialize("json", queryset):
        PatientGenomeVariation.objects.create(patient=obj.object, variation_data="ansari")
    return "preprocessing done"


@shared_task
def create_random_user_accounts(total):
    print("shared task frazzzzzzzzzzzzzzz")
    print(total)
    return 'fraz'


@shared_task
def printtask():
    print("print task................")
    return 'fraz'
