##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes

pageblock = context.addPageBlock(**kw)
if pageblock is None:
    return

url = pageblock.absolute_url() + '/edit_form'

# set the edit mode to 'layout'
tmtool.setViewMode(edit_mode='layout')

if REQUEST is None:
    return pageblock
else:
    REQUEST.RESPONSE.redirect(url)
