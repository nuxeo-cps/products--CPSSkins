##parameters=level=0, base=None, show_docs=None, base_path=None, max_results=None, display_hidden_folders=None, context_obj=None

if base_path is None:
    return {'menuentries': [],
            'create_url': '', 'folder_title': ''}

# XXX backward compatibilty since the trailing '/' was omitted
# in previous versions, this will be moved to the
# 'rebuild theme' method.
l = len(base_path)
if base_path[l-1:l] != '/':
   base_path = base_path + '/'
# end backward compatibility code

delta = len(base_path.split('/')) -3
rel_level = level
if delta > 0:
   rel_level = level + delta

if show_docs is None:
   show_docs = 0
else:
   try:
      show_docs=int(show_docs)
   except:
      show_docs = 0

if base is None:
    return {'menuentries': [],
            'create_url': '', 'folder_title': ''}

ttool = context.portal_trees
utool = context.portal_url

if base in ttool.objectIds():
    base_obj = ttool[base]
    base_obj_as_proxy = getattr(context.portal_proxies, base)
else:
    return {'menuentries': [],
            'create_url': '', 'folder_title': ''}

REQUEST = context.REQUEST

parent_url = ''

if context_obj is None:
    return {'menuentries': [],
            'create_url': '', 'folder_title': ''}

here_rurl =  '/' + utool.getRelativeUrl(context_obj)
here_rurl_slash = here_rurl + '/'

parent_url = here_rurl
path_list = here_rurl.split('/')

base_url = REQUEST.get('cpsskins_base_url', '')

base_create_path = ''
base_create_obj = None
create_url = ''
folder_title = ''
menuentries = []

if rel_level > 0:
    try:
        parent_treelist = base_obj.getList(
            start_depth=rel_level-1,
            stop_depth=rel_level-1,
            filter=1,
            order=1,
            count_children=0)
    except TypeError: # CPS < 3.3
        parent_treelist = base_obj.getList(
            start_depth=rel_level-1,
            stop_depth=rel_level-1,
            filter=1)

    for item in parent_treelist:
        rpath = item['rpath']
        if here_rurl_slash.startswith('/' + rpath + '/'):
            parent_url = rpath
            base_create_path = utool.getPortalPath() + '/' + parent_url
            break

if rel_level == 1:
    base_create_url = base_url + base
    base_create_obj = base_obj_as_proxy

if base_create_obj is None and base_create_path != '':
    try:
        base_create_obj = context.restrictedTraverse(base_create_path)
        base_create_url = base_url + parent_url
    except:
        pass

if rel_level > 0 and base_create_obj is not None:
    if context.portal_membership.checkPermission('Add portal content',
                                                  base_create_obj):
        create_url = base_create_url + '/folder_factories'

if rel_level > 1 and \
   (rel_level > len(path_list)-1  or \
   not here_rurl.startswith(base_path)):
      create_url = ''

if base_create_obj:
    folder_title = base_create_obj.Title()
    items = base_create_obj.objectValues()
    if max_results is not None:
        items = items[0:max_results]
    docs = base_create_obj.filterContents(items=items,
                                  hide_folder=0,
                                  displayed=[''])
    for doc in docs:
        folderish = doc.isPrincipiaFolderish
        if not show_docs and not folderish:
            continue

        if not display_hidden_folders:
            content = doc.getContent()
            if hasattr(content.aq_explicit, 'hidden_folder'):
                if content.hidden_folder == 1:
                    continue

        if hasattr(doc.aq_explicit, 'getRID'):
            doc = doc.getObject()

        doc_rpath = utool.getRelativeUrl(doc)
        menuentries.append(
            {'title' : doc.title_or_id(),
             'id' : doc.id,
             'url' : base_url + doc_rpath,
             'selected' : here_rurl_slash.startswith('/' + doc_rpath + '/'),
             'icon' : doc.getIcon(relative_to_portal=1),
             'folderish' : folderish }
        )

# tree root
if rel_level == 0:
    checkPerm = context.portal_membership.checkPermission
    if checkPerm('List folder contents', base_obj_as_proxy):
        base_obj_rpath = utool.getRelativeUrl(base_obj_as_proxy)
        menuentries = [
            {'title': base_obj_as_proxy.title_or_id(),
             'id': base_obj_as_proxy.id,
             'url': base_url + base_obj_rpath,
             'selected': here_rurl_slash.startswith('/' + base_obj_rpath + '/'),
             'icon': base_obj_as_proxy.getIcon(relative_to_portal=1),
             'folderish': 1, }
        ]

return { 'menuentries' : menuentries,
         'create_url' : create_url,
         'folder_title': folder_title }

