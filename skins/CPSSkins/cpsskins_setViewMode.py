##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)
else:
    REQUEST = context.REQUEST

session = REQUEST.SESSION
session_key = 'cpsskins_view_mode'

session_dict = session.get(session_key, {})

fullscreen = kw.get('fullscreen')
if fullscreen in ['0', '1']:
    session_dict['fullscreen'] = int(fullscreen)

portlets_panel = kw.get('portlets_panel')
if portlets_panel in ['visibility', 'browser', 'unused']:
    session_dict['portlets_panel'] = portlets_panel

selected_portlets = kw.get('selected_portlet')
if selected_portlets is not None:
    session_dict['selected_portlet'] = selected_portlets

session[session_key] = session_dict

url = REQUEST.get('HTTP_REFERER')
REQUEST.RESPONSE.redirect(url)
