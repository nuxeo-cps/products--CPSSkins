##parameters=level=None, base=None, show_docs=None, base_path=None, max_results=None, **kw

REQUEST=context.REQUEST

if show_docs is None:
   show_docs = 0
else:
   try:
      show_docs=int(show_docs)
   except:
      show_docs = 0

if base is None:
   return

if level is None:
   return

if base_path is None:
   base_path = '/'

try:
   level = int(level) 
except:
   return

utool = context.portal_url
portal_url = utool.getPortalPath()

mtool = context.portal_membership
mcat = context.portal_messages
user = mtool.getAuthenticatedMember()
roles = user.getRoles()
myid = user.getUserName()
try: mygroups = user.getGroups()
except: mygroups = ()
myids = [myid] + ['group:'+id for id in mygroups]

try:
   hier_base =  getattr(context.portal_hierarchies, base, None)
except:
   return None

if hier_base is None:
   return

base_path_list = base_path.split('/')
rel_level = len(base_path_list) -2
total_level = level + rel_level

base_parent_list = base_path.split('/')
base_parent_path = '/'.join(base_parent_list[0:len(base_parent_list)-1])

hierlist = hier_base.getHierarchyList()

hierlist = [h for h in hierlist if h['depth'] == total_level]
hierlist = [h for h in hierlist if (h['rurl'] +'/').startswith(base_parent_path)]

context_obj = REQUEST.get('context_obj', None)

if context_obj is not None:
    current_path =  '/' + utool.getRelativeUrl(context_obj)
else:
    return

munge_url = REQUEST.get('munge_absolute_url', context, None)
if len(munge_url) > 1:
   hier_url = munge_url[1]
   portal_path = context.portal_url.getPortalPath()
   portal_path_length = len(portal_path.split('/'))
   current_path = '/' + '/'.join(hier_url[portal_path_length:-1])

path_list = current_path.split('/')
path = '/'.join(path_list[0:total_level + 1])

current_path = '/'.join(path_list[0:total_level + 2])

if total_level == 1:
     try:
        current_hier = hier_base.getRootObject()
     except:
        current_hier = None
else:
     try:
        current_hier = context.restrictedTraverse(portal_url + path)
     except:
        current_hier = None

if level == 0:
     hierlist = [h for h in hierlist if (h['rurl'] + '/').startswith(base_parent_path) ]
     current_hier = context.restrictedTraverse(portal_url + base_parent_path)
else:
     if total_level != 1:
         hierlist = [h for h in hierlist if (h['rurl'] + '/').startswith(path + '/') ]
     if len(path_list) <= total_level  or not (path + '/').startswith(base_parent_path):
         hierlist = []
         current_hier = None

create_url = ''
folder_title = ''
if current_hier:
    folder_title = current_hier.Title()

pubinfos = []
can_create = mtool.checkPermission('Add Hierarchy Level', current_hier)

if current_hier is not None:
    ti =  current_hier.getTypeInfo()
    if ti is not None:
       is_hierarchy = ( ti.getId() == 'Reviewed Hierarchy Level' ) 
       current_url = current_hier.absolute_url()
       if is_hierarchy:
           if can_create:
               create_url = current_url + '/folder_invoke_factory?type_name=Reviewed+Hierarchy+Level'

           if show_docs==1:
              documents = current_hier.queryCatalog()
              for brain in documents:
                 d = context.cpsdocument_info_get(brain=brain, mcat=mcat)
                 obj = brain.getObject()

                 url = current_url + '/' + d['id']
                 hier_rurl =  '/' + utool.getRelativeUrl(current_hier) + '/'
                 if not (hier_rurl + '/').startswith(base_path):
                    continue
                 if context_obj.absolute_url() == url:
                    selected = 1
                 else:
                    selected = 0

                 doc = {
                         'title' : d['title'],
                         'id' : d['id'],
                         'url' : url + '/view',
                         'selected' : selected,
                         'icon' : d['icon'],
                         'folderish' : 0,
                       }
                       
                 pubinfos.append(doc)


hierarchies = []
if max_results is not None:
    hierlist = hierlist[0:maxresults]

for h in hierlist:
    readers = h['levelreaders']
    if readers and not 'Manager' in roles:
        readers = readers + h['levelreviewers']
        ok = 0
        for id in myids:
            if id in readers:
                ok = 1
                break
        if not ok:
            continue
    rurl = h['rurl']

    url = utool(relative=0) + rurl 

    if (rurl + '/').startswith(current_path + '/') and total_level < len(path_list)  -1:
        selected = 1
    else:
        selected = 0

    hierarchies.append(
        {'id' : h['id'],
         'title': h['title'],
         'url': url,
         'selected': selected,
         'icon': 'folder_icon.gif',
         'folderish': 1 }
    ) 


return { 'menuentries': pubinfos + hierarchies,
         'create_url': create_url,
         'folder_title': folder_title }
