##parameters=level=0, base=None, show_docs=None, base_path=None, max_results=None, display_hidden_folders=None, context_obj=None

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

REQUEST = context.REQUEST
if context_obj is None:
    return

nav = CPSNavigation(root_uid=base,
                    current_uid=utool.getRelativeUrl(context_obj),
                    context=context_obj,
                    request_form=REQUEST.form)

menuentries = []
current_object = None
folder_title = ''

for node in nav.getTree():

    node_level = node['level']
    object = node['object']

    if node.get('is_current'):
       folder_title = object['title_or_id']

    if node_level == int(level) -1:
       if node['state'] == 'open':
           current_object = object

    if node_level != level:
        continue

    if not display_hidden_folders:
        if node.get('hidden_folder'):
            continue

    menuentries.append(
        {'title' : object['title_or_id'],
         'id' : object['id'],
         'url' : object['url'],
         'icon': '', #XXX
         'folderish': 1, #XXX
         'selected': node.get('is_open'),
        }
    ) 

create_url = ''
if current_object is not None:
    create_url = current_object['url'] + '/folder_factories'

return {'menuentries' : menuentries,
        'create_url' : create_url,
        'folder_title': folder_title,
       }
