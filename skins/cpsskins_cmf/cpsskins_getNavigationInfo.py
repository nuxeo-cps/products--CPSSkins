##parameters=level=None, base=None, show_docs=None, base_path='/', max_results=None, context_obj=None, **kw

REQUEST=context.REQUEST

if level is None:
   return {'menuentries': [], 'create_url': '', 'folder_title': ''}

if show_docs is None:
   show_docs = 0
else:
   show_docs=int(show_docs)

try:
   level = int(level)
except ValueError:
   return {'menuentries': [], 'create_url': '', 'folder_title': ''}

utool = context.portal_url
mtool = context.portal_membership
wtool = context.portal_workflow
portal_url = utool(relative=1)
portal_root = utool.getPortalObject()

if portal_url != '/':
    portal_url = '/' + portal_url

if context_obj is None:
   return {'menuentries': [], 'create_url': '', 'folder_title': ''}

here_rurl =  '/' + utool.getRelativeUrl(context_obj)
current_path = here_rurl

here_url = context_obj.absolute_url()

if not base_path.startswith('/'):
    base_path = '/' + base_path

base_url = portal_url
if base_path != '/':
    base_url += base_path

    # restrictedTraverse() raises IndexError if the url starts with '/' (??)
    # a problem here is that the url may start with '//' if portal_url is '/'
    if len(base_path) > 1:
        i = 0
        while base_path[i] == '/':
            base_path = base_path[1:]
        if base_path == '/':
            base_obj = portal_root
        else:
            base_obj = portal_root.restrictedTraverse(base_path, default=None)
            if base_obj is None:
                return {'menuentries': [],
                    'create_url': '', 'folder_title': ''}

if not current_path.startswith(base_path):
    if level > 0:
        return {'menuentries': [],
                'create_url': '', 'folder_title': ''}
    else:
        level_obj = base_obj
else:
    split_current_path = current_path.split('/')
    if not getattr(context_obj.aq_explicit, 'isPrincipiaFolderish', 0):
        split_current_path = split_current_path[0:len(split_current_path)-1]
    split_base_path = base_path.split('/')
    split_relative_path = split_current_path[0:len(split_base_path)+level-1]

    if split_relative_path == ['']:
        level_obj = utool.getPortalObject()
    else:
        relative_path = '/'.join(split_relative_path)

        pp = portal_url + relative_path
        if len(pp) > 1:
            # instead of pp = lstrip('/')
            # to ensure compatibility with python 2.1
            i = 0
            while pp[i] == '/':
                pp = pp[1:]
        level_obj = portal_root.restrictedTraverse(pp, default=None)
        if level_obj is None:
            return {'menuentries': [],
                    'create_url': '', 'folder_title': ''}

    if len(split_relative_path) <= level:
        return {'menuentries': [],
                'create_url': '', 'folder_title': ''}

dict = {}
obj_info = []
create_url = ''
folder_title = getattr(level_obj, 'title', '')

checkPerm = mtool.checkPermission
if checkPerm('Add portal content', level_obj):
    if level_obj.allowedContentTypes():
        create_url = level_obj.absolute_url() + '/folder_factories'

objs = level_obj.cpsskins_getFolderContents()
if objs is None:
    return {'menuentries': [],
            'create_url': '', 'folder_title': ''}

if max_results is not None:
    objs = objs[0:max_results]

for obj in objs:
    folderish = getattr(obj.aq_explicit, 'isPrincipiaFolderish', 0)
    if not folderish and not show_docs:
        continue

    obj_url = obj.absolute_url()
    obj_info.append(
        {'id':  obj.getId(),
         'title': obj.title_or_id(),
         'url': obj_url,
         'selected': (here_url + '/').startswith(obj_url + '/'),
         'icon': obj.getIcon(),
         'folderish': folderish,
        }
    )

return { 'menuentries': obj_info,
         'create_url': create_url,
         'folder_title': folder_title }
