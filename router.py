import re
import os
import urllib
import json


routes = {}

def serve(config=None):
    global routes

    link = os.environ['HTTP_ORIGIN']

    # Validate host
    if config and 'host' in config and config['host'].lower() != link.lower():
        return('403 Forbidden', f'Your host is set as "{config["host"]}" however you visit from "{link}"')

    # Validate port
    if config and 'port' in config and str(config['port']) != os.environ['SERVER_PORT']:
        return('403 Forbidden', f'Your port is set as "{config["port"]}" however you visit from "{os.environ["SERVER_PORT"]}"')

    # Validate url
    link += os.environ['REQUEST_URI'] + "?" + os.environ['QUERY_STRING']
    path = urllib.parse.urlparse(link).path

    if not path:
        return('400 Bad Request', 'Malformed url')
    else:
        path = path.strip('/')

    # Prepare path
    path = path.split('?')[0]
    callback = None
    params = []

    # Compartmentalize
    for route in routes.values():
        routePath = route['path'].strip('/')
        routePath = re.sub(r'{[^}]+}', '(.+)', routePath)
        routePath = routePath.rstrip('?')

        matches = re.match(f'^{routePath}$', path)
        if matches:
            callback = route
            params = matches.groups()
            break

    # 404 Page return
    if not callback or not callable(callback['callback']):
        return('404 Not Found', 'Sorry, the page you are looking for could not be found. but you can always try again')

    # 405 Page return
    if os.environ['REQUEST_METHOD'] not in callback['method'] and callback['method']:
        if os.environ['REQUEST_METHOD'] == 'GET':
            return('405 Method Not Allowed', f'The method \'{os.environ["REQUEST_METHOD"]}\' is not allowed, please try again with one of the following method(s) \'{", ".join(callback["method"])}\'')
        else:
            response = {
                'status': 405,
                'message': f'The method \'{os.environ["REQUEST_METHOD"]}\' is not allowed, please try again with one of the following method(s) \'{", ".join(callback["method"])}\''
            }
            return json.dumps(response)

    # Callback
    return callback['callback'](*params)

def route(name, path, callback, method=None):
    global routes

    routes[name] = {
        'path': path,
        'method': method,
        'callback': callback
    }