def get(url, **kwargs):
    from get import get as _get
    return _get(url, cachedir = 'data', **kwargs)
