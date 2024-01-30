import csv
import sys

from cccga.models import SampleClinicInfo


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            k = row['Tumor_Sample_Barcode'].strip()
            if d.get(k) is None:
                sd = d[k] = {}
                sd['barcode'] = k
                sd['gender'] = row['gender'].strip()
                sd['birth'] = row['date_of_birth'].strip().replace('/', '-') if row['date_of_birth'].strip() != 'NA' else None
                sd['marital'] = row['marital_status'].strip()
                sd['height'] = row['height'].strip()
                sd['weight'] = row['weight'].strip()
                sd['smoking'] = row['smoking'].strip()
                sd['diagnosis_date'] = row['date_of_diagnosis'].strip().replace('/', '-') if row['date_of_diagnosis'].strip() != 'NA' else None
                sd['diagnosis_age'] = row['age_at_diagnosis'].strip()
                sd['chemo_radio'] = row['chemo.radio_before_surgery'].strip()
                sd['surgery_date'] = row['date_of_surgery'].strip().replace('/', '-') if row['date_of_surgery'].strip() != 'NA' else None
                sd['detailed_site'] = row['detailed_tumor_site'].strip()
                sd['primary_location'] = row['primary_tumor_location'].strip()
                sd['pathological_grade'] = row['pathological_grade'].strip()
                sd['tumor_length'] = row['tumor_length'].strip()
                sd['tumor_width'] = row['tumor_width'].strip()
                sd['tumor_height'] = row['tumor_height'].strip()
                sd['ajcc_T_stage'] = row['ajcc_T_stage'].strip()
                sd['positive_lymph_node'] = row['positive_lymph_node'].strip()
                sd['total_examined_lymphnode'] = row['total_examined_lymphnode'].strip()
                sd['tumor_depoist'] = row['tumor_depoist'].strip()
                sd['ajcc_N_stage'] = row['ajcc_N_stage'].strip()
                sd['metastasis'] = row['metastasis_at_diagnosis'].strip()
                sd['surgery_stage'] = row['surgery_stage'].strip()
                sd['pathological_stage'] = row['pathological_stage'].strip()
                sd['nerve_invasion'] = row['nerve_invasion'].strip()
                sd['vessel_invasion'] = row['vessel_invasion'].strip()
                sd['distal'] = row['distal_margin_positive'].strip()
                sd['proximal'] = row['proximal_margin_positive'].strip()
                sd['mlh1'] = row['MLH1'].strip()
                sd['msh2'] = row['MSH2'].strip()
                sd['msh6'] = row['MSH6'].strip()
                sd['pms2'] = row['PMS2'].strip()
                sd['her2'] = row['Her.2'].strip()
                sd['nras'] = row['NRAS'].strip()
                sd['kras'] = row['KRAS'].strip()
                sd['braf'] = row['BRAF'].strip()
                sd['death_date_n'] = row['date_of_death_new'].strip().replace('/', '-') if row['date_of_death_new'].strip() != 'NA' else None
                sd['time_os'] = row['time_from_diagnosis_to_death_new'].strip()
                sd['vital_n'] = row['vital_status_new'].strip()
                sd['mmr'] = row['MMR'].strip()
                sd['vital'] = row['vital_status'].strip()
    return d


def import_sample_clinic_info(row):
    SampleClinicInfo.objects.get_or_create(
        barcode=row['barcode'], gender=row['gender'],
        birth=row['birth'], marital=row['marital'], height=row['height'],
        weight=row['weight'], smoking=row['smoking'], diagnosis_date=row['diagnosis_date'],
        diagnosis_age=row['diagnosis_age'], chemo_radio=row['chemo_radio'], surgery_date=row['surgery_date'],
        detailed_site=row['detailed_site'], primary_location=row['primary_location'], pathological_grade=row['pathological_grade'],
        tumor_length=row['tumor_length'], tumor_width=row['tumor_width'], tumor_height=row['tumor_height'],
        ajcc_T_stage=row['ajcc_T_stage'], positive_lymph_node=row['positive_lymph_node'], total_examined_lymphnode=row['total_examined_lymphnode'],
        tumor_depoist=row['tumor_depoist'], ajcc_N_stage=row['ajcc_N_stage'], metastasis=row['metastasis'],
        surgery_stage=row['surgery_stage'], pathological_stage=row['pathological_stage'], nerve_invasion=row['nerve_invasion'],
        vessel_invasion=row['vessel_invasion'], distal=row['distal'], proximal=row['proximal'],
        mlh1=row['mlh1'], msh2=row['msh2'], msh6=row['msh6'],
        pms2=row['pms2'], her2=row['her2'], nras=row['nras'],
        kras=row['kras'], braf=row['braf'], death_date_n=row['death_date_n'],
        time_os=row['time_os'], vital_n=row['vital_n'], mmr=row['mmr'],
        vital=row['vital'])


if __name__ == '__main__':
    tab = sys.argv[1]
