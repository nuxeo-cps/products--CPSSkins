##parameters=level=0, base=None, show_docs=None, base_path=None, max_results=None, display_hidden_folders=None, context_rurl=None, REQUEST=None

if base_path is None:
    return

if show_docs is None:
   show_docs = 0
else:
   try:
      show_docs=int(show_docs)
   except:
      show_docs = 0

if base is None:
    return 

from Products.CPSNavigation.CPSNavigation import CPSNavigation
utool = context.portal_url

if REQUEST is None:
    REQUEST = context.REQUEST

context_obj = REQUEST.get('context_obj', None)

nav = CPSNavigation(root_uid=base,
                    current_uid=utool.getRelativeUrl(context_obj),
                    context=context_obj,
                    request_form=REQUEST.form)

menuentries = []
tree = [t for t in nav.getTree() if t['level'] == level]
for t in tree:
    if not display_hidden_folders:
        if t.get('hidden_folder'):
            continue

    object = t['object']
    menuentries.append(
        {'title' : object['title_or_id'],
         'id' : object['id'],
         'url' : object['url'],
         'icon': '', #XXX
         'folderish': 1, #XXX
         'selected': t.get('is_open'),
        }
    ) 

return {'menuentries' : menuentries,
        'create_url' : '', #XXX
        'folder_title': '', #XXX
       }
