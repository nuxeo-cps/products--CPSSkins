##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

tmtool = context.portal_themes
action = kw.get('action', None)

url_obj = None
redirect_url = '/edit_form'

if action == 'insert':
    try:
        xpos = context.xpos
    except:
        return
    ypos = context.getVerticalPosition()
    if ypos is None:
        return
    if ypos > 0:
        ypos = ypos -1
    redirect_url = '/add_templet_form?templet_xpos=' + str(xpos) + \
                  '&templet_ypos=' + str(ypos)
    url_obj = context.aq_parent

if action == 'duplicate':
    url_obj = context.duplicate()

if action == 'delete':
    tmtool.delObject(context)
    url_obj = context.aq_parent

if action == 'edit':
    url_obj = context

if action == 'edit_styles':
    url_obj = context
    redirect_url += '?cat=style'

if url_obj is None:
    return

url = url_obj.absolute_url() + redirect_url

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
