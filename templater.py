import os
import re

def template(file: str, args: dict = None) -> str:
    file_path = './templates/' + file

    if not os.path.exists(file_path):
        raise Exception('500', f'The template file "{file}" does not exist.')

    if isinstance(args, dict):
        locals().update(args)

    html = ''
    with open(file_path, 'r') as f:
        html = f.read()

    search = [
        r'>[^\S ]+',
        r'[^\S ]+<',
        r'(\s)+',
        r'<!--(.|\s)*?-->'
    ]
    replace = ['>', '<', '\\1']
    for i in range(len(search)):
        html = re.sub(search[i], replace[i], html)

    return html