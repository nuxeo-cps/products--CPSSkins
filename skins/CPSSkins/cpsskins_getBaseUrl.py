
# return the base url of the zope instance, ex: /cps/ or /

REQUEST = getattr(context, 'REQUEST', None)

# check whether the base url is already cached in the REQUEST
if REQUEST is not None and REQUEST.has_key('cpsskins_base_url'):
    return REQUEST['cpsskins_base_url']

# use utool.getBaseUrl() if it is present
utool = context.portal_url
if getattr(utool.aq_inner.aq_explicit, 'getBaseUrl', None) is not None:
    return utool.getBaseUrl()

# CMF, CPS < 3.3.5, Plone ...
if REQUEST is None:
    path_info = ''
else:
    path_info = getattr(REQUEST, 'PATH_INFO', '')

if path_info.startswith('/VirtualHostBase/'):
    # apache detection

    # Inside-out hosting (VHM _vh_)
    if path_info.find('_vh_') > 0:
        base = path_info.split('_vh_')[1]
        if base.find('/') > 0:
            base = base.split('/')[0]
        base_url = '/' + base + '/'
    else:
        base_url = '/'
else:
    # XXX squid detection
    # classic case
    utool = context.portal_url
    base_url = utool.getPortalPath() + '/'

# cache the base url in the REQUEST
if REQUEST is not None:
    REQUEST.set('cpsskins_base_url', base_url)
return base_url
