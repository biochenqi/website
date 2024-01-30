import csv
import sys

from cccga.models import (
    TumorSampleQC, VariationClassification,
    VariantType, SnvClass, MutatedGenes, GeneVariationClassification,
    GeneVariantType, GeneSnvClass,
    SortedGeneVariationClassification, Oncoplot,
    SampleClinicInfo, OverViewStatsPlot,
    VariationClassificationCategoryPlot,
    VariantTypeCategoryPlot,
    SnvClassCategoryPlot
)


def overview_stats_plot():
    infos = {
        'sex': {
            'name': ['male', 'female', 'NA'],
            'value': [0, 0, 0]
        },
        'age': {
            'name': ['<20', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90-99', '>=100', 'NA'],
            'value': [0 for x in range(11)]
        },
        'os': {
            'source': {},
            'process': {
                'sampleid': [],
                'time': [],
                'number': [],
                'probability': [],
                'status': []
            }
        },
        'pathological_stage': {
            'name': [],
            'value': []
        },
        'patients_num': 0,
        'tumor_sample_num': 0,
        'mcrc_primary': 0,
        'mcrc_metastasis': 0
    }
    ios = infos['os']['source']
    ios_1 = ios['1'] = {}
    ios_censored = ios['censored'] = {}
    iop = infos['os']['process']
    # maxt = ''
    patho_stage = {}
    objs = SampleClinicInfo.objects.all()
    for obj in objs:
        # gender
        if obj.gender == infos['sex']['name'][0]:
            infos['sex']['value'][0] += 1
        if obj.gender == infos['sex']['name'][1]:
            infos['sex']['value'][1] += 1
        if obj.gender == infos['sex']['name'][2]:
            infos['sex']['value'][2] += 1
        # age
        try:
            age = int(obj.diagnosis_age)
        except ValueError:
            age = 'NA'
        if age == 'NA':
            infos['age']['value'][10] += 1
        elif age < 20:
            infos['age']['value'][0] += 1
        elif 20 <= age < 30:
            infos['age']['value'][1] += 1
        elif 30 <= age < 40:
            infos['age']['value'][2] += 1
        elif 40 <= age < 50:
            infos['age']['value'][3] += 1
        elif 50 <= age < 60:
            infos['age']['value'][4] += 1
        elif 60 <= age < 70:
            infos['age']['value'][5] += 1
        elif 70 <= age < 80:
            infos['age']['value'][6] += 1
        elif 80 <= age < 90:
            infos['age']['value'][7] += 1
        elif 90 <= age < 100:
            infos['age']['value'][8] += 1
        else:
            infos['age']['value'][9] += 1
        # os
        try:
            time = float(obj.time_os)
            if obj.os_status == '1':
                ioss = ios_1
            elif obj.os_status == 'censored':
                ioss = ios_censored
            else:
                raise
            if ioss.get(time) is None:
                iost = ioss[time] = {}
                iost['sampleid'] = [obj.barcode]
                iost['number'] = 1
            else:
                ioss[time]['sampleid'].append(obj.barcode)
                ioss[time]['number'] += 1
        except ValueError:
            pass
        # if obj.diagnosis_date is not None:
        #     time = maxt - obj.diagnosis_date
        #     time = time  # to month
        # pathological stage
        if patho_stage.get(obj.pathological_stage) is None:
            patho_stage[obj.pathological_stage] = 1
        else:
            patho_stage[obj.pathological_stage] += 1
        # metastasis
        if obj.metastasis == 'yes':
            infos['mcrc_metastasis'] += 1
        elif obj.metastasis == 'no':
            infos['mcrc_primary'] += 1
        else:
            pass

    osns_list = []  # element: (os, os_status, sample_num, sampleid_list)
    for k in ios_1:
        el = (k, 1, ios_1[k]['number'], '|'.join(ios_1[k]['sampleid']))
        osns_list.append(el)
    for k in ios_censored:
        el = (k, 0, ios_censored[k]['number'], '|'.join(ios_censored[k]['sampleid']))
        osns_list.append(el)
    osns_list_order = sorted(osns_list)
    total = len(objs)
    for i, v in enumerate(osns_list_order):
        if v[1] == 1:
            iop['time'].append(v[0])
            iop['sampleid'].append(v[3])
            p = (total - v[2]) / total
            if not iop['probability']:
                p = p * 1
            else:
                p = p * iop['probability'][-1]
            iop['probability'].append(p)
        total -= v[2]

    # patho_stage_order = sorted(patho_stage.items(), key=lambda d: d[1], reverse=True)
    # order by I/II/III/VI/IV/...
    patho_stage_order = sorted(patho_stage.items(), key=lambda d: d[0])
    for k in patho_stage_order:
        infos['pathological_stage']['name'].append(k[0])
        infos['pathological_stage']['value'].append(k[1])

    infos['patients_num'] = len(objs)
    infos['tumor_sample_num'] = len(TumorSampleQC.objects.all())

    return infos


def create_or_update_overview_stats_plot(d):
    sex_name = ','.join(d['sex']['name'])
    sex_value = ','.join(map(str, d['sex']['value']))
    age_name = ','.join(d['age']['name'])
    age_value = ','.join(map(str, d['age']['value']))
    os_sampleid_list = ','.join(d['os']['process']['sampleid'])
    os_time_list = ','.join(map(str, d['os']['process']['time']))
    os_number_list = ','.join(map(str, d['os']['process']['number']))
    os_probability_list = ','.join(map(str, d['os']['process']['probability']))
    os_status_list = ','.join(map(str, d['os']['process']['status']))
    patho_name = ','.join(d['pathological_stage']['name'])
    patho_value = ','.join(map(str, d['pathological_stage']['value']))
    patients_num = d['patients_num']
    tumor_sample_num = d['tumor_sample_num']
    mcrc_primary = d['mcrc_primary']
    mcrc_metastasis = d['mcrc_metastasis']
    OverViewStatsPlot.objects.get_or_create(
        sex_list=sex_name, sex_num_list=sex_value,
        age_list=age_name, age_num_list=age_value,
        os_sampleid_list=os_sampleid_list, os_time_list=os_time_list,
        os_number_list=os_number_list, os_probability_list=os_probability_list,
        os_status_list=os_status_list,
        pathostage_list=patho_name, pathostage_num_list=patho_value,
        patients_num=patients_num, tumor_sample_num=tumor_sample_num,
        mcrc_primary_num=mcrc_primary, mcrc_metastasis_num=mcrc_metastasis
    )


def sorted_gene_variation_classification():
    d = {
        'varclass': {},
        'rank': {}
    }
    objs = GeneVariationClassification.objects.all()
    for obj in objs:
        if d['varclass'].get(obj.symbol) is None:
            dg = d['varclass'][obj.symbol] = {
                'missense': obj.missense,
                'nonsense': obj.nonsense,
                'splice': obj.splice,
                'fsi': obj.fsi,
                'fsd': obj.fsd,
                'ifi': obj.ifi,
                'ifd': obj.ifd
            }
        else:
            dg = d['varclass'][obj.symbol]
            dg['missense'] += obj.missense
            dg['nonsense'] += obj.nonsense
            dg['splice'] += obj.splice
            dg['fsi'] += obj.fsi
            dg['fsd'] += obj.fsd
            dg['ifi'] += obj.ifi
            dg['ifd'] += obj.ifd
    # 统计某基因发生突变的样本数
    objs = MutatedGenes.objects.all()
    for obj in objs:
        if d['rank'].get(obj.symbol) is None:
            d['rank'][obj.symbol] = 1
        else:
            d['rank'][obj.symbol] += 1

    return d


def update_or_create_sorted_gene_variation_classification(d):
    # 排序
    dr_rank = sorted(d['rank'].items(), key=lambda x: x[1], reverse=True)
    # 写入db
    for i, dr in enumerate(dr_rank):
        dg = d['varclass'][dr[0]]
        rank = i + 1
        try:
            obj = SortedGeneVariationClassification.objects.get(symbol=dr[0])
            obj.tsample_num = dr[1]
            obj.rank = rank
            obj.missense = dg['missense']
            obj.nonsense = dg['nonsense']
            obj.splice = dg['splice']
            obj.fsi = dg['fsi']
            obj.fsd = dg['fsd']
            obj.ifi = dg['ifi']
            obj.ifd = dg['ifd']
            obj.save()
        except SortedGeneVariationClassification.DoesNotExist:
            SortedGeneVariationClassification.objects.create(
                symbol=dr[0], tsample_num=dr[1], rank=rank,
                missense=dg['missense'],
                nonsense=dg['nonsense'],
                splice=dg['splice'],
                fsi=dg['fsi'],
                fsd=dg['fsd'],
                ifi=dg['ifi'],
                ifd=dg['ifd']
            )


def oncoplot(num):
    gene_list = []
    for i in range(num):
        rank = i + 1
        obj = SortedGeneVariationClassification.objects.get(rank=rank)
        gene_list.append(obj.symbol)
    #
    objs = GeneVariationClassification.objects.all()
    d = {}
    for obj in objs:
        if obj.symbol not in gene_list:
            continue
        # initialize
        if d.get(obj.symbol) is None:
            ds = d[obj.symbol] = {}
            dt = ds[obj.tsampleid] = [obj.missense, obj.nonsense, obj.splice, obj.fsi, obj.fsd, obj.ifi, obj.ifd]
        else:
            if d[obj.symbol].get(obj.tsampleid) is None:
                dt = d[obj.symbol][obj.tsampleid] = [obj.missense, obj.nonsense, obj.splice, obj.fsi, obj.fsd, obj.ifi, obj.ifd]
            else:
                dt = d[obj.symbol][obj.tsampleid]
                n = [obj.missense, obj.nonsense, obj.splice, obj.fsi, obj.fsd, obj.ifi, obj.ifd]
                dt = list(map(lambda x: x[0] + x[1], zip(dt, n)))
    #
    ssv = {}
    sample_list = []
    for symbol in gene_list:
        for sample in d[symbol]:
            if ssv.get(sample) is None:
                sample_list.append(sample)
                ssv[sample] = {symbol: [0 for x in range(8)]}  # missense,nonsense,splice,fsi,fsd,ifi,ifd,mh
            else:
                ssv[sample][symbol] = [0 for x in range(8)]
            for i, v in enumerate(d[symbol][sample]):
                if v != 0:
                    ssv[sample][symbol][i] = 1
            if sum(ssv[sample][symbol]) > 1:
                ssv[sample][symbol] = [0 for x in range(7)] + [1]

    return gene_list, sample_list, ssv


def update_or_create_oncoplot(all_gene_list, sample_list, ssv):
    for i, sample in enumerate(sample_list):
        rank = i + 1
        gene_list, value_list = [], []
        all_value_list = ['0-0-0-0-0-0-0-0' for _ in all_gene_list]
        for gene in ssv[sample]:
            gene_list.append(gene)
            value = '-'.join(map(str, ssv[sample][gene]))
            value_list.append(value)
            index = all_gene_list.index(gene)
            all_value_list[index] = value
        g = ','.join(gene_list)
        v = ','.join(value_list)
        m, n, s, fi, fd, ii, ifd, mh = '', '', '', '', '', '', '', ''
        for value in all_value_list:
            _tmp = value.split('-')
            tmp = ['-' if x == '0' else x for x in _tmp]
            m += tmp[0]
            n += tmp[1]
            s += tmp[2]
            fi += tmp[3]
            fd += tmp[4]
            ii += tmp[5]
            ifd += tmp[6]
            mh += tmp[7]
        try:
            obj = Oncoplot.objects.get(tsampleid=sample)
            obj.rank = rank
            obj.gene_list = g
            obj.type_list = v
            obj.missense_list = m
            obj.nonsense_list = n
            obj.splice_list = s
            obj.fsi_list = fi
            obj.fsd_list = fd
            obj.ifi_list = ii
            obj.ifd_list = ifd
            obj.mh_list = mh
            obj.save()
        except Oncoplot.DoesNotExist:
            Oncoplot.objects.create(
                tsampleid=sample, rank=rank, gene_list=g, type_list=v,
                missense_list=m, nonsense_list=n,
                splice_list=s, fsi_list=fi,
                fsd_list=fd, ifi_list=ii,
                ifd_list=ifd, mh_list=mh
            )


def get_category():
    infos = {
        'pathological_stages': {},
        'primary_locations': {},
        'detailed_sites': {}
    }
    objs = SampleClinicInfo.objects.all()
    for obj in objs:
        if infos['pathological_stages'].get(obj.pathological_stage) is None:
            infos['pathological_stages'][obj.pathological_stage] = [obj.tsampleid]
        else:
            infos['pathological_stages'][obj.pathological_stage].append(obj.tsampleid)
        if infos['primary_locations'].get(obj.primary_location) is None:
            infos['primary_locations'][obj.primary_location] = [obj.tsampleid]
        else:
            infos['primary_locations'][obj.primary_location].append(obj.tsampleid)
        if infos['detailed_sites'].get(obj.detailed_site) is None:
            infos['detailed_sites'][obj.detailed_site] = [obj.tsampleid]
        else:
            infos['detailed_sites'][obj.detailed_site].append(obj.tsampleid)

    return infos


def variation_classification_category_plot(d):
    infos = {}
    for k in d:
        for c in d[k]:
            if c == 'NA':
                continue
            category = '_'.join([k, c])
            ic = infos[category] = {
                'missense': 0,
                'nonsense': 0,
                'splice': 0,
                'fsi': 0,
                'fsd': 0,
                'ifi': 0,
                'ifd': 0
            }
            for tsampleid in d[k][c]:
                try:
                    obj = VariationClassification.objects.get(tsampleid=tsampleid)
                    ic['missense'] += obj.missense
                    ic['nonsense'] += obj.nonsense
                    ic['splice'] += obj.splice
                    ic['fsi'] += obj.fsi
                    ic['fsd'] += obj.fsd
                    ic['ifi'] += obj.ifi
                    ic['ifd'] += obj.ifd
                except VariationClassification.DoesNotExist:
                    pass
    return infos


def create_or_update_variation_classification_category_plot(d):
    for k in d:
        try:
            obj = VariationClassificationCategoryPlot.objects.get(category=k)
            obj.missense = d[k]['missense']
            obj.nonsense = d[k]['nonsense']
            obj.splice = d[k]['splice']
            obj.fsi = d[k]['fsi']
            obj.fsd = d[k]['fsd']
            obj.ifi = d[k]['ifi']
            obj.ifd = d[k]['ifd']
            total = d[k]['missense'] + d[k]['nonsense'] + d[k]['splice'] + d[k]['fsi'] + d[k]['fsd'] + d[k]['ifi'] + d[k]['ifd']
            obj.total = total
            obj.missense_rate = d[k]['missense'] / total * 100
            obj.nonsense_rate = d[k]['nonsense'] / total * 100
            obj.splice_rate = d[k]['splice'] / total * 100
            obj.fsi_rate = d[k]['fsi'] / total * 100
            obj.fsd_rate = d[k]['fsd'] / total * 100
            obj.ifi_rate = d[k]['ifi'] / total * 100
            obj.ifd_rate = d[k]['ifd'] / total * 100
            obj.save()
        except VariationClassificationCategoryPlot.DoesNotExist:
            missense = d[k]['missense']
            nonsense = d[k]['nonsense']
            splice = d[k]['splice']
            fsi = d[k]['fsi']
            fsd = d[k]['fsd']
            ifi = d[k]['ifi']
            ifd = d[k]['ifd']
            total = d[k]['missense'] + d[k]['nonsense'] + d[k]['splice'] + d[k]['fsi'] + d[k]['fsd'] + d[k]['ifi'] + d[k]['ifd']
            missense_rate = d[k]['missense'] / total * 100
            nonsense_rate = d[k]['nonsense'] / total * 100
            splice_rate = d[k]['splice'] / total * 100
            fsi_rate = d[k]['fsi'] / total * 100
            fsd_rate = d[k]['fsd'] / total * 100
            ifi_rate = d[k]['ifi'] / total * 100
            ifd_rate = d[k]['ifd'] / total * 100
            VariationClassificationCategoryPlot.objects.create(
                category=k, missense=missense, nonsense=nonsense,
                splice=splice, fsi=fsi, fsd=fsd, ifi=ifi, ifd=ifd,
                total=total, missense_rate=missense_rate,
                nonsense_rate=nonsense_rate, splice_rate=splice_rate,
                fsi_rate=fsi_rate, fsd_rate=fsd_rate, ifi_rate=ifi_rate,
                ifd_rate=ifd_rate
            )


def variant_type_category_plot(d):
    infos = {}
    for k in d:
        for c in d[k]:
            if c == 'NA':
                continue
            category = '_'.join([k, c])
            ic = infos[category] = {
                'snp': 0,
                'ins': 0,
                'dels': 0,
                'number': 0
            }
            for tsampleid in d[k][c]:
                try:
                    obj = VariantType.objects.get(tsampleid=tsampleid)
                    ic['snp'] += obj.snp
                    ic['ins'] += obj.ins
                    ic['dels'] += obj.dels
                    ic['number'] += 1
                except VariantType.DoesNotExist:
                    pass
    return infos


def create_or_update_variant_type_category_plot(d):
    for k in d:
        try:
            obj = VariantTypeCategoryPlot.objects.get(category=k)
            obj.tsample_num = d[k]['number']
            obj.snp = d[k]['snp']
            obj.ins = d[k]['ins']
            obj.dels = d[k]['dels']
            total = d[k]['snp'] + d[k]['ins'] + d[k]['dels']
            obj.total = total
            obj.snp_rate = d[k]['snp'] / total * 100
            obj.ins_rate = d[k]['ins'] / total * 100
            obj.del_rate = d[k]['dels'] / total * 100
            obj.save()
        except VariantTypeCategoryPlot.DoesNotExist:
            tsample_num = d[k]['number']
            snp = d[k]['snp']
            ins = d[k]['ins']
            dels = d[k]['dels']
            total = d[k]['snp'] + d[k]['ins'] + d[k]['dels']
            snp_rate = d[k]['snp'] / total * 100
            ins_rate = d[k]['ins'] / total * 100
            del_rate = d[k]['dels'] / total * 100
            VariantTypeCategoryPlot.objects.create(
                category=k, snp=snp, ins=ins, dels=dels,
                snp_rate=snp_rate, ins_rate=ins_rate,
                del_rate=del_rate, tsample_num=tsample_num
            )


def snv_class_category_plot(d):
    infos = {}
    for k in d:
        for c in d[k]:
            if c == 'NA':
                continue
            category = '_'.join([k, c])
            ic = infos[category] = {
                't2g': 0,
                't2a': 0,
                't2c': 0,
                'c2t': 0,
                'c2g': 0,
                'c2a': 0
            }
            for tsampleid in d[k][c]:
                try:
                    obj = SnvClass.objects.get(tsampleid=tsampleid)
                    ic['t2g'] += obj.t2g
                    ic['t2a'] += obj.t2a
                    ic['t2c'] += obj.t2c
                    ic['c2t'] += obj.c2t
                    ic['c2g'] += obj.c2g
                    ic['c2a'] += obj.c2a
                except SnvClass.DoesNotExist:
                    pass
    return infos


def create_or_update_snv_class_category_plot(d):
    for k in d:
        try:
            obj = SnvClassCategoryPlot.objects.get(category=k)
            obj.t2g = d[k]['t2g']
            obj.t2a = d[k]['t2a']
            obj.t2c = d[k]['t2c']
            obj.c2t = d[k]['c2t']
            obj.c2g = d[k]['c2g']
            obj.c2a = d[k]['c2a']
            total = d[k]['t2g'] + d[k]['t2a'] + d[k]['t2c'] + d[k]['c2t'] + d[k]['c2g'] + d[k]['c2a']
            obj.total = total
            obj.t2g_rate = d[k]['t2g'] / total * 100
            obj.t2a_rate = d[k]['t2a'] / total * 100
            obj.t2c_rate = d[k]['t2c'] / total * 100
            obj.c2t_rate = d[k]['c2t'] / total * 100
            obj.c2g_rate = d[k]['c2g'] / total * 100
            obj.c2a_rate = d[k]['c2a'] / total * 100
            obj.save()
        except SnvClassCategoryPlot.DoesNotExist:
            t2g = d[k]['t2g']
            t2a = d[k]['t2a']
            t2c = d[k]['t2c']
            c2t = d[k]['c2t']
            c2g = d[k]['c2g']
            c2a = d[k]['c2a']
            total = d[k]['t2g'] + d[k]['t2a'] + d[k]['t2c'] + d[k]['c2t'] + d[k]['c2g'] + d[k]['c2a']
            t2g_rate = d[k]['t2g'] / total * 100
            t2a_rate = d[k]['t2a'] / total * 100
            t2c_rate = d[k]['t2c'] / total * 100
            c2t_rate = d[k]['c2t'] / total * 100
            c2g_rate = d[k]['c2g'] / total * 100
            c2a_rate = d[k]['c2a'] / total * 100
            SnvClassCategoryPlot.objects.create(
                category=k, t2g=t2g, t2a=t2a,
                t2c=t2c, c2t=c2t, c2g=c2g, c2a=c2a,
                total=total, t2g_rate=t2g_rate,
                t2a_rate=t2a_rate, t2c_rate=t2c_rate,
                c2t_rate=c2t_rate, c2g_rate=c2g_rate,
                c2a_rate=c2a_rate
            )


def stat_from_maf(maf):
    d = {}
    with open(maf) as fp:
        reader = csv.DictReader(fp, delimiter='\t')
        for row in reader:
            tsampleid = row['Tumor_Sample_Barcode']
            # initialize sample stats
            if d.get(tsampleid) is None:
                dts = d[tsampleid] = {
                    'varclass': {
                        'missense': 0,
                        'nonsense': 0,
                        'splice': 0,
                        'fsi': 0,
                        'fsd': 0,
                        'ifi': 0,
                        'ifd': 0
                    },
                    'vartype': {
                        'snp': 0,
                        'ins': 0,
                        'del': 0
                    },
                    'snvclass': {
                        't2g': 0,
                        't2a': 0,
                        't2c': 0,
                        'c2t': 0,
                        'c2g': 0,
                        'c2a': 0
                    },
                    'mutgenes': {}
                }
            else:
                dts = d[tsampleid]
            # mutgene
            if row['Hugo_Symbol'] not in ['.', 'Unknown']:
                # initialize gene stats
                if dts['mutgenes'].get(row['Hugo_Symbol']) is None:
                    dtsmg = dts['mutgenes'][row['Hugo_Symbol']] = {
                        'varclass': [],
                        'vartype': {
                            'snp': 0,
                            'ins': 0,
                            'del': 0
                        },
                        'snvclass': {
                            't2g': 0,
                            't2a': 0,
                            't2c': 0,
                            'c2t': 0,
                            'c2g': 0,
                            'c2a': 0
                        }
                    }
                else:
                    dtsmg = dts['mutgenes'][row['Hugo_Symbol']]
                # start stat
                # varclass
                tmp = row['Variant_Classification']
                varclass_tmp = {
                    'missense': 0,
                    'nonsense': 0,
                    'splice': 0,
                    'fsi': 0,
                    'fsd': 0,
                    'ifi': 0,
                    'ifd': 0,
                    'maf': 0.0,
                    'aachange': '',
                }
                # mutation rate
                try:
                    rate = float(row['t_alt_count']) / float(row['t_depth'])
                except Exception:
                    rate = 0.0
                varclass_tmp['maf'] = rate
                # aachange
                varclass_tmp['aachange'] = row['AAchange']
                if tmp == 'Missense_Mutation':
                    dts['varclass']['missense'] += 1
                    varclass_tmp['missense'] = 1
                elif tmp == 'Nonsense_Mutation':
                    dts['varclass']['nonsense'] += 1
                    varclass_tmp['nonsense'] = 1
                elif tmp == 'Splice_Region':
                    dts['varclass']['splice'] += 1
                    varclass_tmp['splice'] = 1
                elif tmp == 'Frame_Shift_Ins':
                    dts['varclass']['fsi'] += 1
                    varclass_tmp['fsi'] = 1
                elif tmp == 'Frame_Shift_Del':
                    dts['varclass']['fsd'] += 1
                    varclass_tmp['fsd'] = 1
                elif tmp == 'In_Frame_Ins':
                    dts['varclass']['ifi'] += 1
                    varclass_tmp['ifi'] = 1
                elif tmp == 'In_Frame_Del':
                    dts['varclass']['ifd'] += 1
                    varclass_tmp['ifd'] = 1
                else:
                    pass
                dtsmg['varclass'].append(varclass_tmp)
                # vartype
                tmp = row['Variant_Type']
                if tmp == 'SNP':
                    dts['vartype']['snp'] += 1
                    dtsmg['vartype']['snp'] += 1
                    # snvclass
                    bn, bt = row['Reference_Allele'], row['Tumor_Seq_Allele2']
                    snvcls = '%s2%s' % (bn.lower(), bt.lower())
                    if dts['snvclass'].get(snvcls) is not None:
                        dts['snvclass'][snvcls] += 1
                        dtsmg['snvclass'][snvcls] += 1
                elif tmp == 'INS':
                    dts['vartype']['ins'] += 1
                    dtsmg['vartype']['ins'] += 1
                elif tmp == 'DEL':
                    dts['vartype']['del'] += 1
                    dtsmg['vartype']['del'] += 1
                else:
                    pass
            else:
                # varclass
                tmp = row['Variant_Classification']
                if tmp == 'Missense_Mutation':
                    dts['varclass']['missense'] += 1
                elif tmp == 'Nonsense_Mutation':
                    dts['varclass']['nonsense'] += 1
                elif tmp == 'Splice_Region':
                    dts['varclass']['splice'] += 1
                elif tmp == 'Frame_Shift_Ins':
                    dts['varclass']['fsi'] += 1
                elif tmp == 'Frame_Shift_Del':
                    dts['varclass']['fsd'] += 1
                elif tmp == 'In_Frame_Ins':
                    dts['varclass']['ifi'] += 1
                elif tmp == 'In_Frame_Del':
                    dts['varclass']['ifd'] += 1
                else:
                    pass
                # vartype
                tmp = row['Variant_Type']
                if tmp == 'SNP':
                    dts['vartype']['snp'] += 1
                    # snvclass
                    bn, bt = row['Reference_Allele'], row['Tumor_Seq_Allele2']
                    snvcls = '%s2%s' % (bn.lower(), bt.lower())
                    if dts['snvclass'].get(snvcls) is not None:
                        dts['snvclass'][snvcls] += 1
                elif tmp == 'INS':
                    dts['vartype']['ins'] += 1
                elif tmp == 'DEL':
                    dts['vartype']['del'] += 1
                else:
                    pass
    return d


def create_or_update_maf(d):
    for k in d:
        try:
            tsampleid = k.replace('_NT', '_T1')
            tsampleinfo = TumorSampleQC.objects.get(tsampleid=tsampleid)  # cautions: k != tumor sampleid
        except TumorSampleQC.DoesNotExist:
            try:
                tsampleid = k.replace('_NT', '_T2')
                tsampleinfo = TumorSampleQC.objects.get(tsampleid=tsampleid)
            except TumorSampleQC.DoesNotExist:
                print('tumor sample qc missing: TumorSampleQC tsampleid<%s>, SnvRecord Tumor_Sample_Barcode<%s>.' % (k.replace('_NT', '_T1'), k))
                continue
        # Variation Classification
        try:
            obj = VariationClassification.objects.get(tsampleid=tsampleid)
            obj.missense = d[k]['varclass']['missense']
            obj.nonsense = d[k]['varclass']['nonsense']
            obj.splice = d[k]['varclass']['splice']
            obj.fsi = d[k]['varclass']['fsi']
            obj.fsd = d[k]['varclass']['fsd']
            obj.ifi = d[k]['varclass']['ifi']
            obj.ifd = d[k]['varclass']['ifd']
            obj.save()
        except VariationClassification.DoesNotExist:
            VariationClassification.objects.create(
                tsampleinfo=tsampleinfo, tsampleid=tsampleid,
                missense=d[k]['varclass']['missense'],
                nonsense=d[k]['varclass']['nonsense'],
                splice=d[k]['varclass']['splice'],
                fsi=d[k]['varclass']['fsi'],
                fsd=d[k]['varclass']['fsd'],
                ifi=d[k]['varclass']['ifi'],
                ifd=d[k]['varclass']['ifd']
            )
        # Variant Type
        try:
            obj = VariantType.objects.get(tsampleid=tsampleid)
            obj.snp = d[k]['vartype']['snp']
            obj.ins = d[k]['vartype']['ins']
            obj.dels = d[k]['vartype']['del']
            obj.save()
        except VariantType.DoesNotExist:
            VariantType.objects.create(
                tsampleinfo=tsampleinfo, tsampleid=tsampleid,
                snp=d[k]['vartype']['snp'],
                ins=d[k]['vartype']['ins'],
                dels=d[k]['vartype']['del']
            )
        # Snv Class
        try:
            obj = SnvClass.objects.get(tsampleid=tsampleid)
            obj.t2g = d[k]['snvclass']['t2g']
            obj.t2a = d[k]['snvclass']['t2a']
            obj.t2c = d[k]['snvclass']['t2c']
            obj.c2t = d[k]['snvclass']['c2t']
            obj.c2g = d[k]['snvclass']['c2g']
            obj.c2a = d[k]['snvclass']['c2a']
            obj.save()
        except SnvClass.DoesNotExist:
            SnvClass.objects.create(
                tsampleinfo=tsampleinfo, tsampleid=tsampleid,
                t2g=d[k]['snvclass']['t2g'],
                t2a=d[k]['snvclass']['t2a'],
                t2c=d[k]['snvclass']['t2c'],
                c2t=d[k]['snvclass']['c2t'],
                c2g=d[k]['snvclass']['c2g'],
                c2a=d[k]['snvclass']['c2a']
            )
        # mutated genes
        dsm = d[k]['mutgenes']
        for gene in dsm:
            # Mutated Genes
            try:
                obj = MutatedGenes.objects.get(tsampleid=tsampleid, symbol=gene)
            except MutatedGenes.DoesNotExist:
                MutatedGenes.objects.create(
                    tsampleinfo=tsampleinfo, tsampleid=tsampleid, symbol=gene
                )
            mutgeneinfo = MutatedGenes.objects.get(tsampleid=tsampleid, symbol=gene)
            # Variation Classification
            for varclass in dsm[gene]['varclass']:
                GeneVariationClassification.objects.get_or_create(
                    mutgeneinfo=mutgeneinfo, tsampleid=tsampleid, symbol=gene,
                    missense=varclass['missense'],
                    nonsense=varclass['nonsense'],
                    splice=varclass['splice'],
                    fsi=varclass['fsi'],
                    fsd=varclass['fsd'],
                    ifi=varclass['ifi'],
                    ifd=varclass['ifd'],
                    maf=varclass['maf'],
                    aachange=varclass['aachange']
                )
            # Variant Type
            try:
                obj = GeneVariantType.objects.get(tsampleid=tsampleid, symbol=gene)
                obj.snp = dsm[gene]['vartype']['snp']
                obj.ins = dsm[gene]['vartype']['ins']
                obj.dels = dsm[gene]['vartype']['del']
                obj.save()
            except GeneVariantType.DoesNotExist:
                GeneVariantType.objects.create(
                    mutgeneinfo=mutgeneinfo, tsampleid=tsampleid, symbol=gene,
                    snp=dsm[gene]['vartype']['snp'],
                    ins=dsm[gene]['vartype']['ins'],
                    dels=dsm[gene]['vartype']['del']
                )
            # Snv Class
            try:
                obj = GeneSnvClass.objects.get(tsampleid=tsampleid, symbol=gene)
                obj.t2g = dsm[gene]['snvclass']['t2g']
                obj.t2a = dsm[gene]['snvclass']['t2a']
                obj.t2c = dsm[gene]['snvclass']['t2c']
                obj.c2t = dsm[gene]['snvclass']['c2t']
                obj.c2g = dsm[gene]['snvclass']['c2g']
                obj.c2a = dsm[gene]['snvclass']['c2a']
                obj.save()
            except GeneSnvClass.DoesNotExist:
                GeneSnvClass.objects.create(
                    mutgeneinfo=mutgeneinfo, tsampleid=tsampleid, symbol=gene,
                    t2g=dsm[gene]['snvclass']['t2g'],
                    t2a=dsm[gene]['snvclass']['t2a'],
                    t2c=dsm[gene]['snvclass']['t2c'],
                    c2t=dsm[gene]['snvclass']['c2t'],
                    c2g=dsm[gene]['snvclass']['c2g'],
                    c2a=dsm[gene]['snvclass']['c2a']
                )


def get_data():
    pass
