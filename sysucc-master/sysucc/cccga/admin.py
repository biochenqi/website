from django.contrib import admin

from .models import (
    ProteinDomainsDB, SampleClinicInfo,
    TumorSampleQC, NormalSampleQC, SnvRecord,
    VariationClassification, VariantType, SnvClass,
    MutatedGenes, GeneVariationClassification,
    GeneVariantType, GeneSnvClass,
    SortedGeneVariationClassification, Oncoplot
)


@admin.register(SampleClinicInfo)
class SampleClinicInfoAdmin(admin.ModelAdmin):
    list_display = (
        'barcode', 'gender', 'diagnosis_date', 'diagnosis_age', 'detailed_site', 'primary_location',
    )


@admin.register(TumorSampleQC)
class TumorSampleQCAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'rawsize', 'cleansize', 'duplicate_rate', 'bot', 'bnt',
    )


@admin.register(NormalSampleQC)
class NormalSampleQCAdmin(admin.ModelAdmin):
    list_display = (
        'nsampleid', 'rawsize', 'cleansize', 'duplicate_rate', 'bot', 'bnt',
    )


@admin.register(SnvRecord)
class SnvRecordAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleinfo', 'symbol', 'chromos', 'spo', 'epo', 'vari_classification', 'vari_type',
        'tumor_sampleid', 'normal_sampleid'
    )
    search_fields = ('symbol', 'tumor_sampleid', 'normal_sampleid')


@admin.register(VariationClassification)
class VariationClassificationAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'missense', 'nonsense', 'splice', 'fsi', 'fsd',
        'ifi', 'ifd'
    )
    search_fields = ('tsampleid',)


@admin.register(VariantType)
class VariantTypeAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'snp', 'ins', 'dels'
    )
    search_fields = ('tsampleid',)


@admin.register(SnvClass)
class SnvClassAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 't2g', 't2a', 't2c', 'c2t', 'c2g', 'c2a'
    )
    search_fields = ('tsampleid',)


@admin.register(MutatedGenes)
class MutatedGenesAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'symbol', 'gene_id'
    )
    search_fields = ('tsampleid', 'symbol')


@admin.register(GeneVariationClassification)
class GeneVariationClassificationAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'symbol', 'gene_id', 'missense', 'nonsense', 'splice', 'fsi', 'fsd',
        'ifi', 'ifd', 'maf', 'show_aachange'
    )
    search_fields = ('tsampleid', 'symbol')

    def show_aachange(self, obj):
        if len(obj.aachange) <= 10:
            return obj.aachange
        return '%s...' % obj.aachange[:10]
    show_aachange.short_description = 'aachange'


@admin.register(GeneVariantType)
class GeneVariantTypeAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'symbol', 'gene_id', 'snp', 'ins', 'dels'
    )
    search_fields = ('tsampleid', 'symbol')


@admin.register(GeneSnvClass)
class GeneSnvClassAdmin(admin.ModelAdmin):
    list_display = (
        'tsampleid', 'symbol', 'gene_id', 't2g', 't2a', 't2c', 'c2t', 'c2g', 'c2a'
    )
    search_fields = ('tsampleid', 'symbol')


@admin.register(SortedGeneVariationClassification)
class SortedGeneVariationClassificationAdmin(admin.ModelAdmin):
    list_display = (
        'symbol', 'tsample_num', 'tsample_num_rate', 'rank', 'missense',
        'nonsense', 'splice', 'fsi', 'fsd',
        'ifi', 'ifd', 'total'
    )
    search_fields = ('symbol', 'rank')


@admin.register(Oncoplot)
class OncoplotAdmin(admin.ModelAdmin):
    list_display = ('tsampleid',)
    search_fields = ('tsampleid',)


@admin.register(ProteinDomainsDB)
class ProteinDomainsDBAdmin(admin.ModelAdmin):
    list_display = (
        'hgnc', 'refseq_id', 'protein_id', 'aa_length', 'start', 'end', 'domain_source'
    )
    search_fields = ('hgnc',)
