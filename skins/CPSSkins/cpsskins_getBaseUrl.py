
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
portal = utool.getPortalObject()
base_url = portal.absolute_url_path()
if not base_url.endswith('/'):
    base_url += '/'

# cache the base url in the REQUEST
if REQUEST is not None:
    REQUEST.set('cpsskins_base_url', base_url)
return base_url
