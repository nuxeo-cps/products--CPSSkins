##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

ptltool = context.portal_cpsportlets

# XXX rename 'getViewMode' to something else.
tmtool = context.portal_themes
view_mode = tmtool.getViewMode()
object_rurl = view_mode.get('clipboard')
if object_rurl is None:
    return

portal_path = context.portal_url.getPortalPath() + '/'
object = context.restrictedTraverse(portal_path + object_rurl, default=None)
if object is None:
    return

ptltool.movePortlet(portlet=object,
                    dest_folder=context,
                    **kw)

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
