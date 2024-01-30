import json

from .models import (
    ProteinDomainsDB,
    SampleClinicInfo, TumorSampleQC, NormalSampleQC,
    SnvRecord, VariationClassification, VariantType,
    SnvClass, MutatedGenes, GeneVariationClassification,
    GeneVariantType, GeneSnvClass,
    SortedGeneVariationClassification, Oncoplot,
    VariationClassificationTotalBar,
    VariantTypeTotalBar, SnvClassTotalBar,
    OverViewStatsPlot,
    VariationClassificationCategoryPlot,
    VariantTypeCategoryPlot,
    SnvClassCategoryPlot
)


def index_data():
    infos = {
        'sex': {
            'male': 0,
            'female': 0,
            'NA': 0
        },
        'age': {
            'name': [],
            'value': []
        },
        'os': {
            'sampleid': [],
            'time': [],
            'probability': [],
            'status': [],
            'xmax': 0
        },
        'pathological_stage': {
            'name': [],
            'value': [],
            'pair': []
        },
        'patients_num': 0,
        'tumor_sample_num': 0,
        'mcrc_primary': 0,
        'mcrc_metastasis': 0
    }
    # overview
    objs = OverViewStatsPlot.objects.all()
    obj = objs[0]
    sex_values = obj.sex_num_list.split(',')
    infos['sex']['male'] = sex_values[0]
    infos['sex']['female'] = sex_values[1]
    infos['sex']['NA'] = sex_values[2]
    age_names = obj.age_list.split(',')
    age_values = obj.age_num_list.split(',')
    infos['age']['name'] = age_names
    infos['age']['value'] = age_values
    infos['os']['sampleid'] = obj.os_sampleid_list.split(',')
    os_time_list = obj.os_time_list.split(',')
    infos['os']['time'] = os_time_list
    infos['os']['probability'] = obj.os_probability_list.split(',')
    infos['os']['status'] = obj.os_status_list.split(',')
    infos['os']['xmax'] = max(map(float, os_time_list))
    patho_names = obj.pathostage_list.split(',')
    patho_values = obj.pathostage_num_list.split(',')
    infos['pathological_stage']['name'] = patho_names
    infos['pathological_stage']['value'] = patho_values
    for i in range(len(patho_names)):
        infos['pathological_stage']['pair'].append([patho_values[i], patho_names[i]])
    infos['patients_num'] = obj.patients_num
    infos['tumor_sample_num'] = obj.tumor_sample_num
    infos['mcrc_primary'] = obj.mcrc_primary_num
    infos['mcrc_metastasis'] = obj.mcrc_metastasis_num

    return infos


def sampleinfo_data(**kwargs):
    infos = {
        'sampleinfos': [],
        'pathological_stages': [],
        'primary_locations': [],
        'detailed_sites': []
    }
    objs = SampleClinicInfo.objects.all()
    for obj in objs:
        infos['pathological_stages'].append(obj.pathological_stage)
        infos['primary_locations'].append(obj.primary_location)
        infos['detailed_sites'].append(obj.detailed_site)
        if not kwargs:
            sampleinfo = {}
            sampleinfo['barcode'] = obj.barcode
            sampleinfo['tsampleid'] = obj.tsampleid
            sampleinfo['nsampleid'] = obj.nsampleid
            sampleinfo['gender'] = obj.gender
            sampleinfo['diagnosis_age'] = obj.diagnosis_age
            sampleinfo['surgery_date'] = obj.surgery_date
            sampleinfo['pathological_grade'] = obj.pathological_grade
            sampleinfo['pathological_stage'] = obj.pathological_stage
            sampleinfo['primary_location'] = obj.primary_location
            sampleinfo['detailed_site'] = obj.detailed_site
            sampleinfo['metastasis'] = obj.metastasis
            sampleinfo['time_os'] = obj.time_os
            sampleinfo['ajcc_T_stage'] = obj.ajcc_T_stage
            sampleinfo['ajcc_N_stage'] = obj.ajcc_N_stage
            sampleinfo['sampleid'] = obj.barcode.split('_')[0]
            infos['sampleinfos'].append(sampleinfo)

    infos['pathological_stages'] = set(infos['pathological_stages'])
    infos['primary_locations'] = set(infos['primary_locations'])
    infos['detailed_sites'] = set(infos['detailed_sites'])

    if kwargs:
        infos['args'] = kwargs
        objs = SampleClinicInfo.objects.filter(**kwargs)
        for obj in objs:
            sampleinfo = {}
            sampleinfo['barcode'] = obj.barcode
            sampleinfo['tsampleid'] = obj.tsampleid
            sampleinfo['nsampleid'] = obj.nsampleid
            sampleinfo['gender'] = obj.gender
            sampleinfo['diagnosis_age'] = obj.diagnosis_age
            sampleinfo['surgery_date'] = obj.surgery_date
            sampleinfo['pathological_grade'] = obj.pathological_grade
            sampleinfo['pathological_stage'] = obj.pathological_stage
            sampleinfo['primary_location'] = obj.primary_location
            sampleinfo['detailed_site'] = obj.detailed_site
            sampleinfo['metastasis'] = obj.metastasis
            sampleinfo['time_os'] = obj.time_os
            sampleinfo['ajcc_T_stage'] = obj.ajcc_T_stage
            sampleinfo['ajcc_N_stage'] = obj.ajcc_N_stage
            sampleinfo['sampleid'] = obj.barcode.split('_')[0]
            infos['sampleinfos'].append(sampleinfo)

    return infos


def sampletab_initialize():
    infos = {
        'pathological_stages': [],
        'primary_locations': [],
        'detailed_sites': [],
    }
    objs = SampleClinicInfo.objects.all()
    for obj in objs:
        infos['pathological_stages'].append(obj.pathological_stage)
        infos['primary_locations'].append(obj.primary_location)
        infos['detailed_sites'].append(obj.detailed_site)

    infos['pathological_stages'] = set(sorted(infos['pathological_stages']))
    infos['primary_locations'] = set(sorted(infos['primary_locations']))
    infos['detailed_sites'] = set(sorted(infos['detailed_sites']))

    return infos


def sampletab_data(page_start, page_length, order, **kwargs):
    sampleinfos = []
    if not kwargs:
        total_objs = SampleClinicInfo.objects.all()
    else:
        total_objs = SampleClinicInfo.objects.filter(**kwargs)
    if not order:
        total_objs = total_objs
    else:
        total_objs = total_objs.order_by(order[0])
    total_length = total_objs.count()
    if page_length == -1:
        page_length = total_length
    page_end = page_start + page_length
    objs = total_objs[page_start:page_end]
    for obj in objs:
        sampleinfo = {}
        sampleinfo['barcode'] = obj.barcode
        sampleinfo['tsampleid'] = obj.tsampleid
        sampleinfo['nsampleid'] = obj.nsampleid
        sampleinfo['gender'] = obj.gender
        sampleinfo['diagnosis_age'] = obj.diagnosis_age
        sampleinfo['surgery_date'] = obj.surgery_date
        sampleinfo['pathological_grade'] = obj.pathological_grade
        sampleinfo['pathological_stage'] = obj.pathological_stage
        sampleinfo['primary_location'] = obj.primary_location
        sampleinfo['detailed_site'] = obj.detailed_site
        sampleinfo['metastasis'] = obj.metastasis
        sampleinfo['time_os'] = obj.time_os
        sampleinfo['ajcc_T_stage'] = obj.ajcc_T_stage
        sampleinfo['ajcc_N_stage'] = obj.ajcc_N_stage
        sampleinfo['sampleid'] = obj.barcode.split('_')[0]
        sampleinfos.append(sampleinfo)

    return sampleinfos, total_length


def variation_data():
    infos = {}
    # varclass
    objs = VariationClassificationTotalBar.objects.all()
    for obj in objs:
        infos['varclass_all'] = {
            'name': ['In_Frame_Del', 'In_Frame_Ins', 'Frame_Shift_Del', 'Frame_Shift_Ins', 'Splice_Region', 'Nonsense_Mutation', 'Missense_Mutation'],
            'value': [obj.ifd, obj.ifi, obj.fsd, obj.fsi, obj.splice, obj.nonsense, obj.missense]
        }
    ivps = infos['varclass_per_sample'] = {
        'tsampleid': [],
        'max': 0,
        'max2': 0,
        'ifd': [],
        'ifi': [],
        'fsd': [],
        'fsi': [],
        'splice': [],
        'nonsense': [],
        'missense': []
    }
    objs = VariationClassification.objects.all()  # sorted
    ivps['max'] = objs[0].total
    ivps['max'] += ivps['max'] * 5 // 100
    ivps['max2'] = objs[50].total
    ivps['max2'] += ivps['max2'] * 5 // 100
    for obj in objs:
        ivps['tsampleid'].append(obj.tsampleid)
        ivps['ifd'].append(obj.ifd)
        ivps['ifi'].append(obj.ifi)
        ivps['fsd'].append(obj.fsd)
        ivps['fsi'].append(obj.fsi)
        ivps['splice'].append(obj.splice)
        ivps['nonsense'].append(obj.nonsense)
        ivps['missense'].append(obj.missense)
    # vartype
    objs = VariantTypeTotalBar.objects.all()
    infos['vartype_all'] = {
        'name': ['DEL', 'INS', 'SNP'],
        'value': [0 for x in range(3)]
    }
    for obj in objs:
        infos['vartype_all']['value'][0] = obj.dels
        infos['vartype_all']['value'][1] = obj.ins
        infos['vartype_all']['value'][2] = obj.snp
    # snvclass
    isa = infos['snvclass_all'] = {
        'name': ['T>G', 'T>A', 'T>C', 'C>T', 'C>G', 'C>A'][::-1],
        'value': [0 for x in range(6)],
        'rate': [0.0 for x in range(6)]
    }
    objs = SnvClassTotalBar.objects.all()
    for obj in objs:
        isa['value'][5] = obj.t2g
        isa['value'][4] = obj.t2a
        isa['value'][3] = obj.t2c
        isa['value'][2] = obj.c2t
        isa['value'][1] = obj.c2g
        isa['value'][0] = obj.c2a
        isa['rate'][5] = '%.2f' % (obj.t2g_rate * 100)
        isa['rate'][4] = '%.2f' % (obj.t2a_rate * 100)
        isa['rate'][3] = '%.2f' % (obj.t2c_rate * 100)
        isa['rate'][2] = '%.2f' % (obj.c2t_rate * 100)
        isa['rate'][1] = '%.2f' % (obj.c2g_rate * 100)
        isa['rate'][0] = '%.2f' % (obj.c2a_rate * 100)
    objs = SnvClass.objects.all()
    snvclass_sample_list = ivps['tsampleid']  # 与varclass排序保持一致
    isps = infos['snvclass_per_sample'] = {
        'tsampleid': snvclass_sample_list,
        't2g': [0.0 for x in snvclass_sample_list],
        't2a': [0.0 for x in snvclass_sample_list],
        't2c': [0.0 for x in snvclass_sample_list],
        'c2t': [0.0 for x in snvclass_sample_list],
        'c2g': [0.0 for x in snvclass_sample_list],
        'c2a': [0.0 for x in snvclass_sample_list],
        'max': 1
    }
    for obj in objs:
        i = snvclass_sample_list.index(obj.tsampleid)
        isps['t2g'][i] = '%.2f' % (obj.t2g_rate)
        isps['t2a'][i] = '%.2f' % (obj.t2a_rate)
        isps['t2c'][i] = '%.2f' % (obj.t2c_rate)
        isps['c2t'][i] = '%.2f' % (obj.c2t_rate)
        isps['c2g'][i] = '%.2f' % (obj.c2g_rate)
        isps['c2a'][i] = '%.2f' % (obj.c2a_rate)
    # oncoplot
    infos['oncoplot'] = {}
    top_gene_list = list(range(30))
    itg = infos['oncoplot']['topgenes'] = {
        'name': ['' for x in top_gene_list],
        'sample_number': [0.0 for x in top_gene_list],
        'max': 0,
        'missense': [0 for x in top_gene_list],
        'nonsense': [0 for x in top_gene_list],
        'splice': [0 for x in top_gene_list],
        'fsi': [0 for x in top_gene_list],
        'fsd': [0 for x in top_gene_list],
        'ifi': [0 for x in top_gene_list],
        'ifd': [0 for x in top_gene_list],
        # 'ssv': {},
        'gsv': [],
        'gsvbar': []
    }
    objs = SortedGeneVariationClassification.objects.all()[:30]
    itg['max'] = objs[0].tsample_num_rate * 100
    itg['max'] = itg['max'] + itg['max'] * 5 // 100
    for i in range(30):
        # obj = objs[29 - i]
        obj = objs[i]
        itg['name'][i] = obj.symbol
        # obj = objs[29 - i]
        itg['sample_number'][i] = '%.2f' % (obj.tsample_num_rate * 100)
        itg['missense'][i] = '%.2f' % (obj.missense_rate * obj.tsample_num_rate * 100)
        itg['nonsense'][i] = '%.2f' % (obj.nonsense_rate * obj.tsample_num_rate * 100)
        itg['splice'][i] = '%.2f' % (obj.splice_rate * obj.tsample_num_rate * 100)
        itg['fsi'][i] = '%.2f' % (obj.fsi_rate * obj.tsample_num_rate * 100)
        itg['fsd'][i] = '%.2f' % (obj.fsd_rate * obj.tsample_num_rate * 100)
        itg['ifi'][i] = '%.2f' % (obj.ifi_rate * obj.tsample_num_rate * 100)
        itg['ifd'][i] = '%.2f' % (obj.ifd_rate * obj.tsample_num_rate * 100)
    infos['top10genes'] = {
        'name': itg['name'][:10],
        'sample_number': itg['sample_number'][:10],
        'max': itg['max'],
        'missense': itg['missense'][:10],
        'nonsense': itg['nonsense'][:10],
        'splice': itg['splice'][:10],
        'fsi': itg['fsi'][:10],
        'fsd': itg['fsd'][:10],
        'ifi': itg['ifi'][:10],
        'ifd': itg['ifd'][:10]
    }
    # sample:symbol:varclass
    # itgs = itg['ssv'] = {
    #     'samples_list': [],
    #     'missense_list': [],
    #     'nonsense_list': [],
    #     'splice_list': [],
    #     'fsi_list': [],
    #     'fsd_list': [],
    #     'ifi_list': [],
    #     'ifd_list': [],
    #     'mh_list': []
    # }
    objs = Oncoplot.objects.all()
    # for obj in objs:
    #     itgs['samples_list'].append(obj.tsampleid)
    #     itgs['missense_list'].append(obj.missense_list)
    #     itgs['nonsense_list'].append(obj.nonsense_list)
    #     itgs['splice_list'].append(obj.splice_list)
    #     itgs['fsi_list'].append(obj.fsi_list)
    #     itgs['fsd_list'].append(obj.fsd_list)
    #     itgs['ifi_list'].append(obj.ifi_list)
    #     itgs['ifd_list'].append(obj.ifd_list)
    #     itgs['mh_list'].append(obj.mh_list)
    onco_sample_list = list(range(len(objs)))
    itgg = itg['gsv'] = [[-1 for x in onco_sample_list] for x in top_gene_list]
    itggb = itg['gsvbar'] = {
        'tsampleid': ['' for x in onco_sample_list],
        'max': ivps['max'],
        'ifd': [0.0 for x in onco_sample_list],
        'ifi': [0.0 for x in onco_sample_list],
        'fsd': [0.0 for x in onco_sample_list],
        'fsi': [0.0 for x in onco_sample_list],
        'splice': [0.0 for x in onco_sample_list],
        'nonsense': [0.0 for x in onco_sample_list],
        'missense': [0.0 for x in onco_sample_list]
    }
    for i, obj in enumerate(objs):
        itggb['tsampleid'][i] = obj.tsampleid
        idx = ivps['tsampleid'].index(obj.tsampleid)
        itggb['ifd'][i] = ivps['ifd'][idx]
        itggb['ifi'][i] = ivps['ifi'][idx]
        itggb['fsd'][i] = ivps['fsd'][idx]
        itggb['fsi'][i] = ivps['fsi'][idx]
        itggb['splice'][i] = ivps['splice'][idx]
        itggb['nonsense'][i] = ivps['nonsense'][idx]
        itggb['missense'][i] = ivps['missense'][idx]
        for j, v in enumerate(obj.missense_list):
            if v == '1':
                itgg[j][i] = 0
        for j, v in enumerate(obj.nonsense_list):
            if v == '1':
                itgg[j][i] = 1
        for j, v in enumerate(obj.splice_list):
            if v == '1':
                itgg[j][i] = 2
        for j, v in enumerate(obj.fsi_list):
            if v == '1':
                itgg[j][i] = 3
        for j, v in enumerate(obj.fsd_list):
            if v == '1':
                itgg[j][i] = 4
        for j, v in enumerate(obj.ifi_list):
            if v == '1':
                itgg[j][i] = 5
        for j, v in enumerate(obj.ifd_list):
            if v == '1':
                itgg[j][i] = 6
        for j, v in enumerate(obj.mh_list):
            if v == '1':
                itgg[j][i] = 7

    return infos


def category_data():
    infos = {
        'detailed_sites': {
            'varclass': {
                'name': [],
                'missense': [],
                'nonsense': [],
                'splice': [],
                'fsi': [],
                'fsd': [],
                'ifi': [],
                'ifd': [],
                'max': 1
            },
            'vartype': {
                'name': [],
                'number': [],
                'snp': [],
                'ins': [],
                'del': [],
                'max': 1
            },
            'snvclass': {
                'name': [],
                'c2a': [],
                'c2g': [],
                'c2t': [],
                't2c': [],
                't2a': [],
                't2g': [],
                'max': 1
            },
            'sample_number': {
                'name': [],
                'number': []
            }
        },
        'primary_locations': {
            'varclass': {
                'name': [],
                'missense': [],
                'nonsense': [],
                'splice': [],
                'fsi': [],
                'fsd': [],
                'ifi': [],
                'ifd': [],
                'max': 1
            },
            'vartype': {
                'name': [],
                'number': [],
                'snp': [],
                'ins': [],
                'del': [],
                'max': 1
            },
            'snvclass': {
                'name': [],
                'c2a': [],
                'c2g': [],
                'c2t': [],
                't2c': [],
                't2a': [],
                't2g': [],
                'max': 1
            }
        },
        'pathological_stages': {
            'varclass': {
                'name': [],
                'missense': [],
                'nonsense': [],
                'splice': [],
                'fsi': [],
                'fsd': [],
                'ifi': [],
                'ifd': [],
                'max': 1
            },
            'vartype': {
                'name': [],
                'number': [],
                'snp': [],
                'ins': [],
                'del': [],
                'max': 1
            },
            'snvclass': {
                'name': [],
                'c2a': [],
                'c2g': [],
                'c2t': [],
                't2c': [],
                't2a': [],
                't2g': [],
                'max': 1
            }
        }
    }
    # varclass
    objs = VariationClassificationCategoryPlot.objects.all()
    for obj in objs:
        k = '_'.join(obj.category.split('_')[:2])
        ikv = infos[k]['varclass']
        category = obj.category.split('_')[-1]
        ikv['name'].append(category)
        ikv['missense'].append('%.2f' % (obj.missense_rate / 100))
        ikv['nonsense'].append('%.2f' % (obj.nonsense_rate / 100))
        ikv['splice'].append('%.2f' % (obj.splice_rate / 100))
        ikv['fsi'].append('%.2f' % (obj.fsi_rate / 100))
        ikv['fsd'].append('%.2f' % (obj.fsd_rate / 100))
        ikv['ifi'].append('%.2f' % (obj.ifi_rate / 100))
        ikv['ifd'].append('%.2f' % (obj.ifd_rate / 100))
    # vartype
    objs = VariantTypeCategoryPlot.objects.all()
    for obj in objs:
        k = '_'.join(obj.category.split('_')[:2])
        ikv = infos[k]['vartype']
        category = obj.category.split('_')[-1]
        ikv['name'].append(category)
        ikv['number'].append(obj.tsample_num)
        ikv['snp'].append('%.2f' % (obj.snp_rate / 100))
        ikv['ins'].append('%.2f' % (obj.ins_rate / 100))
        ikv['del'].append('%.2f' % (obj.del_rate / 100))
    # snvclass
    objs = SnvClassCategoryPlot.objects.all()
    for obj in objs:
        k = '_'.join(obj.category.split('_')[:2])
        iks = infos[k]['snvclass']
        category = obj.category.split('_')[-1]
        iks['name'].append(category)
        iks['c2a'].append('%.2f' % (obj.c2a_rate / 100))
        iks['c2g'].append('%.2f' % (obj.c2g_rate / 100))
        iks['c2t'].append('%.2f' % (obj.c2t_rate / 100))
        iks['t2c'].append('%.2f' % (obj.t2c_rate / 100))
        iks['t2a'].append('%.2f' % (obj.t2a_rate / 100))
        iks['t2g'].append('%.2f' % (obj.t2g_rate / 100))
    # sort sample number
    idv = infos['detailed_sites']['vartype']
    dnn = zip(idv['number'], idv['name'])
    dnn = sorted(dnn, reverse=True)
    for d in dnn:
        infos['detailed_sites']['sample_number']['name'].append(d[1])
        infos['detailed_sites']['sample_number']['number'].append(d[0])

    return infos


def json_serializer(d, fp):
    with open(fp, 'w') as jf:
        json.dump(d, jf, indent=4, sort_keys=True)


def index_json():
    d = index_data()
    fp = 'tmp/index.json'
    json_serializer(d, fp)


def variation_json():
    d = variation_data()
    fp = 'tmp/variation.json'
    json_serializer(d, fp)
