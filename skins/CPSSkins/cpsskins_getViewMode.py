##parameters=REQUEST=None

if REQUEST is None:
    REQUEST = context.REQUEST

session = REQUEST.SESSION
session_key = 'cpsskins_view_mode'

mode = {}
if session.has_key(session_key):
   mode = session[session_key]

return mode
