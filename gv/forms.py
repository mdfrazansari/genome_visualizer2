from django import forms

from .models import Patient, PatientGenomeVariation


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('name', 'disease_type', 'remarks', 'vcf_file')


class PatientGenomeVariationForm(forms.ModelForm):
    class Meta:
        model = PatientGenomeVariation
        fields = ('patient', 'variation_data')
