##parameters=theme=None, no_referer=0, REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is not None:
    kw.update(REQUEST.form)

params = {}

# get the current theme
theme, page = tmtool.getEffectiveThemeAndPageName(editing=1)
# set the current theme
params['theme'] = theme

# vertical scroll position
if kw.has_key('scrolly'):
    params['scrolly'] = kw['scrolly']

# current url
if no_referer:
    tmtool.clearViewMode('current_url')
else:
    params['current_url'] = context.REQUEST['HTTP_REFERER']

# set the default panel to WYSIWYG
params['themes_panel'] ='wysiwyg'

# save session variables
tmtool.setViewMode(**params)

url = context.portal_url() + '/cpsskins_theme_manage_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
