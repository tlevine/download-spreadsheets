from io import StringIO

from special_snowflake import fromcsv

from settings import get

def worker(read_queue, write_queue):
    while not read_queue.empty():
        catalog, dataset = read_queue.get()
        args = catalog, dataset['datasetid']
        url = '%s/explore/dataset/%s/download?format=csv' % args
        raw = get(url, load = True)

        dataset['catalog'] = catalog
        with StringIO(raw) as fp:
            dataset.update(featurize(fp))

        write_queue.put(dataset)

def featurize(fp):
    return {
        'primary_keys': fromcsv(fp, delimiter = ';')
    }
