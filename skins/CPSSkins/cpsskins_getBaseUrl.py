##parameters=utool=None

# return the base url of the zope instance, ex: /cps/ or /

if not utool:
    utool = context.portal_url

REQUEST = getattr(context, 'REQUEST', None)

if REQUEST is None:
    path_info = ''
else:
    path_info = getattr(REQUEST, 'PATH_INFO', '')

if path_info.startswith('/VirtualHostBase/') :
    # apache detection
    return '/'
else:
    # XXX squid detection
    # classic case
    return utool.getPortalPath()+ '/'

# XXX: virtualhostbases with _vh_ ?
