from Products.CMFCore.utils import getToolByName

import zLOG

def logf(summary,message='',severity=0):
    summary = '['+ str(summary) +']'
    if message:
       message = str(message)+'\n'
    zLOG.LOG('CPSSkins: ',severity,summary, message)


def migrate(self):
    logf("START: CPSSkins Migrate")
    log = []
    prlog = log.append

    portal = self.portal_url.getPortalObject()
    skinstool = getToolByName(self, 'portal_skins')
    actionstool = getToolByName(self, 'portal_actions')
    ttool = getToolByName(self, 'portal_types')

    def pr(msg, prlog=prlog):
        prlog('%s<br>' % msg)

    def pr_nobr(msg, prlog=prlog):
        prlog('%s' % msg)

    def pr_h2(msg, prlog=prlog):
        prlog('<h2>%s</h2>' % msg)

    def pr_h3(msg, prlog=prlog):
        prlog('<h3>%s</h3>' % msg)

    def prok(prlog=prlog):
        prlog(" Already correctly installed")

    def portalhas(id, portal=portal):
        return id in portal.objectIds()

    pr_h2("Starting CPSSkins migrate")

    theme_container = getattr(portal, 'portal_themes', None)
    if theme_container is None:
        portal.manage_addProduct['CPSSkins'].manage_addTool('Portal Themes Tool', None)
    
    if theme_container.objectIds() == []:
        pr("  migrating the 'themes' folder to 'portal_themes'")

        old_theme_container = getattr(portal, 'themes', None)
        if old_theme_container is not None:
             old_themes = old_theme_container.objectIds()
             pr("    moving the themes: %s " % str(old_themes) )
             cookie = old_theme_container.manage_copyObjects(old_themes)
             theme_container.manage_pasteObjects(cookie)
    else:
        pr("  the 'portal_themes' folder is not empty.")

    pr_h3("Rebuilding themes")
    try:
        theme_container.rebuild()
    except:
        pr("  <strong>Could not rebuild existing themes!</strong>")
        pr("  Open the 'portal_themes' folder and remove all broken objects ")
        pr("  Then click on the 'Rebuild' tab to rebuild the themes")
    else:
        pr("  Themes have been rebuilt")

    pr("  Removing obsolete cache attributes: ")
    for theme in theme_container.getThemes():
        for templet in theme.getTemplets():
            for oldattr in ('cache', 'cache_last_update', \
                            'cache_count', 'cache_size'):
                if hasattr(templet, oldattr):
                    try:
                        delattr(templet, oldattr)
                    except:
                        pass
                    else:
                        pr_nobr(".")

    pr_h3("Portal types")
    pr(" Removing unused and obsolete portal types ...")
    ptypes_to_delete = [ 'FontShape', 'FontColor', 'Typefaces' ]
    for ptype in ptypes_to_delete:
        if ptype in ttool.objectIds():
            pr("  Portal type '%s' deleted" % ptype)
            ttool.manage_delObjects([ptype])


    pr_h3("Portal actions")
    portal_actions = actionstool
    pr(" Cleaning obsolete actions from earlier versions ...")
    actiondelmap = {
        'portal_actions': [ 'skinconfig', 
                            'uiconfig', 
                            'imgconfig', 
                            'templetconfig',
                            'lightskins_skinconfig', 
                            'lightskins_templetconfig', 
                            'lightskins_uiconfig',
                            'lightskins_myskinconfig', 
                            'lightskins_mytempletconfig', 
                            'lightskins_myuiconfig' 
                          ],
        }

    for tool, actionids in actiondelmap.items():
        actions_to_delete = []
        actions = list(portal[tool]._actions)
        for action in actions:
             if action.id in actionids:
                actions_to_delete.append(action) 
        for ac in actions_to_delete:
             pr(" Deleting %s : %s" %  (tool,ac.id))
             actions.remove(ac)
        portal[tool]._actions = actions


    pr_h3("Portal Skins")
    pr(" Removing obsolete skins used in earlier versions ...")
    for skindir_name in (
        'icons',
        'cpsskins_styles',
        'cpsskins_palettes' ):

        if skindir_name not in skinstool.objectIds():
            continue 
        dir = getattr(skinstool, skindir_name)
        objs = dir.objectIds() 
        if skindir_name == 'icons' and not(len(objs) == 0 or 'actionbox_templet.gif' in objs):
            continue
        skinstool.manage_delObjects([skindir_name])
        pr(" Deleting %s filesystem directory " % skindir_name)

        for skin_name, skin_path in skinstool.getSkinPaths():
            if skin_name != 'CPSSkins':
                continue
            path = [x.strip() for x in skin_path.split(',')]
            if skindir_name not in path:
                continue
            new_path = [x for x in path if x != skindir_name]
            npath = ', '.join(new_path)
            pr(" Removing '%s' from skin %s" % (skindir_name, skin_name))
            skinstool.addSkinSelection(skin_name, npath)


    pr_h3("RAM Cache")
    custom_skin = skinstool.custom
    CPSSkins_skin = skinstool.CPSSkins

    CPSSKINS_RAMCACHE_ID = 'cpsskins-templetcache'
    CPSSKINS_RENDER_METHOD_ID = 'cpsskins_render'

    if CPSSKINS_RENDER_METHOD_ID in custom_skin.objectIds():
        custom_skin._delObject(CPSSKINS_RENDER_METHOD_ID)
        pr(" Removing %s from custom" % CPSSKINS_RENDER_METHOD_ID)
    else:
        pr(" %s already removed" % CPSSKINS_RENDER_METHOD_ID)
             
    if CPSSKINS_RAMCACHE_ID in portal.objectIds():
        portal._delObject(CPSSKINS_RAMCACHE_ID)
        pr(" Removing the %s RAM cache" % CPSSKINS_RAMCACHE_ID)
    else:
        pr(" %s already removed" % CPSSKINS_RAMCACHE_ID)


    logf("END:  CPSSkins Migrate")
    return '\n'.join(log)
