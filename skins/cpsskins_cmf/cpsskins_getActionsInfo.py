##parameters=obj=None, context_obj=None

if obj is None:
    return

REQUEST = context.REQUEST
tmtool = context.portal_themes
current_url = REQUEST.get('cpsskins_url', None)
base_url = REQUEST.get('cpsskins_base_url', '')

action_categories = obj.action_categories
custom_action_categories = obj.custom_action_categories
invisible_actions = obj.invisible_actions

categories = action_categories[:]
if custom_action_categories:
    if custom_action_categories[0] != '':
        categories += custom_action_categories

actions = REQUEST.get('cpsskins_cmfactions', None)
if actions is None:
    if context_obj is None:
        context_obj = context
    actions = context.portal_actions.listFilteredActionsFor(context_obj)

actioninfo = []

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

            if we_are_here:
                menuclass = 'selected'
            else:
                menuclass = None

            actioninfo.append({
                'we_are_here': we_are_here,
                'title': action.get('name'),
                'url': action_url,
                'class': menuclass,
                'newcat': newcat,
                }
            )
            newcat = 0
    firstcat = 0
return actioninfo
