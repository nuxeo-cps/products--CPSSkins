tmtool = context.portal_themes
ttool = context.portal_types

allowed_content_types = ['image/gif', 'image/jpeg', 'image/png', 'image/x-icon']

themeroot = tmtool.getPortalThemeRoot(context)

images_dir = getattr(themeroot, 'thumbnails', None)
if images_dir is None:
    themeroot.rebuild()
    return []

images = ['']
for obj in images_dir.objectValues():
    content_type = getattr(obj, 'content_type', None)
    if content_type in allowed_content_types:
        images.append(obj.getId())

return images
