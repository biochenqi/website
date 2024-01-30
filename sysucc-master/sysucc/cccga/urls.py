from django.urls import path

from .views import (
    index, workflow, sampleqc,
    variation, download,
    querygene, query_sample, category,
    sampleinfo_ajax, querygene_vep_ajax,
    sampletab_ajax, sampletab,
    sampleinfo_export, sampleinfo_export_all
)


app_name = 'cccga'
urlpatterns = [
    path('', index, name='index'),
    path('workflow/', workflow, name='analysis_workflow'),
    path('sampleqc/', sampleqc, name='sample_qc'),
    path('sampletab/', sampletab, name='sample_tab'),
    path('ajax/sampletab/', sampletab_ajax, name='sample_table_ajax'),
    path('ajax/sampleinfo/', sampleinfo_ajax, name='sampleinfo_ajax'),
    path('ajax/sampleinfo/export/', sampleinfo_export, name='sampleinfo_export'),
    path('ajax/sampleinfo/exportall/', sampleinfo_export_all, name='sampleinfo_export_all'),
    path('variation/', variation, name='variation'),
    path('category/', category, name='category'),
    path('querygene/', querygene, name='querygene'),
    path('ajax/querygene/', querygene_vep_ajax, name='querygene_ajax'),
    path('querysample/', query_sample, name='query_sample'),
    path('download/', download, name='download')
]
