
REQUEST=context.REQUEST

request_url = REQUEST.get('URL', None)
query_string = REQUEST.get('QUERY_STRING', None)

if request_url.endswith('/index_html'):
    request_url = request_url[:-11]
if query_string:
    request_url += '?' + query_string

return request_url
