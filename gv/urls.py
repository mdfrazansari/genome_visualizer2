# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 18:07:25 2018

@author: fraz
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/<int:pk>/', views.view_vcf, name='view_vcf'),
    path('getPQArmData', views.getPQArmData, name='getPQArmData'),
    path('getCytoBand/<str:chrom>', views.getCytoBand, name='getCytoBand'),
    path('getVariationData', views.getVariationData, name='getVariationData'),
    path('cv3/<int:pk>/<str:chrom>', views.cv3, name='cv3'),
    path('getPQArmData/<str:chrom>', views.getPQArmDataChrom, name='getPQArmDataChrom'),
    path('getCensusData/<str:chrom>', views.getCensusData, name='getCensusData'),
    path('getVariationAllDetails/<int:pk>/<str:chrom>', views.getVariationAllDetails, name='getVariationAllDetails'),
    path('getGeneData/<str:chrom>', views.getGeneData, name='getGeneData'),
    
    path('cv4/<int:pk>/<str:chrom>', views.cv4, name='cv4'),
    path('getChromList/', views.getChromList, name='getChromList'),
    path('accounts/register/', views.register, name='register'),
    

]