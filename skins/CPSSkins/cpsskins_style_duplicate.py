##parameters=REQUEST=None, **kw

if REQUEST is not None:
    kw.update(REQUEST.form)

# duplicate the current style
newstyle = context.duplicate()

# do not let the new style be used by default
newstyle.edit(default=0)

# assign the new style to the edited object
tmtool = context.portal_themes
view_mode = tmtool.getViewMode()
edited_url = view_mode.get('edited_url')

if edited_url is not None:
    edited_obj = context.restrictedTraverse(edited_url, default=None)
    if edited_obj is not None:
        edited_obj.setStyle(newstyle)

url = newstyle.absolute_url() + '/cpsskins_edit_form'

if REQUEST is not None:
    REQUEST.RESPONSE.redirect(url)
