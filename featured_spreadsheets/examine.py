from io import StringIO
from logging import getLogger
from traceback import print_exc

from special_snowflake import fromcsv

from featured_spreadsheets.settings import get
from featured_spreadsheets.ignore import ignore

logger = getLogger('featured-spreadsheets')

def worker(read_queue, write_queue):
    while not read_queue.empty():
        catalog, dataset = read_queue.get()
        if ignore(dataset):
            continue

        args = catalog, dataset['datasetid']
        url = '%s/explore/dataset/%s/download?format=csv' % args
        raw = get(url, load = True)

        dataset['catalog'] = catalog
        with StringIO(raw.decode('utf-8')) as fp:
            dataset['unique_indices'] = unique_indices(fp, url)

        write_queue.put(dataset)

def unique_indices(fp, url):
    try:
        header_raw = next(fp)
    except StopIteration:
        header_raw = []
    else:
        header = header_raw.split(';')
        if header == ['']:
            header = []
    indices = set()
    for n_columns in range(1, len(header) + 1):
        try:
            pk = fromcsv(fp, delimiter = ';', n_columns = n_columns, only_adjacent = True)
        except:
            not_file = StringIO()
            print_exc(file = not_file)
            logger.error('Error featurizing %s:\n\n%s\n' % (url, not_file.getvalue()))
        else:
            indices = indices.union(pk)
    return indices
