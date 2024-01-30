import csv
import sys

from cccga.models import Hgnc2PfamDB


def import_hgnc2pfam(row):
    Hgnc2PfamDB.objects.get_or_create(
        hgnc=row['hgnc'],
        symbol=row['symbol'],
        uniprot=row['uniprot'],
        aa_length=row['aa_length'],
        start=row['start'],
        end=row['end'],
        hmm_acc=row['hmm_acc'],
        hmm_name=row['hmm_name'],
        p_type=row['p_type']
    )


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for i, row in enumerate(reader):
            k = '-'.join([row['HGCN'].strip(), str(i)])
            if d.get(k) is None:
                sd = d[k] = {}
                sd['hgnc'] = row['HGCN'].strip()
                # HGCN is ''
                if not sd['hgnc']:
                    del d[k]
                    continue
                sd['symbol'] = row['symbol'].strip()
                sd['uniprot'] = row['uniprot'].strip()
                sd['aa_length'] = row['length'].strip()
                sd['start'] = row['start'].strip()
                sd['end'] = row['end'].strip()
                sd['hmm_acc'] = row['hmm.acc'].strip()
                sd['hmm_name'] = row['hmm.name'].strip()
                sd['p_type'] = row['type'].strip()
                # NA
                if 'NA' in [sd['aa_length'], sd['start'], sd['end']]:
                    del d[k]
    return d


if __name__ == '__main__':
    tab = sys.argv[1]
