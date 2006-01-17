##parameters=REQUEST, cluster=None, cpsdocument_edit_and_view_button=None, action=None

context.editLayouts(REQUEST=REQUEST)

doc = context.getContent()
is_valid, ds = doc.validate(request=REQUEST, proxy=context, cluster=cluster,
                            use_session=True)


url = REQUEST['HTTP_REFERER']
REQUEST.RESPONSE.redirect(url)
