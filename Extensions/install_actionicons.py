
from Products.CMFCore.utils import getToolByName
from Products.CPSSkins.cpsskins_utils import detectPortalType

COMMON_ACTIONS = \
( { 'category'              : 'global'
  , 'action_id'             : 'configThemes'
  , 'title'                 : 'Portal Themes'
  , 'icon_expr'             : 'cpsskins_actionicons/configthemes.png'
  }
, { 'category'              : 'global'
  , 'action_id'             : 'configPortal'
  , 'title'                 : 'Portal Configuration'
  , 'icon_expr'             : 'cpsskins_actionicons/configpanel.png'
  }
, { 'category'              : 'user'
  , 'action_id'             : 'login'
  , 'title'                 : 'Login'
  , 'icon_expr'             : 'cpsskins_actionicons/login.png'
  }
, { 'category'              : 'user'
  , 'action_id'             : 'logout'
  , 'title'                 : 'Logout'
  , 'icon_expr'             : 'cpsskins_actionicons/logout.png'
  }
, { 'category'              : 'user'
  , 'action_id'             : 'join'
  , 'title'                 : 'Join'
  , 'icon_expr'             : 'cpsskins_actionicons/join.png'
  }
)


CPS2_ACTIONS = \
( { 'category'              : 'global'
  , 'action_id'             : 'globalboxes'
  , 'title'                 : 'Global boxes'
  , 'icon_expr'             : 'cpsskins_actionicons/boxes.png'
  }
, { 'category'              : 'user'
  , 'action_id'             : 'personalboxes'
  , 'title'                 : 'My boxes'
  , 'icon_expr'             : 'cpsskins_actionicons/boxes.png'
  }
, { 'category'              : 'global'
  , 'action_id'             : 'directories'
  , 'title'                 : 'Directories'
  , 'icon_expr'             : 'cpsskins_actionicons/directories.png'
  }
)

CPS3_ACTIONS = \
( { 'category'              : 'global'
  , 'action_id'             : 'boxes'
  , 'title'                 : 'action_boxes_root'
  , 'icon_expr'             : 'cpsskins_actionicons/boxes.png'
  }
, { 'category'              : 'global'
  , 'action_id'             : 'directories'
  , 'title'                 : 'Directories'
  , 'icon_expr'             : 'cpsskins_actionicons/directories.png'
  }
)



def install(self):
    portal = self.portal_url.getPortalObject()
                                              
    log = []
    prlog = log.append

    def pr(msg, prlog=prlog):
        prlog('%s<br>' % msg)

    def pr_h2(msg, prlog=prlog):
        prlog('<h2>%s</h2>' % msg)

    def pr_h3(msg, prlog=prlog):
        prlog('<h3>%s</h3>' % msg)

    def prok(prlog=prlog):
        prlog(" Already correctly installed")

    def portalhas(id, portal=portal):
        return id in portal.objectIds()

    pr_h2("Starting CPSSkins action icons install")

    aitool = getToolByName(self, 'portal_actionicons', None)
    if aitool is None:
        try:
            cmfactionicons = portal.manage_addProduct['CMFActionIcons']
            cmfactionicons.manage_addTool('Action Icons Tool', None)
        except:
            pr('CMFActionIcons not found, skipping')
        else:
            pr('Installing CMF Action Icons Tool')
    else:
        pr('CMFActionIcons already installed')

    aitool = getToolByName(self, 'portal_actionicons', None)
    if aitool is not None:
        DEFAULT_MAPPINGS = COMMON_ACTIONS
        target = detectPortalType(self)
        pr(' Detected portal is <strong>%s</strong><br>' % target)
        if target == 'CPS2':
            DEFAULT_MAPPINGS += CPS2_ACTIONS

        if target == 'CPS3':
            DEFAULT_MAPPINGS += CPS3_ACTIONS

        pr(' Installing default action icons for %s' % target)
        for mapping in DEFAULT_MAPPINGS:
            try :
                aitool.updateActionIcon( category=mapping['category']
                                   , action_id=mapping['action_id']
                                   , icon_expr=mapping['icon_expr']
                                   , title=mapping['title']
                                   , priority=0
                                   )
            except:
                aitool.addActionIcon( category=mapping['category']
                                   , action_id=mapping['action_id']
                                   , icon_expr=mapping['icon_expr']
                                   , title=mapping['title']
                                   , priority=0
                                   )
                msg = 'new'
            else:
                msg = 'update'
            pr(' - %s/%s (%s)' % (mapping['category'], mapping['action_id'], msg)  )
             
    return '\n'.join(log)
