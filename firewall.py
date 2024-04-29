import secrets
import hashlib
import re
from http import cookies
import mysql.connector

session = cookies.SimpleCookie()

def generate_csrf_token():
    token = secrets.token_hex(32)
    session['csrf_token'] = token
    return hashlib.sha256(token.encode()).hexdigest()

def validate_csrf_token(token):
    if 'csrf_token' in session and hashlib.sha256(session['csrf_token'].encode()).hexdigest() == token:
        del session['csrf_token']
        return True
    return False

def validate_email(email):
    return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))

def validate_url(url):
    return bool(re.match(r'^(http|https)://[\w\.-]+\.\w+$', url))

def connect_sql(host, user, password, database):
    conn = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    if conn.is_connected():
        return conn
    else:
        raise Exception('Failed to connect to MySQL')

def sql_escape_real(string, conn):
    return conn.converter.escape(string)

def sql_escape_mimic(inp):
    if isinstance(inp, list):
        return list(map(sql_escape_mimic, inp))
    if inp and isinstance(inp, str):
        return re.sub(r'[\x00\x0a\x0d\x1a\\\'"\b\t\n\r\x1a]', r'\\\g<0>', inp)
    return inp

def session_set(key, value=None):
    if value is None:
        return session.get(key)
    session[key] = value

def session_unset(key):
    if key in session:
        del session[key]