import os
import sys
from re import match
from App.Extensions import getPath

from Products.CMFCore.utils import getToolByName
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.CMFCore.CMFCorePermissions import View, AccessContentsInformation
from Products.CMFCore.DirectoryView import createDirectoryView

from Products.CPSSkins.cpsskins_utils import detectPortalType

import zLOG

def package_home(name):
    """Returns path to Products.name"""
    m = sys.modules['Products.%s' % name]
    return (m.__path__[0])

cpsskins_home = package_home('CPSSkins')
zexpdir = os.path.join(cpsskins_home, 'Install')
                                           
def logf(summary,message='',severity=0):
    summary = '['+ str(summary) +']'
    if message:
        message = str(message)+'\n'
    zLOG.LOG('CPSSkins: ',severity,summary, message)

def setperms(object, perms, pr=None):
    """ """
    for perm, roles in perms.items():
        acquire = type(roles) == type([])
        object.manage_permission(perm, roles, acquire)
        pr("  Permission %s" % perm)

def checktool(self, name):
    """ """
    try:
        getToolByName(self, name)
    except AttributeError:
        pass
    else:
        return 1
             
def install(self, SourceSkin=None, Target=None, ReinstallDefaultThemes=None):
    """ """
    logf("START: CPSSkins Install")
    log = []
    prlog = log.append

    portal = self.portal_url.getPortalObject()
    skinstool = getToolByName(self, 'portal_skins')
    actionstool = getToolByName(self, 'portal_actions')

    def pr(msg, prlog=prlog):
        prlog('%s<br>' % msg)

    def pr_h2(msg, prlog=prlog):
        prlog('<h2>%s</h2>' % msg)

    def pr_h3(msg, prlog=prlog):
        prlog('<h3>%s</h3>' % msg)

    def prok(prlog=prlog):
        prlog(" Already correctly installed")

    def portalhas(id, portal=portal):
        """ """
        return id in portal.objectIds()

    pr_h2("Starting CPSSkins install")

    if Target is None:
        Target = detectPortalType(self)
        pr('Detected portal type is <strong>%s</strong>' % Target) 
    else:
        pr('Portal type is <strong>%s</strong>' % Target) 
    if SourceSkin is None:
        for skin in self.portal_skins.getSkinSelections():
            if skin != 'CPSSkins':
                SourceSkin = skin 
                break

    pr('Default skin is <strong>%s</strong>' % SourceSkin) 

    pr_h3("Dependencies")
    try:
        import Products.TranslationService
        translationservice_is_present = 1
        pr("TranslationService is installed")
    except ImportError:
        translationservice_is_present = 0
        pr("TranslationService is not installed")

    try:
        import Products.Localizer
        localizer_is_present = 1
        pr("Localizer is installed")
    except ImportError:
        localizer_is_present = 0
        pr("Localizer is not installed")

    pr_h3("External methods")
    ext_methods = ( { 'id': 'cpsskinsmigrate',
                      'title': 'CPSSkins (migrate from an earlier version)',
                      'script': 'CPSSkins.migrate',
                      'method': 'migrate', 
                      'protected': 1,
                    }, 
                    { 'id': 'cpsskinsupdate',
                      'title': 'CPSSkins Updater',
                      'script': 'CPSSkins.Install',
                      'method': 'update', 
                      'protected': 1,
                    },
                    { 'id': 'cpsskins_benchmarktimer', 
                      'title': 'Benchmark timer',
                      'script': 'CPSSkins.benchmarktimer',
                      'method': 'BenchmarkTimerInstance',
                      'protected': 0,
                    },
                    { 'id': 'install_actionicons',
                      'title': 'Install CPSSkins action icons',
                      'script': 'CPSSkins.install_actionicons',
                      'method': 'install',
                      'protected': 1,
                    },
                  ) 
    portal_objectIds = portal.objectIds()
    for meth in ext_methods:
        method = meth['id']
        if method in portal_objectIds:
            portal._delObject(method)
        pr('Creating %s External Method' % method)
        ext_method = ExternalMethod(method, 
                                    meth['title'], 
                                    meth['script'], 
                                    meth['method']) 
        portal._setObject(method, ext_method)
        if method in portal_objectIds:
            manage_perms = portal[method].manage_permission
            if meth['protected']:
                pr("Protecting %s" % method)
                manage_perms(View, roles=['Manager'], acquire=0) 
                manage_perms(AccessContentsInformation, roles=['Manager'], acquire=0)
            else:
                manage_perms(View, roles=['Manager'], acquire=1)


    pr_h3("i18n")
    mcat = None
    if Target == 'CPS2':
        if portalhas('Localizer'):
            portal.manage_delObjects(['Localizer'])
    if Target in ['CMF', 'CPS3', 'Plone', 'Plone2' ]:
        # Localizer
        if localizer_is_present:
            if not portalhas('Localizer'):
                pr("  Adding Localizer")
                languages = ('en',)
                localizer = portal.manage_addProduct['Localizer'] 
                localizer.manage_addLocalizer(title='', languages=languages,)
                Localizer = portal['Localizer']
            else:
                pr("Localizer already here")
                Localizer = portal['Localizer']
                languages = Localizer.get_supported_languages()

        # translation_service                       
        if translationservice_is_present:
            if not portalhas('translation_service'):
                pr("  translation_service not found")
                try:
                    pts = portal.manage_addProduct['TranslationService']
                    pts.addPlacefulTranslationService(id='translation_service')
                except:                                        
                    pass                 
            else:                  
                pr("  translation_service tool added")                  
                translation_service = portal.translation_service  

    # create portal_themes tool
    pr_h3("portal_themes tool")
    if portalhas('portal_themes') and ReinstallDefaultThemes:
        portal.manage_delObjects(['portal_themes'])
    if not portalhas('portal_themes') or ReinstallDefaultThemes:
        portal.manage_addProduct['CPSSkins'].manage_addTool('Portal Themes Tool', None)
    # adding portal_themes to the list of action providers
    pr("  Adding portal_themes to the list of action providers")
    if 'portal_themes' in actionstool.listActionProviders():
        pr("    Already there")
    else:    
        try: 
            actionstool.addActionProvider('portal_themes')
            pr("   Done")
        except:
            pr("   Failed")

    # Importing portal themes 
    theme_container = getattr(portal, 'portal_themes')
    pr_h3("Portal themes")
    if ReinstallDefaultThemes or (theme_container.objectIds() == [] and not portalhas('themes')):
        themes_list = { 'CMF':     ( 'CMF-Plone', 
                                     'CMF-Printable', 
                                   ),
                        'CPS2':    ( 'CPS2-LightSkins', 
                                     'CPS2-Plone', 
                                     'CMF-Printable', 
                                   ),
                        'CPS3':    ( 'CPS3-LightSkins', 
                                     'CPS3-Autumn', 
                                     'CPS3-Default', 
                                     'CMF-Printable', 
                                     'CPS3-Plone', 
                                   ),
                        'Plone':   ( 'Plone-Plone', 
                                     'CMF-Printable',  
                                   ),
                        'Plone2':  ( 'Plone2-Plone', 
                                     'Plone2-Autumn', 
                                     'CMF-Printable', 
                                   ), 
                      }
        if Target in ['CMF', 'CPS2', 'CPS3', 'Plone', 'Plone2' ]:
            theme_ids = theme_container.objectIds()
            theme_container.manage_delObjects(theme_ids)
            for theme_name in themes_list[Target]:
                pr(" Importing %s theme" % theme_name)
                zexppath = os.path.join(zexpdir, '%s.%s' % (theme_name, 'zexp'))
                try:
                    theme_container._importObjectFromFile(zexppath)
                except:
                    pr("    Could not import theme  %s" % theme_name)

    pr(portal.cpsskinsupdate())
    pr(portal.cpsskinsmigrate())
    pr(portal.install_actionicons())
    return '\n'.join(log)


def update(self):
    """ Update """
    logf("START: CPSSkins Update")
    log = []
    prlog = log.append

    portal = self.portal_url.getPortalObject()
    skinstool = getToolByName(self, 'portal_skins')
    ttool = getToolByName(self, 'portal_types')
    tmtool = getToolByName(self, 'portal_themes')
    actionstool = getToolByName(self, 'portal_actions')

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

    pr_h2("Starting CPSSkins update")

    # setting roles
    pr_h3("Setting roles")
    already = portal.valid_roles()
    for role in ('ThemeManager', ):
        if role not in already:
            portal._addRole(role)
            pr(" Add role %s" % role)
        else:
            pr(" Role %s already there" % role)

    # portal_themes
    tool_id = 'portal_themes'
    perms = ('Manage Themes', 
             'Copy or Move',
             'Change permissions',
             'Delete objects',
             'Add portal content', 
             'Manage properties',
             'Change Images and Files', 
    ) 
    pr(" Verifying permissions on the '%s' tool" % tool_id)
    tool = getattr(portal, tool_id)
    for perm in perms:
        setperms(tool, {perm: ('Manager', 'Owner', 'ThemeManager')}, pr=pr)
    tool.reindexObjectSecurity()

    # portal_cpsportlets (CPSPortlets)
    tool_id = 'portal_cpsportlets'
    if checktool(self, tool_id):
        tool = getattr(portal, tool_id)
        perms = ('Manage Portlets', ) 
        pr(" Verifying permissions on the '%s' tool" % tool_id)
        for perm in perms:
            setperms(tool, {perm: ('Manager', 'Owner', 'ThemeManager')}, pr=pr) 
        tool.reindexObjectSecurity()

    # portal types
    pr_h3("Portal types")
    types_in_portalthemes = (
        'Theme Page',
        'Theme Folder',
    )

    types_in_themepages = (
        'Page Block',
    )

    types_templets = (
        'Search Box Templet',
        'Action Box Templet',
        'Text Box Templet',
        'Image Box Templet',
        'Flash Box Templet',
        'Portal Box Templet',
        'Document Info Templet',
        'Theme Chooser Templet',
        'Language Templet',
        'Breadcrumbs Templet',
        'Portal Box Group Templet',
        'Main Content Templet',
        'Collapsible Menu Templet',
        'Portal Tab Templet',
        )

    types_in_pageblocks = types_templets + (
        'Cell Sizer',
        'Cell Styler',
        'Cell Hider',
        'Cell Block',
        )

    types_in_cellblocks = types_templets + (
        'Cell Sizer',
        )

    types_in_stylefolders = (
        'Area Shape',
        'Area Color',
        'Portal Box Shape',
        'Portal Box Color',
        'Font Color',
        'Font Shape',
        'Collapsible Menu Style',
        'Portal Tab Style',
        'Form Style',
        'Box Corners',
        )

    types_in_palettefolders = (
        'Palette Color',
        'Palette Border',
        ) 

    ptypes_to_delete = ()

    # CMFCalendar
    if checktool(self, 'portal_calendar'):
        types_in_stylefolders += ('Calendar Style',)
        types_in_pageblocks += ('Calendar Templet',)
        types_in_cellblocks += ('Calendar Templet',)
    else:
        ptypes_to_delete += ('Calendar Templet', 'Calendar Style')

    # CPSPortlets
    if checktool(self, 'portal_cpsportlets'):
        types_in_pageblocks += ('Portlet Box Templet',)
        types_in_cellblocks += ('Portlet Box Templet',)
    else:
        ptypes_to_delete += ('Portlet Box Templet',)

    types_in_themefolders = types_in_stylefolders + \
                            types_in_palettefolders + \
                            types_in_themepages + \
                            types_in_pageblocks

    ptypes = {
    'CPSSkins' : ('Portal Theme', ) +
                 types_in_portalthemes +
                 types_in_themepages +
                 types_in_pageblocks + 
                 types_in_stylefolders + 
                 types_in_palettefolders
               }

    # deleting portal types
    pr("  Deleting portal types")
    for ptype in ptypes_to_delete:             
        if ptype in ttool.objectIds():
            pr("  Portal type '%s' deleted" % ptype)
            ttool.manage_delObjects([ptype])

    # reinstalling portal types
    pr("  Resinstalling portal types")
    ptypes_installed = ttool.objectIds()
    for prod in ptypes.keys():
        for ptype in ptypes[prod]:
            pr("  Type '%s'" % ptype)
            if ptype in ptypes_installed:
                ttool.manage_delObjects([ptype])
                pr("   Deleted")
            ttool.manage_addTypeInformation(
                id=ptype,   
                add_meta_type='Factory-based Type Information',
                typeinfo_name=prod+': '+ptype,
                )           
            pr("   Installation")
    
    pr("  Installing allowed content types")
    allowed_content_type = {
        'Theme Page' : types_in_themepages,
        'Page Block' : types_in_pageblocks,
        'Cell Block' : types_in_cellblocks,
        'Portal Theme' : types_in_portalthemes,
        'Theme Folder' : types_in_themefolders + (
            'Portal Theme', 'Theme Page', 'Theme Folder'),
       }

    for ptype in allowed_content_type.keys():
        allowed_types = allowed_content_type[ptype]
        ttool[ptype].allowed_content_types = allowed_types

    # Localizer
    pr_h3('i18n')
    mcat=None
    defaultmcat=None
    try:
        mcat = defaultmcat = getToolByName(self, 'portal_messages')
    except:
        pass

    if portalhas('Localizer'):
        pr("Localizer already here")
        Localizer = portal['Localizer']
        languages = Localizer.get_supported_languages()
        # Default MessageCatalog
        default_catalog_id = 'default'
        cpsskins_catalog_id = 'cpsskins'
        localizer = Localizer.manage_addProduct['Localizer']
        if 'default' not in Localizer.objectIds():
            localizer.manage_addMessageCatalog(
                id='default',
                title='Default messages',
                languages=languages,
            )
            pr("  default MessageCatalogCreated")

        # CPSSkins Message Catalog
        if cpsskins_catalog_id in Localizer.objectIds():
            Localizer.manage_delObjects([cpsskins_catalog_id])
            pr(" Previous default MessageCatalog deleted for CPSSkins")
         
        # Adding the new message Catalog
        localizer.manage_addMessageCatalog(
           id=cpsskins_catalog_id,
           title='CPSSkins messages',
           languages=languages,
        )
         
        pr("  CPSSkins MessageCatalogCreated")
        if portalhas('Localizer'):
            mcat = portal['Localizer'][cpsskins_catalog_id]
            defaultmcat = portal['Localizer']['default']

    # portal messages
    skin = 'CPSSkins'
    if mcat is not None:
        # importing CPSSkins .po files
        pr(" Checking available languages for skin %s" % skin)
        podir = os.path.join('Products', 'CPSSkins' )
        popath = getPath(podir, 'i18n')
        if popath is None:      
            pr(" !!! Unable to find .po dir")
        else:                   
            pr("  Checking installable languages")
            langs = []          
            avail_langs = mcat.get_languages()
            pr("    Available languages: %s" % str(avail_langs))
            for file in os.listdir(popath):
                if file.endswith('.po'):
                    m = match('^.*([a-z][a-z]|[a-z][a-z]_[A-Z][A-Z])\.po$', file)
                    if m is None:
                        pr( '    Skipping bad file %s' % file)
                        continue
                    lang = m.group(1)
                    if lang in avail_langs:
                        lang_po_path = os.path.join(popath, file)
                        lang_file = open(lang_po_path)
                        pr("    Importing %s into '%s' locale" % (file, lang))
                        # Localizer < 1.1
                        try:
                            mcat.manage_import(lang, lang_file)
                        except:
                            pass
                        # Localizer 1.1
                        try:
                            mcat.po_import(lang, lang_file.read())
                        except:
                            pass
                    else:       
                        pr( '    Skipping not installed locale for file %s' % file)

    if defaultmcat is not None:
        # importing default .po files
        podir = os.path.join('Products', 'CPSSkins' )
        popath = getPath(podir, 'i18n')
        if popath is not None:      
            langs = []          
            avail_langs = defaultmcat.get_languages()
            for file in os.listdir(popath):
                if file.endswith('.po'):
                    m = match('^.*([a-z][a-z]|[a-z][a-z]_[A-Z][A-Z])\.po$', file)
                    if m is None:
                        pr( '    Skipping bad file %s' % file)
                        continue
                    lang = m.group(1)
                    if lang in avail_langs:
                        lang_po_path = os.path.join(popath, file)
                        lang_file = open(lang_po_path)
                        pr("    Importing %s into default '%s' locale" % (file, lang))
                        # Localizer < 1.1
                        try:
                            defaultmcat.manage_import(lang, lang_file)
                        except:
                            pass
                        # Localizer 1.1
                        try:
                            defaultmcat.po_import(lang, lang_file.read())
                        except:
                            pass
                    else:       
                        pr( '    Skipping not installed locale for file %s' % file)

        # 'cpsskins' domain for translation service
        if portalhas('translation_service'):
            translation_service = portal.translation_service
            pr (" Translation Service Tool found ")
            for cat_id in [cpsskins_catalog_id, default_catalog_id]:
                try:
                    translation_service.manage_addDomainInfo(
                        cat_id,
                       'Localizer/'+cat_id
                    )
                    pr(" %s domain set to Localizer/%s" % (cat_id, cat_id))
                except:
                    pass

    # portal skins
    Target = detectPortalType(self)
    pr_h3("Portal detection")
    pr('Detected portal type is <strong>%s</strong>' % Target)
    SourceSkin = ''
    for skin in self.portal_skins.getSkinSelections():
        if skin != 'CPSSkins':
            SourceSkin = skin 
            break

    skins = ('CPSSkins', 'cpsskins_icons' )
    if Target == 'CPS2':
        skins = skins + ('cpsskins_cps2', )
    if Target == 'CPS3':
        skins = skins + ('cpsskins_cps3', )
    if Target == 'Plone':
        skins = skins + ('cpsskins_plone', )
    if Target == 'Plone2':
        skins = skins + ('cpsskins_plone2', )
    if Target in ['CMF', 'CPS2', 'CPS3', 'Plone', 'Plone2' ]:
        skins = skins + ('cpsskins_cmf', )

    paths = {
        'CPSSkins': 'skins/CPSSkins',
        'cpsskins_cmf': 'skins/cpsskins_cmf',
        'cpsskins_cps2': 'skins/cpsskins_cps2',
        'cpsskins_cps3': 'skins/cpsskins_cps3',
        'cpsskins_plone': 'skins/cpsskins_plone',
        'cpsskins_plone2': 'skins/cpsskins_plone2',
        'cpsskins_icons': 'icons',
    }

    pr_h3("Portal skins")
    for skin in skins:
        rel_path = paths[skin]
        rel_path = rel_path.replace('/', os.sep)
        path = os.path.join('CPSSkins', rel_path)
        pr(" FS Directory View '%s'" % skin)
        if skin in skinstool.objectIds():
            skinstool.manage_delObjects([skin])
        pr("  Reinstalling skin")
        try:
            createDirectoryView(skinstool, path, skin)
        except:
            path = os.path.join('Products', path)
            createDirectoryView(skinstool, path, skin)

    allskins = skinstool.getSkinPaths()
    pr('Using %s as source skin' % SourceSkin)
    for skin_name, skin_path in allskins:
        if skin_name != SourceSkin:
            continue
        path = [x.strip() for x in skin_path.split(',')]
        path = [x for x in path if x not in skins] # strip all
        if path and path[0] == 'custom':
            path = path[:1] + list(skins) + path[1:]
        else:
            path = list(skins) + path
        npath = ', '.join(path)
        skinstool.addSkinSelection('CPSSkins', npath)
    skinstool.default_skin = 'CPSSkins'
    pr(" Setting 'CPSSkins' as default skin")

                                                        
    pr_h3("Purging the RAM cache")                      
    tmtool.manage_clearCaches()
    pr("  Cache purged")

    logf("END:  CPSSkins Update")
    return '\n'.join(log)

def uninstall(self):
    """ uninstall method for CMFQuickInstaller"""
    log = []
    prlog = log.append

    portal = self.portal_url.getPortalObject()
    skinstool = getToolByName(self, 'portal_skins')
    actionstool = getToolByName(self, 'portal_actions')

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

    pr_h2("Starting CPSSkins uninstall")
    # removing portal_themes from the list of action providers
    pr("  Removing portal_themes from the list of action providers")

    actionstool = getToolByName(self, 'portal_actions')
    if 'portal_themes' in actionstool.listActionProviders():
        try: 
            actionstool.deleteActionProvider('portal_themes')
            pr("   Done")
        except:
            pr("   Failed")

    return '\n'.join(log)
