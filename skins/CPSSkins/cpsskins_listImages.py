##parameters=imagecat=None

if imagecat not in context.cpsskins_listImageCategories():
    return []

list = []
tmtool = context.portal_themes
ttool = context.portal_types

allowed_content_types = [
    'image/gif',
    'image/jpeg',
    'image/png',
    'image/x-ico',
    'image/x-icon']
view_mode = tmtool.getViewMode()
theme = view_mode.get('theme')
theme_container = tmtool.getThemeContainer(theme=theme)

images_dir = theme_container.getImageFolder(category=imagecat)
if images_dir is None:
    theme_container.rebuild()
    return []

images = ['']
for obj in images_dir.objectValues():
    content_type = getattr(obj, 'content_type', None)
    if content_type in allowed_content_types:
        images.append(obj)
        list.append(obj)

return list
