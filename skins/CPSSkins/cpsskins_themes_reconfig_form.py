##parameters=theme=None, REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is None:
    REQUEST = context.REQUEST
kw.update(REQUEST.form)

params = {}

# get the current theme
theme = kw.get('theme')
if theme is None:
    theme = tmtool.getRequestedThemeName(context_obj=context)
# set the current theme
params['theme'] = theme

# vertical scroll position
if kw.has_key('scrolly'):
    params['scrolly'] = kw['scrolly']

# current url
params['current_url'] = REQUEST['HTTP_REFERER']

# set the default panel to WYSIWYG
params['themes_panel'] ='wysiwyg'

# save session variables
tmtool.setViewMode(**params)

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
