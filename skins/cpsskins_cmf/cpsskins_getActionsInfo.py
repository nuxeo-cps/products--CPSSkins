##parameters=obj=None, context_obj=None

if obj is None:
   return 

REQUEST = context.REQUEST
tmtool = context.portal_themes
current_url = REQUEST.get('cpsskins_url', None)
base_url = REQUEST.get('cpsskins_base_url', '')

action_categories = getattr(obj, 'action_categories', None) 
custom_action_categories = getattr(obj, 'custom_action_categories', []) 
show_action_icons = getattr(obj, 'show_action_icons', None) 
invisible_actions = getattr(obj, 'invisible_actions', []) 

categories = action_categories
if custom_action_categories:
    if custom_action_categories[0] != '':
       categories += custom_action_categories

actions = REQUEST.get('cpsskins_cmfactions', None)
if actions is None:
    if context_obj is None:
        context_obj = context
    actions = context.portal_actions.listFilteredActionsFor(context_obj)

actioninfo = []

getIconFor = tmtool.getIconFor
firstcat = 1
for category in categories:
    actions_by_cat = actions.get(category, [])

    if firstcat:
       newcat = 0
    elif one_action_is_visible:
       newcat = 1
    one_action_is_visible = 0
    for action in actions_by_cat:
        action_id = action.get('id')
        if action_id not in invisible_actions:
            one_action_is_visible = 1
            action_url = action.get('url').strip()

            we_are_here = 0
            url = action_url
            if url[-1:] == '/':
                url = url[:-1]
            if url == current_url: 
                we_are_here = 1

            menustyle = ''
            if show_action_icons:
                icon = getIconFor(category, action_id)
                if icon:
                    menustyle = 'background: url(%s%s) no-repeat' % (base_url, icon) 
            if we_are_here:
                menuclass = 'submenuin'
            else:
                menuclass = 'submenuout'

            actioninfo.append({
                'we_are_here': we_are_here,
                'title': action.get('name'),
                'url': action_url,
                'class': menuclass,
                'style': menustyle,
                'newcat': newcat,
                }
            ) 
            newcat = 0 
    firstcat = 0
return actioninfo
