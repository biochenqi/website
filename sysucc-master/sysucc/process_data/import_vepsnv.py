import csv
import sys

from cccga.models import VepSnvRecord, TumorSampleQC, SampleClinicInfo


def import_snv(row):
    try:
        sampleinfo = SampleClinicInfo.objects.get(barcode=row['tumor_sampleid'])
        tsampleid = sampleinfo.tsampleid
        tsampleinfo = TumorSampleQC.objects.get(tsampleid=tsampleid)
    except Exception:
        print('sampleinfo or tsampleinfo missing: <%s>.' % row['tumor_sampleid'])
        return
    VepSnvRecord.objects.get_or_create(
        tsampleinfo=tsampleinfo,
        symbol=row['symbol'],
        gene_id=row['gene_id'],
        chromos=row['chromos'],
        spo=row['spo'],
        epo=row['epo'],
        vari_classification=row['vari_classification'],
        vari_type=row['vari_type'],
        ref=row['ref'],
        tum1=row['tum1'],
        tum2=row['tum2'],
        dbsnp=row['dbsnp'],
        tumor_sampleid=row['tumor_sampleid'],
        normal_sampleid=row['normal_sampleid'],
        hgvsc=row['hgvsc'],
        hgvsp=row['hgvsp'],
        hgvsp_short=row['hgvsp_short'],
        trans_id=row['trans_id'],
        exon_num=row['exon_num'],
        t_depth=row['t_depth'],
        t_ref_count=row['t_ref_count'],
        t_alt_count=row['t_alt_count'],
        n_depth=row['n_depth'],
        n_ref_count=row['n_ref_count'],
        n_alt_count=row['n_alt_count']
    )


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp, delimiter='\t')
        for i, row in enumerate(reader):
            k = '-'.join([row['Tumor_Sample_Barcode'].strip(), str(i)])
            if d.get(k) is None:
                sd = d[k] = {}
                sd['symbol'] = row['Hugo_Symbol'].strip()
                sd['gene_id'] = row['Entrez_Gene_Id'].strip()
                sd['chromos'] = row['Chromosome'].strip()
                sd['spo'] = row['Start_Position'].strip()
                sd['epo'] = row['End_Position'].strip()
                sd['vari_classification'] = row['Variant_Classification'].strip()
                sd['vari_type'] = row['Variant_Type'].strip()
                sd['ref'] = row['Reference_Allele'].strip()
                sd['tum1'] = row['Tumor_Seq_Allele1'].strip()
                sd['tum2'] = row['Tumor_Seq_Allele2'].strip()
                sd['dbsnp'] = row['dbSNP_RS'].strip()
                sd['tumor_sampleid'] = row['Tumor_Sample_Barcode'].strip()
                sd['normal_sampleid'] = row['Matched_Norm_Sample_Barcode'].strip()
                sd['hgvsc'] = row['HGVSc'].strip()
                sd['hgvsp'] = row['HGVSp'].strip()
                sd['hgvsp_short'] = row['HGVSp_Short'].strip()
                sd['trans_id'] = row['Transcript_ID'].strip()
                sd['exon_num'] = row['Exon_Number'].strip()
                sd['t_depth'] = row['t_depth'].strip()
                sd['t_ref_count'] = row['t_ref_count'].strip()
                sd['t_alt_count'] = row['t_alt_count'].strip()
                sd['n_depth'] = row['n_depth'].strip()
                sd['n_ref_count'] = row['n_ref_count'].strip()
                sd['n_alt_count'] = row['n_alt_count'].strip()
    return d


if __name__ == '__main__':
    tab = sys.argv[1]
