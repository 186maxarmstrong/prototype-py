def path(name: str):
    global routes
    if name in routes and 'path' in routes[name]:
        return routes[name]['path']
    else:
        return('701', f'Sorry the path "{name}" does not exist.')

def redirect(name: str, pathName: bool = True, params: list = None):
    if pathName:
        path = path(name)
    else:
        path = name

    if params:
        query = '&'.join([f'{key}={value}' for key, value in params.items()])
        return ("Header: {Location" + path + "?" + query + "}")
    else:
        return ("Header: {Location" + path + "}")

def asset(name: str):
    return '/../../static/' + name