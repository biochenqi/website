import csv
import sys

from cccga.models import TumorSampleQC, NormalSampleQC, SampleClinicInfo


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if d.get(row['Sample']) is None:
                sd = d[row['Sample']] = {}
                sd['Sample'] = row['Sample']
                sd['rawsize'] = float(row['Raw'])
                sd['cleansize'] = float(row['Clean'])
                sd['duplicate_rate'] = float(row['Dup%'])
                sd['bot'] = int(row['Bases_on_target'].replace(',', ''))
                sd['bnt'] = int(row['Bases_near_target'].replace(',', ''))
                sd['esot'] = float(row['Effective_sequences_on_target(Mb)'])
                sd['esnt'] = float(row['Effective_sequences_near_target(Mb)'])
                sd['esont'] = float(row['Effective_sequences_on_or_near_targe(Mb)'])
                sd['foebot'] = float(row['Fraction_of_effective_bases_on_target'].replace('%', ''))
                sd['foebnt'] = float(row['Fraction_of_effective_bases_near_target'].replace('%', ''))
                sd['foebont'] = float(row['Fraction_of_effective_bases_on_or_near_target'].replace('%', ''))
                sd['asdot'] = float(row['Average_sequencing_depth_on_target'])
                sd['asdnt'] = float(row['Average_sequencing_depth_near_target'])
                sd['bcot'] = int(row['Bases_covered_on_target'].replace(',', ''))
                sd['cotr'] = float(row['Coverage_of_target_region'].replace('%', ''))
                sd['bcnt'] = int(row['Bases_covered_near_target'].replace(',', ''))
                sd['cofr'] = float(row['Coverage_of_flanking_region'].replace('%', ''))
                sd['fotcwal4'] = float(row['Fraction_of_target_covered_with_at_least_4x'].replace('%', ''))
                sd['fotcwal10'] = float(row['Fraction_of_target_covered_with_at_least_10x'].replace('%', ''))
                sd['fotcwal30'] = float(row['Fraction_of_target_covered_with_at_least_30x'].replace('%', ''))
                sd['fotcwal100'] = float(row['Fraction_of_target_covered_with_at_least_100x'].replace('%', ''))
                sd['fofrcwal4'] = float(row['Fraction_of_flanking_region_covered_with_at_least_4x'].replace('%', ''))
                sd['fofrcwal10'] = float(row['Fraction_of_flanking_region_covered_with_at_least_10x'].replace('%', ''))
                sd['fofrcwal30'] = float(row['Fraction_of_flanking_region_covered_with_at_least_30x'].replace('%', ''))
                sd['fofrcwal100'] = float(row['Fraction_of_flanking_region_covered_with_at_least_100x'].replace('%', ''))
    return d


def import_tsampleqc(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'T':
        return
    barcode = '%s_NT' % sid.split('_')[0]
    sample_clinic_info = SampleClinicInfo.objects.get(barcode=barcode)
    TumorSampleQC.objects.get_or_create(
        sample_clinic_info=sample_clinic_info, tsampleid=sid, sample_type='FFPE', read_type='151+8+8+151', lib_type='WES',
        rawsize=row['rawsize'], cleansize=row['cleansize'],
        duplicate_rate=row['duplicate_rate'], bot=row['bot'], bnt=row['bnt'],
        esot=row['esot'], esnt=row['esnt'], esont=row['esont'],
        foebot=row['foebot'], foebnt=row['foebnt'], foebont=row['foebont'],
        asdot=row['asdot'], asdnt=row['asdnt'], bcot=row['bcot'],
        cotr=row['cotr'], bcnt=row['bcnt'], cofr=row['cofr'],
        fotcwal4=row['fotcwal4'], fotcwal10=row['fotcwal10'], fotcwal30=row['fotcwal30'],
        fotcwal100=row['fotcwal100'], fofrcwal4=row['fofrcwal4'], fofrcwal10=row['fofrcwal10'],
        fofrcwal30=row['fofrcwal30'], fofrcwal100=row['fofrcwal100'])


def import_nsampleqc(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'N':
        return
    barcode = '%s_NT' % sid.split('_')[0]
    sample_clinic_info = SampleClinicInfo.objects.get(barcode=barcode)
    NormalSampleQC.objects.get_or_create(
        sample_clinic_info=sample_clinic_info, nsampleid=sid, sample_type='FFPE', read_type='151+8+8+151', lib_type='WES',
        rawsize=row['rawsize'], cleansize=row['cleansize'],
        duplicate_rate=row['duplicate_rate'], bot=row['bot'], bnt=row['bnt'],
        esot=row['esot'], esnt=row['esnt'], esont=row['esont'],
        foebot=row['foebot'], foebnt=row['foebnt'], foebont=row['foebont'],
        asdot=row['asdot'], asdnt=row['asdnt'], bcot=row['bcot'],
        cotr=row['cotr'], bcnt=row['bcnt'], cofr=row['cofr'],
        fotcwal4=row['fotcwal4'], fotcwal10=row['fotcwal10'], fotcwal30=row['fotcwal30'],
        fotcwal100=row['fotcwal100'], fofrcwal4=row['fofrcwal4'], fofrcwal10=row['fofrcwal10'],
        fofrcwal30=row['fofrcwal30'], fofrcwal100=row['fofrcwal100'])


def import_ntsampleqc(row):
    sid = row['Sample']
    barcode = '%s_NT' % sid.split('_')[0]
    try:
        SampleClinicInfo.objects.get(barcode=barcode)
    except Exception:
        return
    if sid.split('_')[1][:1] == 'N':
        import_nsampleqc(row)
    elif sid.split('_')[1][:1] == 'T':
        import_tsampleqc(row)
    else:
        pass


def process_data_n(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            if d.get(row['Sample']) is None:
                sd = d[row['Sample']] = {}
                sd['Sample'] = row['Sample']
                sd['mtotal_reads'] = row['Total'].strip()
                sd['mduplicate'] = row['Duplicate'].strip()
                sd['map_reads'] = row['Mapped'].strip()
                sd['mrp'] = row['Properly mapped'].strip()
                sd['mtdc'] = row['With mate mapped to a different chr'].strip()
                sd['mtdc5'] = row['With mate mapped to a different chr (mapQ>=5)'].strip()
                sd['bot'] = int(row['Bases_on_target'].replace(',', ''))
                sd['bnt'] = int(row['Bases_near_target'].replace(',', ''))
                sd['esot'] = float(row['Effective_sequences_on_target(Mb)'])
                sd['esnt'] = float(row['Effective_sequences_near_target(Mb)'])
                sd['esont'] = float(row['Effective_sequences_on_or_near_targe(Mb)'])
                sd['foebot'] = float(row['Fraction_of_effective_bases_on_target'].replace('%', ''))
                sd['foebnt'] = float(row['Fraction_of_effective_bases_near_target'].replace('%', ''))
                sd['foebont'] = float(row['Fraction_of_effective_bases_on_or_near_target'].replace('%', ''))
                sd['asdot'] = float(row['Average_sequencing_depth_on_target'])
                sd['asdnt'] = float(row['Average_sequencing_depth_near_target'])
                sd['bcot'] = int(row['Bases_covered_on_target'].replace(',', ''))
                sd['cotr'] = float(row['Coverage_of_target_region'].replace('%', ''))
                sd['bcnt'] = int(row['Bases_covered_near_target'].replace(',', ''))
                sd['cofr'] = float(row['Coverage_of_flanking_region'].replace('%', ''))
                sd['fotcwal4'] = float(row['Fraction_of_target_covered_with_at_least_4x'].replace('%', ''))
                sd['fotcwal10'] = float(row['Fraction_of_target_covered_with_at_least_10x'].replace('%', ''))
                sd['fotcwal30'] = float(row['Fraction_of_target_covered_with_at_least_30x'].replace('%', ''))
                sd['fotcwal100'] = float(row['Fraction_of_target_covered_with_at_least_100x'].replace('%', ''))
                sd['fofrcwal4'] = float(row['Fraction_of_flanking_region_covered_with_at_least_4x'].replace('%', ''))
                sd['fofrcwal10'] = float(row['Fraction_of_flanking_region_covered_with_at_least_10x'].replace('%', ''))
                sd['fofrcwal30'] = float(row['Fraction_of_flanking_region_covered_with_at_least_30x'].replace('%', ''))
                sd['fofrcwal100'] = float(row['Fraction_of_flanking_region_covered_with_at_least_100x'].replace('%', ''))
    return d


def import_tsampleqc_n(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'T':
        return
    barcode = '%s_NT' % sid.split('_')[0]
    sample_clinic_info = SampleClinicInfo.objects.get(barcode=barcode)
    sample_clinic_info.tsampleid = sid
    sample_clinic_info.save()
    TumorSampleQC.objects.get_or_create(
        sample_clinic_info=sample_clinic_info, tsampleid=sid, sample_type='FFPE', read_type='151+8+8+151', lib_type='WES',
        mtotal_reads=row['mtotal_reads'], mduplicate=row['mduplicate'],
        map_reads=row['map_reads'], mrp=row['mrp'], mtdc=row['mtdc'], mtdc5=row['mtdc5'], bot=row['bot'], bnt=row['bnt'],
        esot=row['esot'], esnt=row['esnt'], esont=row['esont'],
        foebot=row['foebot'], foebnt=row['foebnt'], foebont=row['foebont'],
        asdot=row['asdot'], asdnt=row['asdnt'], bcot=row['bcot'],
        cotr=row['cotr'], bcnt=row['bcnt'], cofr=row['cofr'],
        fotcwal4=row['fotcwal4'], fotcwal10=row['fotcwal10'], fotcwal30=row['fotcwal30'],
        fotcwal100=row['fotcwal100'], fofrcwal4=row['fofrcwal4'], fofrcwal10=row['fofrcwal10'],
        fofrcwal30=row['fofrcwal30'], fofrcwal100=row['fofrcwal100'])


def import_nsampleqc_n(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'N':
        return
    barcode = '%s_NT' % sid.split('_')[0]
    sample_clinic_info = SampleClinicInfo.objects.get(barcode=barcode)
    sample_clinic_info.nsampleid = sid
    sample_clinic_info.save()
    NormalSampleQC.objects.get_or_create(
        sample_clinic_info=sample_clinic_info, nsampleid=sid, sample_type='FFPE', read_type='151+8+8+151', lib_type='WES',
        mtotal_reads=row['mtotal_reads'], mduplicate=row['mduplicate'],
        map_reads=row['map_reads'], mrp=row['mrp'], mtdc=row['mtdc'], mtdc5=row['mtdc5'], bot=row['bot'], bnt=row['bnt'],
        esot=row['esot'], esnt=row['esnt'], esont=row['esont'],
        foebot=row['foebot'], foebnt=row['foebnt'], foebont=row['foebont'],
        asdot=row['asdot'], asdnt=row['asdnt'], bcot=row['bcot'],
        cotr=row['cotr'], bcnt=row['bcnt'], cofr=row['cofr'],
        fotcwal4=row['fotcwal4'], fotcwal10=row['fotcwal10'], fotcwal30=row['fotcwal30'],
        fotcwal100=row['fotcwal100'], fofrcwal4=row['fofrcwal4'], fofrcwal10=row['fofrcwal10'],
        fofrcwal30=row['fofrcwal30'], fofrcwal100=row['fofrcwal100'])


def import_ntsampleqc_n(row):
    sid = row['Sample']
    barcode = '%s_NT' % sid.split('_')[0]
    try:
        SampleClinicInfo.objects.get(barcode=barcode)
    except Exception:
        return
    if sid.split('_')[1][:1] == 'N':
        import_nsampleqc_n(row)
    elif sid.split('_')[1][:1] == 'T':
        import_tsampleqc_n(row)
    else:
        pass


def update_tsampleqc_n(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'T':
        return
    try:
        obj = TumorSampleQC.objects.get(tsampleid=sid)
        obj.rawsize = row['rawsize']
        obj.cleansize = row['cleansize']
        obj.duplicate_rate = row['duplicate_rate']
        obj.save()
    except TumorSampleQC.DoesNotExist:
        print('no such tsampleid <%s> <TumorSampleQC>.' % sid)


def update_nsampleqc_n(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] != 'N':
        return
    try:
        obj = NormalSampleQC.objects.get(nsampleid=sid)
        obj.rawsize = row['rawsize']
        obj.cleansize = row['cleansize']
        obj.duplicate_rate = row['duplicate_rate']
        obj.save()
    except NormalSampleQC.DoesNotExist:
        print('no such nsampleid <%s> <NormalSampleQC>.' % sid)


def update_ntsampleqc_n(row):
    sid = row['Sample']
    if sid.split('_')[1][:1] == 'N':
        update_nsampleqc_n(row)
    elif sid.split('_')[1][:1] == 'T':
        update_tsampleqc_n(row)
    else:
        pass


if __name__ == '__main__':
    tab = sys.argv[1]
