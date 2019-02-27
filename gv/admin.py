from django.contrib import admin
from .models import Post, Patient, PatientGenomeVariation
from .tasks import pre_process_vcf
from django.core import serializers
from django.shortcuts import redirect


class patientAdmin(admin.ModelAdmin):
    actions = ["view_variations", "run_preprocessing"]

    def run_preprocessing(self, request, queryset):
        print("Pre processing started...")
        print(queryset)
        a = serializers.serialize('json', queryset)
        print(a)
        pre_process_vcf.delay(a)

    run_preprocessing.short_description = "Run Preprocessing"

    def view_variations(self, request, queryset):
        print(len(queryset))
        a = serializers.serialize('json', queryset)
        return redirect("/view/" + str(queryset[0].pk))

    view_variations.short_description = "View Variations"


admin.site.register(Post)
admin.site.register(Patient, patientAdmin)
admin.site.register(PatientGenomeVariation)
admin.site.site_header = "Genome Visualizer Administration"
