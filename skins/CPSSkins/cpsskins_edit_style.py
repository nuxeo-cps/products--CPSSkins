##parameters=style='', stylecat='', REQUEST=None

tmtool = context.portal_themes
style = tmtool.findStylesFor(category=stylecat, object=context, title=style)
object = style['object']
if len(object) == 0:
    return

redirect_url = object[0].absolute_url() + '/edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(redirect_url)
