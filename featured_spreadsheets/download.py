import json

from featured_spreadsheets.settings import get

catalogs = [
    'http://data.iledefrance.fr',
    'http://opendata.paris.fr.opendatasoft.com',
    'http://tourisme04.opendatasoft.com',
    'http://tourisme62.opendatasoft.com',
    'http://grandnancy.opendatasoft.com',
    'http://bistrotdepays.opendatasoft.com',
    'http://scisf.opendatasoft.com',
    'http://pod.opendatasoft.com',
    'http://dataratp.opendatasoft.com',
    'http://public.opendatasoft.com',
    'http://ressources.data.sncf.com',
]

def datasets(catalog):
    # Search an OpenDataSoft portal, and add things.
    # I chose OpenDataSoft because they care a lot about metadata.
    raw = get(catalog + '/api/datasets/1.0/search?rows=1000000', load = True)
    return json.loads(raw.decode('utf-8'))['datasets']

def worker(queue, _):
    while not queue.empty():
        catalog, dataset = queue.get()
        args = catalog, dataset['datasetid']
        url = '%s/explore/dataset/%s/download?format=csv' % args
        try:
            get(url, load = False)
        except:
            queue.put((catalog, dataset))
