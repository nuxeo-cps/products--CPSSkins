now = DateTime()
objs = []

folder = context.aq_explicit
if hasattr(folder, 'listFolderContents'):
    for obj in folder.listFolderContents():

        if obj.getId().startswith('.') or getattr(obj, 'title', '') == '':
            continue

        start_pub = getattr(obj, 'effective_date', None)
        end_pub   = getattr(obj, 'expiration_date', None)
        if start_pub and start_pub > now:
            continue
        if end_pub and now > end_pub:
            continue

        objs.append(obj)
return objs


