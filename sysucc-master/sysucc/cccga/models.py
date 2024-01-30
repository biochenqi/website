from django.db import models


class SampleClinicInfo(models.Model):
    barcode = models.CharField(verbose_name='barcode', max_length=16, unique=True)
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, blank=True)
    nsampleid = models.CharField(verbose_name='normal sample id', max_length=16, blank=True)
    gender = models.CharField(verbose_name='gender', max_length=8, default='NA')
    birth = models.DateField(verbose_name='date_of_birth', null=True, blank=True)
    marital = models.CharField(verbose_name='marital_status', max_length=16, default='NA')
    height = models.CharField(verbose_name='height', max_length=8, default='NA')
    weight = models.CharField(verbose_name='weight', max_length=8, default='NA')
    smoking = models.CharField(verbose_name='smoking', max_length=8, default='NA')
    diagnosis_date = models.DateField(verbose_name='diagnosis_date', null=True, blank=True)
    diagnosis_age = models.CharField(verbose_name='diagnosis_age', max_length=8, default='NA')
    chemo_radio = models.CharField(verbose_name='chemo_radio_before_surgery', max_length=8, default='NA')
    surgery_date = models.DateField(verbose_name='surgery_date', null=True, blank=True)
    detailed_site = models.CharField(verbose_name='detailed_tumor_site', max_length=32, default='NA')
    primary_location = models.CharField(verbose_name='primary_tumor_location', max_length=32, default='NA')
    pathological_grade = models.CharField(verbose_name='pathological_grade', max_length=32, default='NA')
    tumor_length = models.CharField(verbose_name='tumor_length', max_length=8, default='NA')
    tumor_width = models.CharField(verbose_name='tumor_width', max_length=8, default='NA')
    tumor_height = models.CharField(verbose_name='tumor_height', max_length=8, default='NA')
    ajcc_T_stage = models.CharField(verbose_name='ajcc_T_stage', max_length=8, default='NA')
    positive_lymph_node = models.CharField(verbose_name='positive_lymph_node', max_length=8, default='NA')
    total_examined_lymphnode = models.CharField(verbose_name='total_examined_lymphnode', max_length=8, default='NA')
    tumor_depoist = models.CharField(verbose_name='tumor_depoist', max_length=8, default='NA')
    ajcc_N_stage = models.CharField(verbose_name='ajcc_N_stage', max_length=8, default='NA')
    metastasis = models.CharField(verbose_name='metastasis_at_diagnosis', max_length=8, default='NA')
    surgery_stage = models.CharField(verbose_name='surgery_stage', max_length=8, default='NA')
    pathological_stage = models.CharField(verbose_name='pathological_stage', max_length=8, default='NA')
    nerve_invasion = models.CharField(verbose_name='nerve_invasion', max_length=8, default='NA')
    vessel_invasion = models.CharField(verbose_name='vessel_invasion', max_length=8, default='NA')
    distal = models.CharField(verbose_name='distal_margin_positive', max_length=8, default='NA')
    proximal = models.CharField(verbose_name='proximal_margin_positive', max_length=8, default='NA')
    mlh1 = models.CharField(verbose_name='MLH1', max_length=16, default='NA')
    msh2 = models.CharField(verbose_name='MSH2', max_length=16, default='NA')
    msh6 = models.CharField(verbose_name='MSH6', max_length=16, default='NA')
    pms2 = models.CharField(verbose_name='PMS2', max_length=16, default='NA')
    her2 = models.CharField(verbose_name='Her2', max_length=16, default='NA')
    nras = models.CharField(verbose_name='NRAS', max_length=16, default='NA')
    kras = models.CharField(verbose_name='KRAS', max_length=16, default='NA')
    braf = models.CharField(verbose_name='BRAF', max_length=16, default='NA')
    death_date_n = models.DateField(verbose_name='date_of_death_new', null=True, blank=True)
    time_os = models.CharField(verbose_name='time_from_diagnosis_to_death_new', max_length=16, default='NA')
    vital_n = models.CharField(verbose_name='vital_status_new', max_length=16, default='NA')
    mmr = models.CharField(verbose_name='MMR', max_length=16, default='NA')
    vital = models.CharField(verbose_name='vital_status', max_length=8, default='NA')
    cancer_type = models.CharField(verbose_name='CancerType', max_length=16, default='NA')
    os_status = models.CharField(verbose_name='Osstatus', max_length=16, default='NA')
    tmb = models.CharField(verbose_name='TMB', max_length=16, default='NA')
    is_hyper = models.CharField(verbose_name='isHyper', max_length=16, default='NA')
    family_history = models.CharField(verbose_name='crc_family_history', max_length=8, default='NA')
    msi = models.CharField(verbose_name='MSIstatus', max_length=16, default='NA')
    m_value_t = models.CharField(verbose_name='mValue_Tumor', max_length=16, default='NA')
    m_value_n = models.CharField(verbose_name='mValue_Normal', max_length=16, default='NA')
    m_ratio = models.CharField(verbose_name='mRatio', max_length=16, default='NA')
    m_value_tumor_status = models.CharField(verbose_name='mValue_Tumor_Status', max_length=8, default='NA')
    cluster = models.CharField(verbose_name='Cluster', max_length=16, default='NA')

    class Meta:
        verbose_name = verbose_name_plural = 'sample clinic information'

    def __str__(self):
        return self.barcode


class TumorSampleQC(models.Model):
    sample_clinic_info = models.ForeignKey(SampleClinicInfo, on_delete=models.CASCADE, verbose_name='sample clinic information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, unique=True)
    sample_type = models.CharField(verbose_name='sample type', max_length=16)
    read_type = models.CharField(verbose_name='read type', max_length=16)
    lib_type = models.CharField(verbose_name='library type', max_length=16)
    rawsize = models.FloatField(verbose_name='raw base number(G)', default=0.0)
    cleansize = models.FloatField(verbose_name='clean base number(G)', default=0.0)
    duplicate_rate = models.FloatField(verbose_name='duplicate rate(%)', default=0.0)
    mtotal_reads = models.CharField(verbose_name='Total reads number', max_length=64, blank=True)
    mduplicate = models.CharField(verbose_name='Duplicate', max_length=64, blank=True)
    map_reads = models.CharField(verbose_name='Mapped reads', max_length=64, blank=True)
    mrp = models.CharField(verbose_name='Properly mapped reads', max_length=64, blank=True)
    mtdc = models.CharField(verbose_name='With mate mapped to a different chr', max_length=64, blank=True)
    mtdc5 = models.CharField(verbose_name='With mate mapped to a different chr (mapQ>=5)', max_length=64, blank=True)
    bot = models.PositiveIntegerField(verbose_name='bases on target')
    bnt = models.PositiveIntegerField(verbose_name='bases near target')
    esot = models.FloatField(verbose_name='effective sequences on target(Mb)')
    esnt = models.FloatField(verbose_name='effective sequences near target(Mb)')
    esont = models.FloatField(verbose_name='effective sequences on or near target(Mb)')
    foebot = models.FloatField(verbose_name='fraction of effective bases on target(%)')
    foebnt = models.FloatField(verbose_name='fraction of effective bases on or near target(%)')
    foebont = models.FloatField(verbose_name='fraction of effective bases on or near target(%)')
    asdot = models.FloatField(verbose_name='average sequencing depth on target')
    asdnt = models.FloatField(verbose_name='average sequencing depth near target')
    bcot = models.PositiveIntegerField(verbose_name='bases covered on target')
    cotr = models.FloatField(verbose_name='coverage of target region(%)')
    bcnt = models.PositiveIntegerField(verbose_name='bases covered near target')
    cofr = models.FloatField(verbose_name='coverage of flanking region(%)')
    fotcwal4 = models.FloatField(verbose_name='fraction of target covered with at least 4x(%)')
    fotcwal10 = models.FloatField(verbose_name='fraction of target covered with at least 10x(%)')
    fotcwal30 = models.FloatField(verbose_name='fraction of target covered with at least 30x(%)')
    fotcwal100 = models.FloatField(verbose_name='fraction of target covered with at least 100x(%)')
    fofrcwal4 = models.FloatField(verbose_name='fraction of flanking region covered with at least 4x(%)')
    fofrcwal10 = models.FloatField(verbose_name='fraction of flanking region covered with at least 10x(%)')
    fofrcwal30 = models.FloatField(verbose_name='fraction of flanking region covered with at least 30x(%)')
    fofrcwal100 = models.FloatField(verbose_name='fraction of flanking region covered with at least 100x(%)')

    class Meta:
        verbose_name = verbose_name_plural = 'tumor sample qc'

    def __str__(self):
        return self.tsampleid


class NormalSampleQC(models.Model):
    sample_clinic_info = models.ForeignKey(SampleClinicInfo, on_delete=models.CASCADE, verbose_name='sample clinic information')
    nsampleid = models.CharField(verbose_name='normal sample id', max_length=16, unique=True)
    sample_type = models.CharField(verbose_name='sample type', max_length=16)
    read_type = models.CharField(verbose_name='read type', max_length=16)
    lib_type = models.CharField(verbose_name='library type', max_length=16)
    rawsize = models.FloatField(verbose_name='raw base number(G)', default=0.0)
    cleansize = models.FloatField(verbose_name='clean base number(G)', default=0.0)
    duplicate_rate = models.FloatField(verbose_name='duplicate rate(%)', default=0.0)
    mtotal_reads = models.CharField(verbose_name='Total reads number', max_length=64, blank=True)
    mduplicate = models.CharField(verbose_name='Duplicate', max_length=64, blank=True)
    map_reads = models.CharField(verbose_name='Mapped reads', max_length=64, blank=True)
    mrp = models.CharField(verbose_name='Properly mapped reads', max_length=64, blank=True)
    mtdc = models.CharField(verbose_name='With mate mapped to a different chr', max_length=64, blank=True)
    mtdc5 = models.CharField(verbose_name='With mate mapped to a different chr (mapQ>=5)', max_length=64, blank=True)
    bot = models.PositiveIntegerField(verbose_name='bases on target')
    bnt = models.PositiveIntegerField(verbose_name='bases near target')
    esot = models.FloatField(verbose_name='effective sequences on target(Mb)')
    esnt = models.FloatField(verbose_name='effective sequences near target(Mb)')
    esont = models.FloatField(verbose_name='effective sequences on or near target(Mb)')
    foebot = models.FloatField(verbose_name='fraction of effective bases on target(%)')
    foebnt = models.FloatField(verbose_name='fraction of effective bases on or near target(%)')
    foebont = models.FloatField(verbose_name='fraction of effective bases on or near target(%)')
    asdot = models.FloatField(verbose_name='average sequencing depth on target')
    asdnt = models.FloatField(verbose_name='average sequencing depth near target')
    bcot = models.PositiveIntegerField(verbose_name='bases covered on target')
    cotr = models.FloatField(verbose_name='coverage of target region(%)')
    bcnt = models.PositiveIntegerField(verbose_name='bases covered near target')
    cofr = models.FloatField(verbose_name='coverage of flanking region(%)')
    fotcwal4 = models.FloatField(verbose_name='fraction of target covered with at least 4x(%)')
    fotcwal10 = models.FloatField(verbose_name='fraction of target covered with at least 10x(%)')
    fotcwal30 = models.FloatField(verbose_name='fraction of target covered with at least 30x(%)')
    fotcwal100 = models.FloatField(verbose_name='fraction of target covered with at least 100x(%)')
    fofrcwal4 = models.FloatField(verbose_name='fraction of flanking region covered with at least 4x(%)')
    fofrcwal10 = models.FloatField(verbose_name='fraction of flanking region covered with at least 10x(%)')
    fofrcwal30 = models.FloatField(verbose_name='fraction of flanking region covered with at least 30x(%)')
    fofrcwal100 = models.FloatField(verbose_name='fraction of flanking region covered with at least 100x(%)')

    class Meta:
        verbose_name = verbose_name_plural = 'normal sample qc'

    def __str__(self):
        return self.nsampleid


class SnvRecord(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol', blank=True)
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)
    chromos = models.CharField(max_length=8, verbose_name='Chromosome', blank=True)
    spo = models.CharField(max_length=32, verbose_name='Start_position', blank=True)
    epo = models.CharField(max_length=32, verbose_name='End_Position', blank=True)
    vari_classification = models.CharField(max_length=32, verbose_name='Variant_Classification', blank=True)
    vari_type = models.CharField(max_length=32, verbose_name='Variant_Type', blank=True)
    ref = models.CharField(max_length=32, verbose_name='Reference_Allele', blank=True)
    tum1 = models.CharField(max_length=32, verbose_name='Tumor_Seq_Allele1', blank=True)
    tum2 = models.CharField(max_length=32, verbose_name='Tumor_Seq_Allele2', blank=True)
    dbsnp = models.CharField(max_length=32, verbose_name='dbSNP_RS', blank=True)
    tumor_sampleid = models.CharField(max_length=32, verbose_name='Tumor_Sample_Barcode', blank=True)
    normal_sampleid = models.CharField(max_length=32, verbose_name='Matched_Norm_Sample_Barcode', blank=True)
    mutation_status = models.CharField(max_length=32, verbose_name='Mutation_Status', blank=True)
    seq_source = models.CharField(max_length=16, verbose_name='Sequence_Source', blank=True)
    sequencer = models.CharField(max_length=16, verbose_name='Sequencer', blank=True)
    aachange = models.TextField(verbose_name='AAchange', blank=True)
    description = models.TextField(verbose_name='Description', blank=True)
    cytoband = models.CharField(max_length=16, verbose_name='cytoBand', blank=True)
    esp6500siv2_all = models.CharField(max_length=16, verbose_name='esp6500siv2_all', blank=True)
    oct_all = models.CharField(max_length=16, verbose_name='1000g2014oct_all', blank=True)
    oct_afr = models.CharField(max_length=16, verbose_name='1000g2014oct_afr', blank=True)
    oct_eas = models.CharField(max_length=16, verbose_name='1000g2014oct_eas', blank=True)
    oct_eur = models.CharField(max_length=16, verbose_name='1000g2014oct_eur', blank=True)
    cosmic86 = models.TextField(verbose_name='cosmic86', blank=True)
    clinvar = models.TextField(verbose_name='clinvar_20180603', blank=True)
    exac_all = models.CharField(max_length=16, verbose_name='ExAC_ALL', blank=True)
    exac_afr = models.CharField(max_length=16, verbose_name='ExAC_AFR', blank=True)
    exac_amr = models.CharField(max_length=16, verbose_name='ExAC_AMR', blank=True)
    exac_eas = models.CharField(max_length=16, verbose_name='ExAC_EAS', blank=True)
    exac_fin = models.CharField(max_length=16, verbose_name='ExAC_FIN', blank=True)
    exac_nfe = models.CharField(max_length=16, verbose_name='ExAC_NFE', blank=True)
    exac_oth = models.CharField(max_length=16, verbose_name='ExAC_OTH', blank=True)
    exac_sas = models.CharField(max_length=16, verbose_name='ExAC_SAS', blank=True)
    varscan_t_vaf = models.CharField(max_length=16, verbose_name='varscan_t_vaf', blank=True)
    mutect2_t_vaf = models.CharField(max_length=16, verbose_name='mutect2_t_vaf', blank=True)
    sention_t_vaf = models.CharField(max_length=16, verbose_name='sention_t_vaf', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'somatic SNV Record'

    def __str__(self):
        return '-'.join([self.tumor_sampleid, self.symbol])


class VepSnvRecord(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol', blank=True)
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)
    chromos = models.CharField(max_length=8, verbose_name='Chromosome', blank=True)
    spo = models.CharField(max_length=32, verbose_name='Start_position', blank=True)
    epo = models.CharField(max_length=32, verbose_name='End_Position', blank=True)
    vari_classification = models.CharField(max_length=32, verbose_name='Variant_Classification', blank=True)
    vari_type = models.CharField(max_length=32, verbose_name='Variant_Type', blank=True)
    ref = models.TextField(verbose_name='Reference_Allele', blank=True)
    tum1 = models.TextField(verbose_name='Tumor_Seq_Allele1', blank=True)
    tum2 = models.TextField(verbose_name='Tumor_Seq_Allele2', blank=True)
    dbsnp = models.CharField(max_length=32, verbose_name='dbSNP_RS', blank=True)
    tumor_sampleid = models.CharField(max_length=32, verbose_name='Tumor_Sample_Barcode', blank=True)
    normal_sampleid = models.CharField(max_length=32, verbose_name='Matched_Norm_Sample_Barcode', blank=True)
    hgvsc = models.TextField(verbose_name='HGVSc', blank=True)
    hgvsp = models.TextField(verbose_name='HGVSp', blank=True)
    hgvsp_short = models.TextField(verbose_name='HGVSp_Short', blank=True)
    trans_id = models.CharField(max_length=32, verbose_name='Transcript_ID', blank=True)
    exon_num = models.CharField(max_length=16, verbose_name='Exon_Number', blank=True)
    t_depth = models.CharField(max_length=16, verbose_name='t_depth', blank=True)
    t_ref_count = models.CharField(max_length=16, verbose_name='t_ref_count', blank=True)
    t_alt_count = models.CharField(max_length=16, verbose_name='t_alt_count', blank=True)
    n_depth = models.CharField(max_length=16, verbose_name='n_depth', blank=True)
    n_ref_count = models.CharField(max_length=16, verbose_name='n_ref_count', blank=True)
    n_alt_count = models.CharField(max_length=16, verbose_name='n_alt_count', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'somatic SNV Record by VEP'

    def __str__(self):
        return '-'.join([self.tumor_sampleid, self.symbol])


class CnvRecord(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, verbose_name='tumor sample information')
    tumor_sampleid = models.CharField(max_length=32, verbose_name='Tumor_Sample_Barcode', blank=True)
    normal_sampleid = models.CharField(max_length=32, verbose_name='Matched_Norm_Sample_Barcode', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'somatic CNV Record'

    def __str__(self):
        return self.tumor_sampleid


class VariationClassification(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, unique=True)
    missense = models.PositiveIntegerField(verbose_name='Missense Mutation')
    nonsense = models.PositiveIntegerField(verbose_name='Nonsense Mutation')
    splice = models.PositiveIntegerField(verbose_name='Splice Site')
    fsi = models.PositiveIntegerField(verbose_name='Frame Shift Ins')
    fsd = models.PositiveIntegerField(verbose_name='Frame Shift Del')
    ifi = models.PositiveIntegerField(verbose_name='In Frame Ins')
    ifd = models.PositiveIntegerField(verbose_name='In Frame Del')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    missense_rate = models.FloatField(verbose_name='Missense Mutation rate', default=0.0)
    nonsense_rate = models.FloatField(verbose_name='Nonsense Mutation rate', default=0.0)
    splice_rate = models.FloatField(verbose_name='Splice Site rate', default=0.0)
    fsi_rate = models.FloatField(verbose_name='Frame Shift Ins rate', default=0.0)
    fsd_rate = models.FloatField(verbose_name='Frame Shift Del rate', default=0.0)
    ifi_rate = models.FloatField(verbose_name='In Frame Ins rate', default=0.0)
    ifd_rate = models.FloatField(verbose_name='In Frame Del rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Variation Classification per tumor sample'
        ordering = ['-total']

    def __str__(self):
        return self.tsampleid


class VariationClassificationTotalBar(models.Model):
    missense = models.PositiveIntegerField(verbose_name='Missense Mutation')
    nonsense = models.PositiveIntegerField(verbose_name='Nonsense Mutation')
    splice = models.PositiveIntegerField(verbose_name='Splice Site')
    fsi = models.PositiveIntegerField(verbose_name='Frame Shift Ins')
    fsd = models.PositiveIntegerField(verbose_name='Frame Shift Del')
    ifi = models.PositiveIntegerField(verbose_name='In Frame Ins')
    ifd = models.PositiveIntegerField(verbose_name='In Frame Del')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    missense_rate = models.FloatField(verbose_name='Missense Mutation rate', default=0.0)
    nonsense_rate = models.FloatField(verbose_name='Nonsense Mutation rate', default=0.0)
    splice_rate = models.FloatField(verbose_name='Splice Site rate', default=0.0)
    fsi_rate = models.FloatField(verbose_name='Frame Shift Ins rate', default=0.0)
    fsd_rate = models.FloatField(verbose_name='Frame Shift Del rate', default=0.0)
    ifi_rate = models.FloatField(verbose_name='In Frame Ins rate', default=0.0)
    ifd_rate = models.FloatField(verbose_name='In Frame Del rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Variation Classification Total Bar Plot'


class VariationClassificationCategoryPlot(models.Model):
    category = models.CharField(verbose_name='tumor sample category', max_length=32, unique=True)
    missense = models.PositiveIntegerField(verbose_name='Missense Mutation')
    nonsense = models.PositiveIntegerField(verbose_name='Nonsense Mutation')
    splice = models.PositiveIntegerField(verbose_name='Splice Site')
    fsi = models.PositiveIntegerField(verbose_name='Frame Shift Ins')
    fsd = models.PositiveIntegerField(verbose_name='Frame Shift Del')
    ifi = models.PositiveIntegerField(verbose_name='In Frame Ins')
    ifd = models.PositiveIntegerField(verbose_name='In Frame Del')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    missense_rate = models.FloatField(verbose_name='Missense Mutation rate', default=0.0)
    nonsense_rate = models.FloatField(verbose_name='Nonsense Mutation rate', default=0.0)
    splice_rate = models.FloatField(verbose_name='Splice Site rate', default=0.0)
    fsi_rate = models.FloatField(verbose_name='Frame Shift Ins rate', default=0.0)
    fsd_rate = models.FloatField(verbose_name='Frame Shift Del rate', default=0.0)
    ifi_rate = models.FloatField(verbose_name='In Frame Ins rate', default=0.0)
    ifd_rate = models.FloatField(verbose_name='In Frame Del rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Variation Classification Category'

    def __str__(self):
        return self.category


class VariantType(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, unique=True)
    snp = models.PositiveIntegerField(verbose_name='SNP')
    ins = models.PositiveIntegerField(verbose_name='INS')
    dels = models.PositiveIntegerField(verbose_name='DEL')

    class Meta:
        verbose_name = verbose_name_plural = 'Variant Type per tumor sample'

    def __str__(self):
        return self.tsampleid


class VariantTypeTotalBar(models.Model):
    snp = models.PositiveIntegerField(verbose_name='SNP')
    ins = models.PositiveIntegerField(verbose_name='INS')
    dels = models.PositiveIntegerField(verbose_name='DEL')

    class Meta:
        verbose_name = verbose_name_plural = 'Variant Type Total Bar Plot'


class VariantTypeCategoryPlot(models.Model):
    category = models.CharField(verbose_name='tumor sample category', max_length=32, unique=True)
    tsample_num = models.PositiveIntegerField(verbose_name='tumor sample number', default=0)
    snp = models.PositiveIntegerField(verbose_name='SNP')
    ins = models.PositiveIntegerField(verbose_name='INS')
    dels = models.PositiveIntegerField(verbose_name='DEL')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    snp_rate = models.FloatField(verbose_name='snp rate', default=0.0)
    ins_rate = models.FloatField(verbose_name='ins rate', default=0.0)
    del_rate = models.FloatField(verbose_name='del rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Variant Type Category'

    def __str__(self):
        return self.category


class SnvClass(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, unique=True)
    t2g = models.PositiveIntegerField(verbose_name='T2G')
    t2a = models.PositiveIntegerField(verbose_name='T2A')
    t2c = models.PositiveIntegerField(verbose_name='T2C')
    c2t = models.PositiveIntegerField(verbose_name='C2T')
    c2g = models.PositiveIntegerField(verbose_name='C2G')
    c2a = models.PositiveIntegerField(verbose_name='C2A')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    t2g_rate = models.FloatField(verbose_name='T2G rate', default=0.0)
    t2a_rate = models.FloatField(verbose_name='T2A rate', default=0.0)
    t2c_rate = models.FloatField(verbose_name='T2C rate', default=0.0)
    c2t_rate = models.FloatField(verbose_name='C2T rate', default=0.0)
    c2g_rate = models.FloatField(verbose_name='C2G rate', default=0.0)
    c2a_rate = models.FloatField(verbose_name='C2A rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Snv Class per tumor sample'

    def __str__(self):
        return self.tsampleid


class SnvClassTotalBar(models.Model):
    t2g = models.PositiveIntegerField(verbose_name='T2G')
    t2a = models.PositiveIntegerField(verbose_name='T2A')
    t2c = models.PositiveIntegerField(verbose_name='T2C')
    c2t = models.PositiveIntegerField(verbose_name='C2T')
    c2g = models.PositiveIntegerField(verbose_name='C2G')
    c2a = models.PositiveIntegerField(verbose_name='C2A')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    t2g_rate = models.FloatField(verbose_name='T2G rate', default=0.0)
    t2a_rate = models.FloatField(verbose_name='T2A rate', default=0.0)
    t2c_rate = models.FloatField(verbose_name='T2C rate', default=0.0)
    c2t_rate = models.FloatField(verbose_name='C2T rate', default=0.0)
    c2g_rate = models.FloatField(verbose_name='C2G rate', default=0.0)
    c2a_rate = models.FloatField(verbose_name='C2A rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Snv Class Total Bar Plot'


class SnvClassCategoryPlot(models.Model):
    category = models.CharField(verbose_name='tumor sample category', max_length=32, unique=True)
    t2g = models.PositiveIntegerField(verbose_name='T2G')
    t2a = models.PositiveIntegerField(verbose_name='T2A')
    t2c = models.PositiveIntegerField(verbose_name='T2C')
    c2t = models.PositiveIntegerField(verbose_name='C2T')
    c2g = models.PositiveIntegerField(verbose_name='C2G')
    c2a = models.PositiveIntegerField(verbose_name='C2A')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    t2g_rate = models.FloatField(verbose_name='T2G rate', default=0.0)
    t2a_rate = models.FloatField(verbose_name='T2A rate', default=0.0)
    t2c_rate = models.FloatField(verbose_name='T2C rate', default=0.0)
    c2t_rate = models.FloatField(verbose_name='C2T rate', default=0.0)
    c2g_rate = models.FloatField(verbose_name='C2G rate', default=0.0)
    c2a_rate = models.FloatField(verbose_name='C2A rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Snv Class Category'

    def __str__(self):
        return self.category


class MutatedGenes(models.Model):
    tsampleinfo = models.ForeignKey(TumorSampleQC, on_delete=models.CASCADE, null=True, verbose_name='tumor sample information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16)
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol')
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'Mutated Genes'
        unique_together = (('tsampleid', 'symbol'),)

    def __str__(self):
        return '-'.join([self.tsampleid, self.symbol])


class GeneVariationClassification(models.Model):
    mutgeneinfo = models.ForeignKey(MutatedGenes, on_delete=models.CASCADE, null=True, verbose_name='mutated gene information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16)
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol')
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)
    missense = models.PositiveIntegerField(verbose_name='Missense Mutation')
    nonsense = models.PositiveIntegerField(verbose_name='Nonsense Mutation')
    splice = models.PositiveIntegerField(verbose_name='Splice Site')
    fsi = models.PositiveIntegerField(verbose_name='Frame Shift Ins')
    fsd = models.PositiveIntegerField(verbose_name='Frame Shift Del')
    ifi = models.PositiveIntegerField(verbose_name='In Frame Ins')
    ifd = models.PositiveIntegerField(verbose_name='In Frame Del')
    maf = models.FloatField(verbose_name='Alter_Frequency', default=0.0)
    aachange = models.TextField(verbose_name='AAchange', blank=True)

    class Meta:
        verbose_name = verbose_name_plural = 'Gene Variation Classification'
        # unique_together = (('tsampleid', 'symbol'),)

    def __str__(self):
        return '-'.join([self.tsampleid, self.symbol])


class GeneVariantType(models.Model):
    mutgeneinfo = models.ForeignKey(MutatedGenes, on_delete=models.CASCADE, null=True, verbose_name='mutated gene information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16)
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol')
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)
    snp = models.PositiveIntegerField(verbose_name='SNP')
    ins = models.PositiveIntegerField(verbose_name='INS')
    dels = models.PositiveIntegerField(verbose_name='DEL')

    class Meta:
        verbose_name = verbose_name_plural = 'Gene Variant Type'
        unique_together = (('tsampleid', 'symbol'),)

    def __str__(self):
        return '-'.join([self.tsampleid, self.symbol])


class GeneSnvClass(models.Model):
    mutgeneinfo = models.ForeignKey(MutatedGenes, on_delete=models.CASCADE, null=True, verbose_name='mutated gene information')
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16)
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol')
    gene_id = models.CharField(max_length=32, verbose_name='Entrez_Gene_Id', blank=True)
    t2g = models.PositiveIntegerField(verbose_name='T2G')
    t2a = models.PositiveIntegerField(verbose_name='T2A')
    t2c = models.PositiveIntegerField(verbose_name='T2C')
    c2t = models.PositiveIntegerField(verbose_name='C2T')
    c2g = models.PositiveIntegerField(verbose_name='C2G')
    c2a = models.PositiveIntegerField(verbose_name='C2A')

    class Meta:
        verbose_name = verbose_name_plural = 'Gene Snv Class'
        unique_together = (('tsampleid', 'symbol'),)

    def __str__(self):
        return '-'.join([self.tsampleid, self.symbol])


class SortedGeneVariationClassification(models.Model):
    symbol = models.CharField(max_length=32, verbose_name='Hugo_Symbol', unique=True)
    tsample_num = models.PositiveIntegerField(verbose_name='tumor sample number', default=0)
    tsample_num_rate = models.FloatField(verbose_name='tumor sample rate', default=0.0)
    rank = models.PositiveIntegerField(verbose_name='rank', default=0)
    missense = models.PositiveIntegerField(verbose_name='Missense Mutation')
    nonsense = models.PositiveIntegerField(verbose_name='Nonsense Mutation')
    splice = models.PositiveIntegerField(verbose_name='Splice Site')
    fsi = models.PositiveIntegerField(verbose_name='Frame Shift Ins')
    fsd = models.PositiveIntegerField(verbose_name='Frame Shift Del')
    ifi = models.PositiveIntegerField(verbose_name='In Frame Ins')
    ifd = models.PositiveIntegerField(verbose_name='In Frame Del')
    total = models.PositiveIntegerField(verbose_name='total', default=0)
    missense_rate = models.FloatField(verbose_name='Missense Mutation rate', default=0.0)
    nonsense_rate = models.FloatField(verbose_name='Nonsense Mutation rate', default=0.0)
    splice_rate = models.FloatField(verbose_name='Splice Site rate', default=0.0)
    fsi_rate = models.FloatField(verbose_name='Frame Shift Ins rate', default=0.0)
    fsd_rate = models.FloatField(verbose_name='Frame Shift Del rate', default=0.0)
    ifi_rate = models.FloatField(verbose_name='In Frame Ins rate', default=0.0)
    ifd_rate = models.FloatField(verbose_name='In Frame Del rate', default=0.0)

    class Meta:
        verbose_name = verbose_name_plural = 'Sorted Gene Variation Classification'
        ordering = ['rank']

    def __str__(self):
        return self.symbol


class Oncoplot(models.Model):
    tsampleid = models.CharField(verbose_name='tumor sample id', max_length=16, unique=True)
    rank = models.PositiveIntegerField(verbose_name='rank', default=0)
    gene_list = models.TextField(verbose_name='gene list')
    type_list = models.TextField(verbose_name='varclass type list')
    missense_list = models.TextField(verbose_name='Missense Mutation', default='')
    nonsense_list = models.TextField(verbose_name='Nonsense Mutation', default='')
    splice_list = models.TextField(verbose_name='Splice Site', default='')
    fsi_list = models.TextField(verbose_name='Frame Shift Ins', default='')
    fsd_list = models.TextField(verbose_name='Frame Shift Del', default='')
    ifi_list = models.TextField(verbose_name='In Frame Ins', default='')
    ifd_list = models.TextField(verbose_name='In Frame Del', default='')
    mh_list = models.TextField(verbose_name='In Frame Del', default='')

    class Meta:
        verbose_name = verbose_name_plural = 'Oncoplot'
        ordering = ['rank']

    def __str__(self):
        return self.tsampleid


class OverViewStatsPlot(models.Model):
    sex_list = models.TextField(verbose_name='sex list')
    sex_num_list = models.TextField(verbose_name='sex number list')
    age_list = models.TextField(verbose_name='age list')
    age_num_list = models.TextField(verbose_name='age number list')
    os_sampleid_list = models.TextField(verbose_name='os sampleid list', default='')
    os_time_list = models.TextField(verbose_name='os time list', default='')
    os_number_list = models.TextField(verbose_name='os number list', default='')
    os_probability_list = models.TextField(verbose_name='os probability list', default='')
    os_status_list = models.TextField(verbose_name='os status list', default='')
    pathostage_list = models.TextField(verbose_name='pathological stage list')
    pathostage_num_list = models.TextField(verbose_name='pathological stage number list')
    patients_num = models.PositiveIntegerField(verbose_name='patients number')
    tumor_sample_num = models.PositiveIntegerField(verbose_name='tumor sample number')
    mcrc_primary_num = models.PositiveIntegerField(verbose_name='mcrc primary number')
    mcrc_metastasis_num = models.PositiveIntegerField(verbose_name='mcrc metastasis number')

    class Meta:
        verbose_name = verbose_name_plural = 'OverView Stats Plot'


class ProteinDomainsDB(models.Model):
    hgnc = models.CharField(max_length=32, verbose_name='HGNC')
    refseq_id = models.CharField(max_length=32, verbose_name='refseq_ID')
    protein_id = models.CharField(max_length=32, verbose_name='protein_ID')
    aa_length = models.PositiveIntegerField(verbose_name='aa_length')
    start = models.PositiveIntegerField(verbose_name='Start')
    end = models.PositiveIntegerField(verbose_name='End')
    domain_source = models.CharField(max_length=32, verbose_name='domain_source')
    label = models.CharField(max_length=256, verbose_name='Label')
    domain_anno = models.TextField(verbose_name='domain_anno')
    pfam = models.TextField(verbose_name='pfam')
    description = models.TextField(verbose_name='Description')

    class Meta:
        verbose_name = verbose_name_plural = 'Protein Domains Database'

    def __str__(self):
        return self.hgnc


class Hgnc2PfamDB(models.Model):
    hgnc = models.CharField(max_length=32, verbose_name='HGNC')
    symbol = models.CharField(max_length=32, verbose_name='symbol')
    uniprot = models.CharField(max_length=32, verbose_name='uniprot')
    aa_length = models.PositiveIntegerField(verbose_name='aa_length')
    start = models.PositiveIntegerField(verbose_name='Start')
    end = models.PositiveIntegerField(verbose_name='End')
    hmm_acc = models.CharField(max_length=32, verbose_name='hmm_acc')
    hmm_name = models.CharField(max_length=32, verbose_name='hmm_name')
    p_type = models.CharField(max_length=32, verbose_name='p_type')

    class Meta:
        verbose_name = verbose_name_plural = 'Hgnc to Pfam Database'

    def __str__(self):
        return self.hgnc
