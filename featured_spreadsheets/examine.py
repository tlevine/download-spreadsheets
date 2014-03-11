from io import StringIO

from special_snowflake import fromcsv

from featured_spreadsheets.settings import get

def worker(read_queue, write_queue):
    while not read_queue.empty():
        catalog, dataset = read_queue.get()
        args = catalog, dataset['datasetid']
        url = '%s/explore/dataset/%s/download?format=csv' % args
        raw = get(url, load = True)

        dataset['catalog'] = catalog
        with StringIO(raw.decode('utf-8')) as fp:
            dataset.update(featurize(fp))

        write_queue.put(dataset)

def featurize(fp):
    try:
        pk = fromcsv(fp, delimiter = ';')
    except:
        pk = set()
    return {
        'primary_keys': pk
    }
