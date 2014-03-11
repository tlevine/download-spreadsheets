def ignore(dataset):
    return 'geo_shape' in set(f['type'] for f in dataset['fields'])
