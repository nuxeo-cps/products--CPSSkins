##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

if REQUEST is None:
    REQUEST = context.REQUEST
session = REQUEST.SESSION

session_key = 'cpsskins_view_mode'

if not session.has_key(session_key):
    session[session_key] = {}

mode = {}
if kw.has_key('fullscreen'):
    value = kw['fullscreen']
    if value in ['0', '1']:
        mode['fullscreen'] = int(value)

if kw.has_key('portlets_panel'):
    value = kw['portlets_panel']
    if value in ['visibility', 'browser', 'unused']:
        mode['portlets_panel'] = value

session[session_key].update(mode)

url = REQUEST.get('HTTP_REFERER')
REQUEST.RESPONSE.redirect(url)
