##parameters=REQUEST=None, **kw

tmtool = context.portal_themes
tmtool.manage_clearCaches()

if REQUEST is None:
    REQUEST = context.REQUEST
kw.update(REQUEST.form)

edit_mode = kw.get('edit_mode', 'wysiwyg')
theme = kw.get('theme', None)
if theme is None:
    theme = tmtool.getDefaultThemeName()

theme_container = tmtool.getEffectiveThemeContainer(theme=theme)
if theme_container is not None:
    url = theme_container.absolute_url() + '/edit_form' + \
          '?theme=' + theme + '&edit_mode=' + edit_mode

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
