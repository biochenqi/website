import csv
import sys

from cccga.models import Snv, SampleInfo


def import_sampleinfo(row):
    SampleInfo.objects.get_or_create(
        sampleid=row['tumor_sampleid'], samplename=row['tumor_sampleid'], sample_type='FFPE',
        read_type='151+8+8+151', lib_type='WES')


def import_snv(row):
    sampleinfo = SampleInfo.objects.get(sampleid=row['tumor_sampleid'])
    Snv.objects.get_or_create(
        sampleinfo=sampleinfo,
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
        mutation_status=row['mutation_status'],
        seq_source=row['seq_source'],
        sequencer=row['sequencer'],
        aachange=row['aachange'],
        description=row['description'],
        cytoband=row['cytoband'],
        esp6500siv2_all=row['esp6500siv2_all'],
        oct_all=row['oct_all'],
        oct_afr=row['oct_afr'],
        oct_eas=row['oct_eas'],
        oct_eur=row['oct_eur'],
        cosmic86=row['cosmic86'],
        clinvar=row['clinvar'],
        exac_all=row['exac_all'],
        exac_afr=row['exac_afr'],
        exac_amr=row['exac_amr'],
        exac_eas=row['exac_eas'],
        exac_fin=row['exac_fin'],
        exac_nfe=row['exac_nfe'],
        exac_oth=row['exac_oth'],
        exac_sas=row['exac_sas'],
        varscan_t_vaf=row['varscan_t_vaf'],
        mutect2_t_vaf=row['mutect2_t_vaf'],
        sention_t_vaf=row['sention_t_vaf'],
    )


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for i, row in enumerate(reader):
            k = '-'.join([row['Tumor_Sample_Barcode'].strip(), str(i)])
            if d.get(k) is None:
                sd = d[k] = {}
                sd['symbol'] = row['Hugo_Symbol'].strip()
                sd['gene_id'] = row['Entrez_Gene_Id'].strip()
                sd['chromos'] = row['Chromosome'].strip()
                sd['spo'] = row['Start_position'].strip()
                sd['epo'] = row['End_Position'].strip()
                sd['vari_classification'] = row['Variant_Classification'].strip()
                sd['vari_type'] = row['Variant_Type'].strip()
                sd['ref'] = row['Reference_Allele'].strip()
                sd['tum1'] = row['Tumor_Seq_Allele1'].strip()
                sd['tum2'] = row['Tumor_Seq_Allele2'].strip()
                sd['dbsnp'] = row['dbSNP_RS'].strip()
                sd['tumor_sampleid'] = row['Tumor_Sample_Barcode'].strip()
                sd['normal_sampleid'] = row['Matched_Norm_Sample_Barcode'].strip()
                sd['mutation_status'] = row['Mutation_Status'].strip()
                sd['seq_source'] = row['Sequence_Source'].strip()
                sd['sequencer'] = row['Sequencer'].strip()
                sd['aachange'] = row['AAchange'].strip()
                sd['description'] = row['Description'].strip()
                sd['cytoband'] = row['cytoBand'].strip()
                sd['esp6500siv2_all'] = row['esp6500siv2_all'].strip()
                sd['oct_all'] = row['1000g2014oct_all'].strip()
                sd['oct_afr'] = row['1000g2014oct_afr'].strip()
                sd['oct_eas'] = row['1000g2014oct_eas'].strip()
                sd['oct_eur'] = row['1000g2014oct_eur'].strip()
                sd['cosmic86'] = row['cosmic86'].strip()
                sd['clinvar'] = row['clinvar_20180603'].strip()
                sd['exac_all'] = row['ExAC_ALL'].strip()
                sd['exac_afr'] = row['ExAC_AFR'].strip()
                sd['exac_amr'] = row['ExAC_AMR'].strip()
                sd['exac_eas'] = row['ExAC_EAS'].strip()
                sd['exac_fin'] = row['ExAC_FIN'].strip()
                sd['exac_nfe'] = row['ExAC_NFE'].strip()
                sd['exac_oth'] = row['ExAC_OTH'].strip()
                sd['exac_sas'] = row['ExAC_SAS'].strip()
                sd['varscan_t_vaf'] = row['varscan_t_vaf'].strip().replace('%', '')
                sd['mutect2_t_vaf'] = row['mutect2_t_vaf'].strip()
                sd['sention_t_vaf'] = row['sention_t_vaf'].strip()
    return d


if __name__ == '__main__':
    tab = sys.argv[1]
