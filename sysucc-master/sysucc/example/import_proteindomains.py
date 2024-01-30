import csv
import sys

from cccga.models import ProteinDomainsDB


def import_prodom(row):
    ProteinDomainsDB.objects.get_or_create(
        hgnc=row['hgnc'],
        refseq_id=row['refseq_id'],
        protein_id=row['protein_id'],
        aa_length=row['aa_length'],
        start=row['start'],
        end=row['end'],
        domain_source=row['domain_source'],
        label=row['label'],
        domain_anno=row['domain_anno'],
        pfam=row['pfam'],
        description=row['description'],
    )


def process_data(tab):
    d = {}
    with open(tab) as fp:
        reader = csv.DictReader(fp)
        for i, row in enumerate(reader):
            k = '-'.join([row['HGNC'].strip(), str(i)])
            if d.get(k) is None:
                sd = d[k] = {}
                sd['hgnc'] = row['HGNC'].strip()
                sd['refseq_id'] = row['refseq.ID'].strip()
                sd['protein_id'] = row['protein.ID'].strip()
                sd['aa_length'] = row['aa.length'].strip()
                sd['start'] = row['Start'].strip()
                sd['end'] = row['End'].strip()
                sd['domain_source'] = row['domain.source'].strip()
                sd['label'] = row['Label'].strip()
                sd['domain_anno'] = row['domain.anno'].strip()
                sd['pfam'] = row['pfam'].strip()
                sd['description'] = row['Description'].strip()
    return d


if __name__ == '__main__':
    tab = sys.argv[1]
