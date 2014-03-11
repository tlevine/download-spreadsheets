from io import StringIO
from logging import getLogger
from traceback import print_exc

from special_snowflake import fromcsv

from featured_spreadsheets.settings import get

logger = getLogger('featured-spreadsheets')

def worker(read_queue, write_queue):
    while not read_queue.empty():
        catalog, dataset = read_queue.get()
        args = catalog, dataset['datasetid']
        url = '%s/explore/dataset/%s/download?format=csv' % args
        raw = get(url, load = True)

        dataset['catalog'] = catalog
        with StringIO(raw.decode('utf-8')) as fp:
            dataset.update(featurize(fp, url))

        write_queue.put(dataset)

def featurize(fp, url):
    try:
        pk = fromcsv(fp, delimiter = ';')
    except:
        not_file = StringIO()
        print_exc(file = not_file)
        logger.error('Error featurizing %s:\n\n%s\n' % (url, not_file.getvalue()))
        pk = set()
    return {
        'primary_keys': pk
    }
