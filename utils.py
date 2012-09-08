def all(listf, **kwargs):
    """
    Simple generator to page through all results of function `listf`.
    """
    resp = listf(**kwargs)

    for obj in resp['objects']:
        yield obj

    while resp['meta']['next']:
        limit = resp['meta']['limit']
        offset = resp['meta']['offset']
        resp = listf(offset=(offset + limit))
        for obj in resp['objects']:
            yield obj
