##parameters=theme=None, edit_mode='wysiwyg', REQUEST=None, **kw

tmtool = context.portal_themes 
if REQUEST is not None:
    kw.update(REQUEST.form)
action = kw.get('action', None)

url_obj = None

if theme is None:
    theme = tmtool.getDefaultThemeName()

redirect_url = '/edit_form' + \
               '?theme=' + theme + '&edit_mode=' + edit_mode

if action == 'insert':
    try:
        xpos = context.xpos
    except:
        return
    ypos = context.getTempletPosition() 
    if ypos is None:
        return
    if ypos > 0:
        ypos = ypos -1
    redirect_url = '/add_templet_form?templet_xpos=' + str(xpos) + \
                  '&templet_ypos=' + str(ypos) + \
                  '&theme=' + theme + '&edit_mode=' + edit_mode
    url_obj = context.aq_parent

if action == 'duplicate':
    url_obj = context.duplicate()

if action == 'delete':
    tmtool.delObject(context)
    url_obj = context.aq_parent

if action == 'edit':
    url_obj = context

if url_obj is None:
    return

url = url_obj.absolute_url() + redirect_url

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
