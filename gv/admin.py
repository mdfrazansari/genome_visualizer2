from django.contrib import admin
from .models import Post, Patient, PatientGenomeVariation
from .tasks import pre_process_vcf
from django.core import serializers
from django.shortcuts import redirect
from django.utils.html import format_html


class patientAdmin(admin.ModelAdmin):
    actions = ["run_preprocessing"]
    list_display = [ 'name', 'disease_type', 'remarks', 'creation_date', 'created_by', 'view_variations']
    def run_preprocessing(self, request, queryset):
        print("Pre processing started...")
        print(queryset)
        a = serializers.serialize('json', queryset)
        print(a)
        pre_process_vcf.delay(a)

    run_preprocessing.short_description = "Run Preprocessing"

    def view_variations_action(self, request, queryset):
        print(len(queryset))
        a = serializers.serialize('json', queryset)
        return redirect("/view/" + str(queryset[0].pk))

    def view_variations(self, a):
        print(a.pk)
        return format_html('<select onchange="if (this.value) window.location.href=this.value">\
            <option value="">-----</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
            <option value="{}">{}</option>\
        </select>'
        .format('/view/' + str(a.pk), 'ALL',\
                '/cv4/' + str(a.pk) + '/chrY', 'chrY', \
                '/cv4/' + str(a.pk) + '/chrX', 'chrX', \
                '/cv4/' + str(a.pk) + '/chr22', 'chr22', \
                '/cv4/' + str(a.pk) + '/chr21', 'chr21', \
                '/cv4/' + str(a.pk) + '/chr20', 'chr20', \
                '/cv4/' + str(a.pk) + '/chr19', 'chr19', \
                '/cv4/' + str(a.pk) + '/chr18', 'chr18', \
                '/cv4/' + str(a.pk) + '/chr17', 'chr17', \
                '/cv4/' + str(a.pk) + '/chr16', 'chr16', \
                '/cv4/' + str(a.pk) + '/chr15', 'chr15', \
                '/cv4/' + str(a.pk) + '/chr14', 'chr14', \
                '/cv4/' + str(a.pk) + '/chr13', 'chr13', \
                '/cv4/' + str(a.pk) + '/chr12', 'chr12', \
                '/cv4/' + str(a.pk) + '/chr11', 'chr11', \
                '/cv4/' + str(a.pk) + '/chr10', 'chr10', \
                '/cv4/' + str(a.pk) + '/chr9', 'chr9', \
                '/cv4/' + str(a.pk) + '/chr8', 'chr8', \
                '/cv4/' + str(a.pk) + '/chr7', 'chr7', \
                '/cv4/' + str(a.pk) + '/chr6', 'chr6', \
                '/cv4/' + str(a.pk) + '/chr5', 'chr5', \
                '/cv4/' + str(a.pk) + '/chr4', 'chr4', \
                '/cv4/' + str(a.pk) + '/chr3', 'chr3', \
                '/cv4/' + str(a.pk) + '/chr2', 'chr2', \
                '/cv4/' + str(a.pk) + '/chr1', 'chr1', \
        ))
    view_variations_action.short_description = "View Variations"


admin.site.register(Post)
admin.site.register(Patient, patientAdmin)
admin.site.register(PatientGenomeVariation)
admin.site.site_header = "Genome Visualizer Administration"
