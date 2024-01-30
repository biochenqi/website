import csv
import json
import os
import re
import time

from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import (
    ProteinDomainsDB, Hgnc2PfamDB,
    SampleClinicInfo, TumorSampleQC, NormalSampleQC,
    VariationClassification, VariantType,
    SnvClass, GeneVariationClassification,
    SortedGeneVariationClassification
)
from .get_data import (
    index_data, variation_data,
    sampleinfo_data, category_data,
    sampletab_initialize, sampletab_data
)


# LANGUAGES = (
#     ('en-us', _('English')),
#     ('zh-hans', _('Chinese')),
# )
LANGUAGES = settings.LANGUAGES


# Create your views here.
def index(request):
    infos = index_data()

    return render(request, 'cccga/index.html', {'infos': infos, "LANGUAGES": LANGUAGES})


def workflow(request):
    return render(request, 'cccga/workflow.html', {"LANGUAGES": LANGUAGES})


def sampleqc(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'search':
            kwargs = {}
            barcode = request.POST.get('barcode').strip()
            if barcode:
                kwargs['barcode'] = barcode.split('_')[0] + '_NT'
            pathological_stage = request.POST.get('patho-stage').strip()
            if pathological_stage:
                kwargs['pathological_stage'] = pathological_stage
            primary_location = request.POST.get('pri-loc').strip()
            if primary_location:
                kwargs['primary_location'] = primary_location
            detailed_site = request.POST.get('det-site').strip()
            if detailed_site:
                kwargs['detailed_site'] = detailed_site
            infos = sampleinfo_data(**kwargs)
        elif request.POST.get('action') == 'reset':
            infos = sampleinfo_data()
    else:
        infos = sampleinfo_data()

    return render(request, 'cccga/sampleqc.html', {'infos': infos, "LANGUAGES": LANGUAGES})


def sampletab(request):
    infos = sampletab_initialize()

    return render(request, 'cccga/sampleqc.html', {'infos': infos, "LANGUAGES": LANGUAGES})


def sampletab_ajax(request):
    if request.method == 'POST':
        reqd = request.POST
        # print(reqd)
        # print(len(reqd.get('order')))
        # filter
        kwargs = {}
        barcode = reqd.get('columns[1][search][value]').strip()
        if barcode:
            kwargs['barcode'] = barcode.split('_')[0] + '_NT'
        pathological_stage = reqd.get('columns[5][search][value]').strip()
        if pathological_stage:
            kwargs['pathological_stage'] = pathological_stage
        primary_location = reqd.get('columns[6][search][value]').strip()
        if primary_location:
            kwargs['primary_location'] = primary_location
        detailed_site = reqd.get('columns[7][search][value]').strip()
        if detailed_site:
            kwargs['detailed_site'] = detailed_site
        # print(kwargs)
        # order
        order = []
        order_column = reqd.get('order[0][column]', None)  # 注意多值排序
        if order_column is not None:
            order_field = reqd.get('columns[{}][data]'.format(order_column))
            order_way = reqd.get('order[0][dir]')  # 注意多值排序
            if order_way == 'asc':
                order.append('{}'.format(order_field))
            if order_way == 'desc':
                order.append('-{}'.format(order_field))
        else:
            # 默认排序
            order_field = reqd.get('columns[5][data]')
            order = ['{}'.format(order_field)]
        # page
        page_length = int(reqd.get('length', '25'))
        page_start = int(reqd.get('start', '0'))
        # get data
        sampleinfos, total_length = sampletab_data(page_start, page_length, tuple(order), **kwargs)
        infos = {"iTotalRecords": page_length}
        infos["sampleinfos"] = sampleinfos
        infos["iTotalDisplayRecords"] = total_length
    else:
        return HttpResponse(f'Invalid Request.')

    return JsonResponse(infos)


def sampleinfo_ajax(request):
    if request.method == 'GET':
        infotype = request.GET.get('infoType')
        sampleinfo = {}
        if infotype == 'clinic':
            barcode = request.GET.get('barcode')
            obj = SampleClinicInfo.objects.get(barcode=barcode)
            sampleinfo['barcode'] = obj.barcode
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
        elif infotype == 'tsampleqc':
            barcode = request.GET.get('barcode')
            obj = TumorSampleQC.objects.get(tsampleid=barcode)
            sampleinfo['tsampleid'] = obj.tsampleid
            sampleinfo['lib_type'] = obj.lib_type
            sampleinfo['rawsize'] = obj.rawsize
            sampleinfo['duplicate_rate'] = obj.duplicate_rate
            sampleinfo['foebot'] = obj.foebot
            sampleinfo['asdot'] = obj.asdot
            sampleinfo['cotr'] = obj.cotr
        elif infotype == 'nsampleqc':
            barcode = request.GET.get('barcode')
            obj = NormalSampleQC.objects.get(nsampleid=barcode)
            sampleinfo['nsampleid'] = obj.nsampleid
            sampleinfo['lib_type'] = obj.lib_type
            sampleinfo['rawsize'] = obj.rawsize
            sampleinfo['duplicate_rate'] = obj.duplicate_rate
            sampleinfo['foebot'] = obj.foebot
            sampleinfo['asdot'] = obj.asdot
            sampleinfo['cotr'] = obj.cotr

    return JsonResponse(sampleinfo)


class Echo:
    def write(self, value):
        return value


@csrf_exempt
def sampleinfo_export(request):
    if request.method == 'POST':
        contents = request.POST.get('contents')
        contents = contents.split(',')
        samples = request.POST.get('samples')
        samples = samples.split(',')
        infos = []
        time_stamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        for sample in samples:
            sampleinfo = {}
            barcode = sample
            tsampleid, nsampleid = '', ''
            if 'clinic' in contents:
                try:
                    obj = SampleClinicInfo.objects.get(barcode=barcode)
                    tsampleid, nsampleid = obj.tsampleid, obj.nsampleid
                except SampleClinicInfo.DoesNotExist:
                    obj = ''
                    tsampleid, nsampleid = '', ''
                sampleinfo['barcode'] = obj.barcode if obj else ''
                sampleinfo['gender'] = obj.gender if obj else ''
                sampleinfo['diagnosis_age'] = obj.diagnosis_age if obj else ''
                sampleinfo['surgery_date'] = obj.surgery_date.strftime('%Y-%m-%d') if (obj and obj.surgery_date) else ''
                sampleinfo['pathological_grade'] = obj.pathological_grade if obj else ''
                sampleinfo['pathological_stage'] = obj.pathological_stage if obj else ''
                sampleinfo['primary_tumor_location'] = obj.primary_location if obj else ''
                sampleinfo['detailed_tumor_site'] = obj.detailed_site if obj else ''
                sampleinfo['metastasis_at_diagnosis'] = obj.metastasis if obj else ''
                sampleinfo['time_from_diagnosis_to_death'] = obj.time_os if obj else ''
                sampleinfo['ajcc_T_stage'] = obj.ajcc_T_stage if obj else ''
                sampleinfo['ajcc_N_stage'] = obj.ajcc_N_stage if obj else ''
            if 'tumor' in contents:
                if not tsampleid:
                    try:
                        obj = SampleClinicInfo.objects.get(barcode=barcode)
                        tsampleid = obj.tsampleid
                    except SampleClinicInfo.DoesNotExist:
                        tsampleid = ''
                try:
                    obj = TumorSampleQC.objects.get(tsampleid=tsampleid)
                except TumorSampleQC.DoesNotExist:
                    obj = ''
                sampleinfo['tumor_sampleid'] = obj.tsampleid if obj else ''
                sampleinfo['tumor_library_type'] = obj.lib_type if obj else ''
                sampleinfo['tumor_raw_base_number(G)'] = obj.rawsize if obj else ''
                sampleinfo['tumor_duplicate_rate(%)'] = obj.duplicate_rate if obj else ''
                sampleinfo['tumor_fraction_of_effective_bases_on_target(%)'] = obj.foebot if obj else ''
                sampleinfo['tumor_average_sequencing_depth_on_target'] = obj.asdot if obj else ''
                sampleinfo['tumor_coverage_of_target_region(%)'] = obj.cotr if obj else ''
            if 'normal' in contents:
                if not nsampleid:
                    try:
                        obj = SampleClinicInfo.objects.get(barcode=barcode)
                        nsampleid = obj.nsampleid
                    except SampleClinicInfo.DoesNotExist:
                        tsampleid = ''
                try:
                    obj = NormalSampleQC.objects.get(nsampleid=nsampleid)
                except NormalSampleQC.DoesNotExist:
                    obj = ''
                sampleinfo['normal_sampleid'] = obj.nsampleid if obj else ''
                sampleinfo['normal_library_type'] = obj.lib_type if obj else ''
                sampleinfo['normal_raw_base_number(G)'] = obj.rawsize if obj else ''
                sampleinfo['normal_duplicate_rate(%)'] = obj.duplicate_rate if obj else ''
                sampleinfo['normal_fraction_of_effective_bases_on_target(%)'] = obj.foebot if obj else ''
                sampleinfo['normal_average_sequencing_depth_on_target'] = obj.asdot if obj else ''
                sampleinfo['normal_coverage_of_target_region(%)'] = obj.cotr if obj else ''
            infos.append(sampleinfo)
        tmpfp = os.path.join('tmp', 'export_%s.json' % time_stamp)
        with open(tmpfp, 'w') as jf:
            json.dump(infos, jf)
        return HttpResponse(time_stamp)
    else:
        fname = request.GET.get('fname')
        tmpfp = os.path.join('tmp', 'export_%s.json' % fname)
        with open(tmpfp, 'r') as jf:
            infos = json.load(jf)
        rows = []
        header = []
        for info in infos:
            if not header:
                header = [k for k in info]
                rows.append(header)
            # 开放前禁止下载
            # content = [info[k] for k in info]
            # rows.append(content)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment;filename="cccga_%s.csv"' % fname
        os.remove(tmpfp)
        return response
        # infos = {'filename': 'abc.csv'}
        # return JsonResponse({'infos': infos})


def sampleinfo_export_all(request):
    if request.method == 'POST':
        infos = []
        time_stamp = time.strftime("%Y-%m-%d_%H%M%S", time.localtime())
        objs = SampleClinicInfo.objects.all()
        for obj in objs:
            sampleinfo = {}
            sampleinfo['barcode'] = obj.barcode
            sampleinfo['gender'] = obj.gender
            sampleinfo['diagnosis_age'] = obj.diagnosis_age
            sampleinfo['surgery_date'] = obj.surgery_date.strftime('%Y-%m-%d') if obj.surgery_date else ''
            sampleinfo['pathological_grade'] = obj.pathological_grade
            sampleinfo['pathological_stage'] = obj.pathological_stage
            sampleinfo['primary_tumor_location'] = obj.primary_location
            sampleinfo['detailed_tumor_site'] = obj.detailed_site
            sampleinfo['metastasis_at_diagnosis'] = obj.metastasis
            sampleinfo['time_from_diagnosis_to_death'] = obj.time_os
            sampleinfo['ajcc_T_stage'] = obj.ajcc_T_stage
            sampleinfo['ajcc_N_stage'] = obj.ajcc_N_stage
            tsampleid = obj.tsampleid
            try:
                obj_t = TumorSampleQC.objects.get(tsampleid=tsampleid)
            except TumorSampleQC.DoesNotExist:
                obj_t = ''
            sampleinfo['tumor_sampleid'] = obj_t.tsampleid if obj_t else ''
            sampleinfo['tumor_library_type'] = obj_t.lib_type if obj_t else ''
            sampleinfo['tumor_raw_base_number(G)'] = obj_t.rawsize if obj_t else ''
            sampleinfo['tumor_duplicate_rate(%)'] = obj_t.duplicate_rate if obj_t else ''
            sampleinfo['tumor_fraction_of_effective_bases_on_target(%)'] = obj_t.foebot if obj_t else ''
            sampleinfo['tumor_average_sequencing_depth_on_target'] = obj_t.asdot if obj_t else ''
            sampleinfo['tumor_coverage_of_target_region(%)'] = obj_t.cotr if obj_t else ''
            nsampleid = obj.nsampleid
            try:
                obj_n = NormalSampleQC.objects.get(nsampleid=nsampleid)
            except NormalSampleQC.DoesNotExist:
                obj_n = ''
            sampleinfo['normal_sampleid'] = obj_n.nsampleid if obj_n else ''
            sampleinfo['normal_library_type'] = obj_n.lib_type if obj_n else ''
            sampleinfo['normal_raw_base_number(G)'] = obj_n.rawsize if obj_n else ''
            sampleinfo['normal_duplicate_rate(%)'] = obj_n.duplicate_rate if obj_n else ''
            sampleinfo['normal_fraction_of_effective_bases_on_target(%)'] = obj_n.foebot if obj_n else ''
            sampleinfo['normal_average_sequencing_depth_on_target'] = obj_n.asdot if obj_n else ''
            sampleinfo['normal_coverage_of_target_region(%)'] = obj_n.cotr if obj_n else ''
            infos.append(sampleinfo)
        tmpfp = os.path.join('tmp', 'export_%s.json' % time_stamp)
        with open(tmpfp, 'w') as jf:
            json.dump(infos, jf)
        return HttpResponse(time_stamp)
    else:
        fname = request.GET.get('fname')
        tmpfp = os.path.join('tmp', 'export_%s.json' % fname)
        with open(tmpfp, 'r') as jf:
            infos = json.load(jf)
        rows = []
        header = []
        for info in infos:
            if not header:
                header = [k for k in info]
                rows.append(header)
            # 开放前禁止下载
            # content = [info[k] for k in info]
            # rows.append(content)
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
        response['Content-Disposition'] = 'attachment;filename="cccga_%s.csv"' % fname
        os.remove(tmpfp)
        return response


def variation(request):
    infos = variation_data()

    return render(request, 'cccga/variation.html', {'infos': infos, "LANGUAGES": LANGUAGES})


def category(request):
    infos = category_data()

    return render(request, 'cccga/category.html', {'infos': infos, "LANGUAGES": LANGUAGES})


def query_gene(request):
    svgd = {}
    err_msgs = []
    if request.method == 'POST':
        query_content = request.POST.get('query_content').strip()
        if not query_content:
            err_msgs.append('Please input gene name, such as: "EGFR"')
        else:
            # get aachange from samples
            objs = GeneVariationClassification.objects.filter(symbol=query_content)
            if not objs:
                err_msgs.append('No matching records found. <GeneVariationClassification><%s>' % query_content)
            else:
                aachange_d = {}
                for obj in objs:
                    if obj.aachange.strip() in ['.', '']:
                        continue
                    # obj.aachange
                    # PTPRN:NM_001199763:exon2:c.T139C:p.C47R,PTPRN:NM_002846:exon2:c.T139C:p.C47R
                    # SPTB:NM_001024858:exon32:c.A6350G:p.E2117G,SPTB:NM_001355436:exon33:c.A6350G:p.E2117G
                    for a in obj.aachange.split(','):
                        if a in ['.', '']:
                            continue
                        if a.split(':')[0] != query_content:
                            continue
                        try:
                            refseqid = a.split(':')[1]
                            change = a.split(':')[-1]
                            pos = re.findall('\d+', change)[0]
                        except Exception:
                            continue
                        # missense,nonsense,splice,fsi,fsd,ifi,ifd,mh,other=0,1,2,3,4,5,6,7,8
                        if obj.missense != 0:
                            varclass_flag = 0
                        elif obj.nonsense != 0:
                            varclass_flag = 1
                        elif obj.splice != 0:
                            varclass_flag = 2
                        elif obj.fsi != 0:
                            varclass_flag = 3
                        elif obj.fsd != 0:
                            varclass_flag = 4
                        elif obj.ifi != 0:
                            varclass_flag = 5
                        elif obj.ifd != 0:
                            varclass_flag = 6
                        else:
                            varclass_flag = 8
                        if aachange_d.get(refseqid) is None:
                            aachange_d[refseqid] = {change: [pos, 1, varclass_flag]}
                        else:
                            if aachange_d[refseqid].get(change) is None:
                                aachange_d[refseqid][change] = [pos, 1, varclass_flag]
                            else:
                                aachange_d[refseqid][change][1] += 1
                                if aachange_d[refseqid][change][2] != varclass_flag:
                                    aachange_d[refseqid][change][2] = 7
                    else:
                        continue
                # get all aa information from protein domains database
                aainfo_objs = ProteinDomainsDB.objects.filter(hgnc=query_content)
                if not aainfo_objs:
                    err_msgs.append('No matching records found. <ProteinDomainsDB><%s>' % query_content)
                else:
                    aainfo_d = {}
                    for obj in aainfo_objs:
                        if aainfo_d.get(obj.refseq_id) is None:
                            aainfo_d[obj.refseq_id] = {
                                'protein_id': obj.protein_id,
                                'length': obj.aa_length,
                                'domains': [[obj.start, obj.end, obj.label]]
                            }
                        else:
                            aainfo_d[obj.refseq_id]['domains'].append([obj.start, obj.end, obj.label])
                    # get aa information for query_content
                    svgd = {}
                    for refseqid in aachange_d:
                        if aainfo_d.get(refseqid) is None:
                            # err_msgs.append('No matching records found. <ProteinDomainsDB: %s><%s>' % (refseqid, query_content))
                            pass
                        else:
                            if svgd.get('refseqid') is None:
                                svgd['gene'] = query_content
                                svgd['panelhead'] = _('Amino Acid Changes for %(gene)s') % {'gene': query_content}
                                svgd['refseqid'] = refseqid
                                svgd['proteinid'] = aainfo_d[refseqid]['protein_id']
                                svgd['length'] = aainfo_d[refseqid]['length']
                                svgd['domains'] = aainfo_d[refseqid]['domains']
                                svgd['changes'] = aachange_d[refseqid]
                            else:
                                if aainfo_d[refseqid]['length'] > svgd['length']:
                                    svgd['refseqid'] = refseqid
                                    svgd['proteinid'] = aainfo_d[refseqid]['protein_id']
                                    svgd['length'] = aainfo_d[refseqid]['length']
                                    svgd['domains'] = aainfo_d[refseqid]['domains']
                                    svgd['changes'] = aachange_d[refseqid]
                    if not svgd:
                        err_msgs.append('No matching records found. <ProteinDomainsDB><%s>' % query_content)
                    else:
                        tmp = []
                        for change in svgd['changes']:
                            tmp.append(svgd['changes'][change][1])
                        svgd['max'] = max(tmp)
                        try:
                            obj = SortedGeneVariationClassification.objects.get(symbol=query_content)
                            svgd['rate'] = '%.2f' % obj.tsample_num_rate
                        except SortedGeneVariationClassification.DoesNotExist:
                            err_msgs.append('No matching records found. <SortedGeneVariationClassification><%s>' % query_content)
                            svgd['rate'] = 0.0
    else:
        pass

    return render(request, 'cccga/query_gene.html', {'err_msgs': err_msgs, 'aa': svgd, "LANGUAGES": LANGUAGES})


def query_gene_vep(request):
    svgd = {}
    err_msgs = []
    if request.method == 'POST':
        query_content = request.POST.get('query_content').strip()
        if not query_content:
            err_msgs.append('Please input gene name, such as: "EGFR"')
        else:
            # get aachange from samples
            objs = GeneVariationClassification.objects.filter(symbol=query_content)
            if not objs:
                err_msgs.append('No matching records found in GeneVariationClassification.<%s>' % query_content)
            else:
                aachange_d = {}
                for obj in objs:
                    if obj.aachange.strip() in ['.', '']:
                        continue
                    # obj.aachange
                    # p.P1417_R1418insQLFEVCLET
                    for a in obj.aachange.split(','):
                        if a in ['.', '']:
                            continue
                        try:
                            # refseqid = a.split(':')[1]
                            change = a
                            pos = re.findall('\d+', change)[0]
                        except Exception:
                            continue
                        # missense,nonsense,splice,fsi,fsd,ifi,ifd,mh,other=0,1,2,3,4,5,6,7,8
                        if obj.missense != 0:
                            varclass_flag = 0
                        elif obj.nonsense != 0:
                            varclass_flag = 1
                        elif obj.splice != 0:
                            varclass_flag = 2
                        elif obj.fsi != 0:
                            varclass_flag = 3
                        elif obj.fsd != 0:
                            varclass_flag = 4
                        elif obj.ifi != 0:
                            varclass_flag = 5
                        elif obj.ifd != 0:
                            varclass_flag = 6
                        else:
                            varclass_flag = 8
                        if aachange_d.get(change) is None:
                            aachange_d[change] = [pos, 1, varclass_flag]
                        else:
                            aachange_d[change][1] += 1
                            if aachange_d[change][2] != varclass_flag:
                                aachange_d[change][2] = 7
                    else:
                        continue
                # get all aa information from protein domains database
                aainfo_objs = Hgnc2PfamDB.objects.filter(hgnc=query_content)
                if not aainfo_objs:
                    err_msgs.append('No matching records found in Hgnc2PfamDB.<%s>' % query_content)
                else:
                    aainfo_d = {}
                    for obj in aainfo_objs:
                        if aainfo_d.get(obj.hgnc) is None:
                            aainfo_d[obj.hgnc] = {
                                'length': obj.aa_length,
                                'domains': [[obj.start, obj.end, obj.hmm_name]]
                            }
                        else:
                            aainfo_d[obj.hgnc]['domains'].append([obj.start, obj.end, obj.hmm_name])
                    # get aa information for query_content
                    svgd = {}
                    svgd['gene'] = query_content
                    svgd['panelhead'] = _('Amino Acid Changes for %(gene)s') % {'gene': query_content}
                    svgd['refseqid'] = ''
                    svgd['proteinid'] = ''
                    svgd['length'] = aainfo_d[query_content]['length']
                    svgd['domains'] = aainfo_d[query_content]['domains']
                    svgd['changes'] = aachange_d
                    tmp = []
                    for change in svgd['changes']:
                        tmp.append(svgd['changes'][change][1])
                    svgd['max'] = max(tmp)
                    try:
                        obj = SortedGeneVariationClassification.objects.get(symbol=query_content)
                        svgd['rate'] = '%.2f' % obj.tsample_num_rate
                    except SortedGeneVariationClassification.DoesNotExist:
                        err_msgs.append('No matching records found in SortedGeneVariationClassification.<%s>' % query_content)
                        svgd['rate'] = 'NA'
    else:
        pass

    return render(request, 'cccga/query_gene.html', {'err_msgs': err_msgs, 'aa': svgd, "LANGUAGES": LANGUAGES})


def querygene(request):

    return render(request, 'cccga/query_gene.html', {"LANGUAGES": LANGUAGES})


def querygene_ajax(request):
    if request.method == 'POST':
        infos = {
            'svgd': {},
            'err_msgs': []
        }
        svgd = infos['svgd']
        err_msgs = infos['err_msgs']
        query_content = request.POST.get('genename').strip()
        if not query_content:
            err_msgs.append('Please input gene name, such as: "EGFR"')
        else:
            # get aachange from samples
            objs = GeneVariationClassification.objects.filter(symbol=query_content)
            if not objs:
                # err_msgs.append('No matching records found. <GeneVariationClassification><%s>' % query_content)
                err_msgs.append('No matching records found. #%s' % query_content)
            else:
                aachange_d = {}
                for obj in objs:
                    if obj.aachange.strip() in ['.', '']:
                        continue
                    # obj.aachange
                    # PTPRN:NM_001199763:exon2:c.T139C:p.C47R,PTPRN:NM_002846:exon2:c.T139C:p.C47R
                    # SPTB:NM_001024858:exon32:c.A6350G:p.E2117G,SPTB:NM_001355436:exon33:c.A6350G:p.E2117G
                    for a in obj.aachange.split(','):
                        if a in ['.', '']:
                            continue
                        if a.split(':')[0] != query_content:
                            continue
                        try:
                            refseqid = a.split(':')[1]
                            change = a.split(':')[-1]
                            pos = re.findall('\d+', change)[0]
                        except Exception:
                            continue
                        # missense,nonsense,splice,fsi,fsd,ifi,ifd,mh,other=0,1,2,3,4,5,6,7,8
                        if obj.missense != 0:
                            varclass_flag = 0
                        elif obj.nonsense != 0:
                            varclass_flag = 1
                        elif obj.splice != 0:
                            varclass_flag = 2
                        elif obj.fsi != 0:
                            varclass_flag = 3
                        elif obj.fsd != 0:
                            varclass_flag = 4
                        elif obj.ifi != 0:
                            varclass_flag = 5
                        elif obj.ifd != 0:
                            varclass_flag = 6
                        else:
                            varclass_flag = 8
                        if aachange_d.get(refseqid) is None:
                            aachange_d[refseqid] = {change: [pos, 1, varclass_flag]}
                        else:
                            if aachange_d[refseqid].get(change) is None:
                                aachange_d[refseqid][change] = [pos, 1, varclass_flag]
                            else:
                                aachange_d[refseqid][change][1] += 1
                                if aachange_d[refseqid][change][2] != varclass_flag:
                                    aachange_d[refseqid][change][2] = 7
                    else:
                        continue
                # get all aa information from protein domains database
                aainfo_objs = ProteinDomainsDB.objects.filter(hgnc=query_content)
                if not aainfo_objs:
                    err_msgs.append('No matching records found in ProteinDomainsDB. #%s' % query_content)
                else:
                    aainfo_d = {}
                    for obj in aainfo_objs:
                        if aainfo_d.get(obj.refseq_id) is None:
                            aainfo_d[obj.refseq_id] = {
                                'protein_id': obj.protein_id,
                                'length': obj.aa_length,
                                'domains': [[obj.start, obj.end, obj.label]]
                            }
                        else:
                            aainfo_d[obj.refseq_id]['domains'].append([obj.start, obj.end, obj.label])
                    # get aa information for query_content
                    svgd = infos['svgd']
                    for refseqid in aachange_d:
                        if aainfo_d.get(refseqid) is None:
                            # err_msgs.append('No matching records found. <ProteinDomainsDB: %s><%s>' % (refseqid, query_content))
                            pass
                        else:
                            if svgd.get('refseqid') is None:
                                svgd['gene'] = query_content
                                svgd['panelhead'] = _('Amino Acid Changes for %(gene)s') % {'gene': query_content}
                                svgd['refseqid'] = refseqid
                                svgd['proteinid'] = aainfo_d[refseqid]['protein_id']
                                svgd['length'] = aainfo_d[refseqid]['length']
                                svgd['domains'] = aainfo_d[refseqid]['domains']
                                svgd['changes'] = aachange_d[refseqid]
                            else:
                                if aainfo_d[refseqid]['length'] > svgd['length']:
                                    svgd['refseqid'] = refseqid
                                    svgd['proteinid'] = aainfo_d[refseqid]['protein_id']
                                    svgd['length'] = aainfo_d[refseqid]['length']
                                    svgd['domains'] = aainfo_d[refseqid]['domains']
                                    svgd['changes'] = aachange_d[refseqid]
                    if not svgd:
                        err_msgs.append('No matching records found. <ProteinDomainsDB><%s>' % query_content)
                    else:
                        tmp = []
                        for change in svgd['changes']:
                            tmp.append(svgd['changes'][change][1])
                        svgd['max'] = max(tmp)
                        try:
                            obj = SortedGeneVariationClassification.objects.get(symbol=query_content)
                            svgd['rate'] = '%.2f' % obj.tsample_num_rate
                        except SortedGeneVariationClassification.DoesNotExist:
                            # err_msgs.append('No matching records found. <SortedGeneVariationClassification><%s>' % query_content)
                            svgd['rate'] = 0.0
    else:
        pass

    return JsonResponse(infos)


def querygene_vep_ajax(request):
    if request.method == 'POST':
        infos = {
            'svgd': {},
            'err_msgs': []
        }
        svgd = infos['svgd']
        err_msgs = infos['err_msgs']
        query_content = request.POST.get('genename').strip()
        if not query_content:
            err_msgs.append('Please input gene name, such as: "EGFR"')
        else:
            # get aachange from samples
            objs = GeneVariationClassification.objects.filter(symbol=query_content)
            if not objs:
                err_msgs.append('No matching records found. <GeneVariationClassification><%s>' % query_content)
            else:
                aachange_d = {}
                for obj in objs:
                    if obj.aachange.strip() in ['.', '']:
                        continue
                    # obj.aachange
                    # p.P1417_R1418insQLFEVCLET
                    for a in obj.aachange.split(','):
                        if a in ['.', '']:
                            continue
                        try:
                            # refseqid = a.split(':')[1]
                            change = a
                            pos = re.findall('\d+', change)[0]
                        except Exception:
                            continue
                        # missense,nonsense,splice,fsi,fsd,ifi,ifd,mh,other=0,1,2,3,4,5,6,7,8
                        if obj.missense != 0:
                            varclass_flag = 0
                        elif obj.nonsense != 0:
                            varclass_flag = 1
                        elif obj.splice != 0:
                            varclass_flag = 2
                        elif obj.fsi != 0:
                            varclass_flag = 3
                        elif obj.fsd != 0:
                            varclass_flag = 4
                        elif obj.ifi != 0:
                            varclass_flag = 5
                        elif obj.ifd != 0:
                            varclass_flag = 6
                        else:
                            varclass_flag = 8
                        if aachange_d.get(change) is None:
                            aachange_d[change] = [pos, 1, varclass_flag]
                        else:
                            aachange_d[change][1] += 1
                            if aachange_d[change][2] != varclass_flag:
                                aachange_d[change][2] = 7
                    else:
                        continue
                # get all aa information from protein domains database
                aainfo_objs = Hgnc2PfamDB.objects.filter(hgnc=query_content)
                if not aainfo_objs:
                    err_msgs.append('No matching records found. <Hgnc2PfamDB><%s>' % query_content)
                else:
                    aainfo_d = {}
                    for obj in aainfo_objs:
                        if aainfo_d.get(obj.hgnc) is None:
                            aainfo_d[obj.hgnc] = {
                                'length': obj.aa_length,
                                'domains': [[obj.start, obj.end, obj.hmm_name]]
                            }
                        else:
                            aainfo_d[obj.hgnc]['domains'].append([obj.start, obj.end, obj.hmm_name])
                    # get aa information for query_content
                    svgd['gene'] = query_content
                    svgd['panelhead'] = _('Amino Acid Changes for %(gene)s') % {'gene': query_content}
                    svgd['refseqid'] = ''
                    svgd['proteinid'] = ''
                    svgd['length'] = aainfo_d[query_content]['length']
                    svgd['domains'] = aainfo_d[query_content]['domains']
                    svgd['changes'] = aachange_d
                    tmp = []
                    for change in svgd['changes']:
                        tmp.append(svgd['changes'][change][1])
                    svgd['max'] = max(tmp)
                    try:
                        obj = SortedGeneVariationClassification.objects.get(symbol=query_content)
                        svgd['rate'] = '%.2f' % (obj.tsample_num_rate * 100)
                    except SortedGeneVariationClassification.DoesNotExist:
                        err_msgs.append('No matching records found. <SortedGeneVariationClassification><%s>' % query_content)
                        svgd['rate'] = 'NA'
    else:
        pass

    return JsonResponse(infos)


def query_sample(request):
    infos = {}
    err_msgs = []
    if request.method == 'POST':
        query_content = request.POST.get('query_content').strip()
        if not query_content:
            err_msgs.append('Please input tumor sample barcode, such as: "CRC666_T1"')
        else:
            infos['tsampleid'] = query_content
            # varclass
            try:
                obj = VariationClassification.objects.get(tsampleid=query_content)
                infos['varclass'] = {
                    'name': ['In_Frame_Del', 'In_Frame_Ins', 'Frame_Shift_Del', 'Frame_Shift_Ins', 'Splice_Region', 'Nonsense_Mutation', 'Missense_Mutation'],
                    'value': [obj.ifd, obj.ifi, obj.fsd, obj.fsi, obj.splice, obj.nonsense, obj.missense]
                }
            except VariationClassification.DoesNotExist:
                err_msgs.append('No matching records found. <VariationClassification><%s>' % query_content)
                infos = {}
            # vartype
            try:
                obj = VariantType.objects.get(tsampleid=query_content)
                infos['vartype'] = {
                    'name': ['DEL', 'INS', 'SNP'],
                    'value': [obj.dels, obj.ins, obj.snp]
                }
            except VariantType.DoesNotExist:
                err_msgs.append('No matching records found. <VariantType><%s>' % query_content)
                infos = {}
            # snvclass
            try:
                obj = SnvClass.objects.get(tsampleid=query_content)
                infos['snvclass'] = {
                    'name': ['T>G', 'T>A', 'T>C', 'C>T', 'C>G', 'C>A'][::-1],
                    'value': [obj.t2g, obj.t2a, obj.t2c, obj.c2t, obj.c2g, obj.c2a]
                }
            except SnvClass.DoesNotExist:
                err_msgs.append('No matching records found. <SnvClass><%s>' % query_content)
                infos = {}
            # 群体top 10 gene在该样本中的表现
            top_gene_list = list(range(10))
            itg = infos['topgenes'] = {
                'name': ['' for x in top_gene_list],
                'sample_number': [0.0 for x in top_gene_list],
                'max': 0,
                'missense': [0.0 for x in top_gene_list],
                'nonsense': [0.0 for x in top_gene_list],
                'splice': [0.0 for x in top_gene_list],
                'fsi': [0.0 for x in top_gene_list],
                'fsd': [0.0 for x in top_gene_list],
                'ifi': [0.0 for x in top_gene_list],
                'ifd': [0.0 for x in top_gene_list]
            }
            objs = SortedGeneVariationClassification.objects.all()[:10]
            itg['max'] = objs[0].tsample_num_rate
            itg['max'] = itg['max'] + itg['max'] * 5 // 100
            for i in range(10):
                obj = objs[9 - i]
                itg['name'][i] = obj.symbol
                itg['sample_number'][i] = '%.2f' % (obj.tsample_num_rate)
                _objs = GeneVariationClassification.objects.filter(tsampleid=query_content, symbol=obj.symbol)
                _missense, _nonsense, _splice, _fsi, _fsd, _ifi, _ifd, _total = 0, 0, 0, 0, 0, 0, 0, 0
                for _obj in _objs:
                    _missense += _obj.missense
                    _nonsense += _obj.nonsense
                    _splice += _obj.splice
                    _fsi += _obj.fsi
                    _fsd += _obj.fsd
                    _ifi += _obj.ifi
                    _ifd += _obj.ifd
                _total = _missense + _nonsense + _splice + _fsi + _fsd + _ifi + _ifd
                if _total == 0:
                    _total = 1
                itg['missense'][i] = '%.2f' % (_missense / _total * obj.tsample_num_rate)
                itg['nonsense'][i] = '%.2f' % (_nonsense / _total * obj.tsample_num_rate)
                itg['splice'][i] = '%.2f' % (_splice / _total * obj.tsample_num_rate)
                itg['fsi'][i] = '%.2f' % (_fsi / _total * obj.tsample_num_rate)
                itg['fsd'][i] = '%.2f' % (_fsd / _total * obj.tsample_num_rate)
                itg['ifi'][i] = '%.2f' % (_ifi / _total * obj.tsample_num_rate)
                itg['ifd'][i] = '%.2f' % (_ifd / _total * obj.tsample_num_rate)

    return render(request, 'cccga/query_sample.html', {'err_msgs': err_msgs, 'infos': infos})


def download(request):
    return render(request, 'cccga/download.html', {"LANGUAGES": LANGUAGES})
