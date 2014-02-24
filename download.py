import json

def get(url, **kwargs):
    from get import get as _get
    return _get(url, cachedir = 'data', **kwargs)

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
    return json.loads(get(catalog + '/api/datasets/1.0/search?rows=1000000', load = True))['datasets']

def worker(queue):
    while not queue.empty():
        url = queue.get()
        try:
            get(url, load = False)
        except:
            queue.put(url)
