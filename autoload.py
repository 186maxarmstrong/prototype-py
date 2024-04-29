import glob
import os
import sys
import traceback

# Find all PHP files in the current directory
for file in glob.glob(os.path.join(os.path.dirname(__file__), '*.py')):
    # Include each PHP file
    try:
        exec(open(file).read())
    except Exception as e:
        # Handle any errors that occur during execution
        error_message = f"File: {file}; Error: {str(e)}"
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

# Define an error handler function
def error_handler(errfile, errline):
    return f"File: {errfile}; Line: {errline}"

# Set the error handler
sys.excepthook = error_handler

# Build the URL
if 'HTTPS' in os.environ and os.environ['HTTPS'] == 'on':
    link = "https://"
else:
    link = "http://"

# Set the HTTP_ORIGIN
os.environ['HTTP_ORIGIN'] = link + os.environ['HTTP_HOST']

# Define the secure headers
prototype_header_secure = {
    'Content-Type': 'text/html; charset=utf-8',
    'X-Frame-Options': 'SAMEORIGIN',
    'X-XSS-Protection': '1; mode=block',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
    'X-Download-Options': 'noopen',
    'X-Permitted-Cross-Domain-Policies': 'none',
    'X-Content-Security-Policy': "default-src 'self'",
    'X-DNS-Prefetch-Control': 'off',
}

# Set the CORS headers
prototype_header_cors = {}
if 'HTTP_ORIGIN' in os.environ:
    prototype_header_cors = {
        'Access-Control-Allow-Origin': os.environ['HTTP_ORIGIN'],
        'Access-Control-Allow-Credentials': 'true',
        'Access-Control-Max-Age': '86400',
        'Content-Security-Policy': "default-src 'self'",
    }

# Handle OPTIONS requests
if os.environ['REQUEST_METHOD'] == 'OPTIONS':
    if 'HTTP_ACCESS_CONTROL_REQUEST_METHOD' in os.environ:
        prototype_header_cors['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    if 'HTTP_ACCESS_CONTROL_REQUEST_HEADERS' in os.environ:
        prototype_header_cors['Access-Control-Allow-Headers'] = os.environ['HTTP_ACCESS_CONTROL_REQUEST_HEADERS']

# Define the cache headers
prototype_header_nocache = {
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0',
}

prototype_header_cache = {
    'Cache-Control': 'public, max-age=604800, immutable',
}