# Copyright (c) 2003-2005 Chalmers University of Technology
# Authors: Jean-Marc Orliaguet <mailto:jmo@ita.chalmers.se>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#

__author__ = "Jean-Marc Orliaguet <jmo@ita.chalmers.se>"

import sys

from Products.CMFCore import utils
from Products.CMFCore.CMFCorePermissions import AddPortalContent
from Products.CMFCore.DirectoryView import registerDirectory

from CPSSkinsInstaller import manage_addInstaller
from PortalThemesTool import PortalThemesTool

import AllowModules

import PortalTheme
import ThemePage
import ThemeFolder

import PageBlock
import CellBlock

import SimpleBox

# Templets
import MainContent
import SearchBox
import Breadcrumbs
import ActionBox
import TextBox
import ImageBox
import FlashBox
import PortalBox
import PortletBox
import Language
import DocumentInfo
import ThemeChooser
import PortalBoxGroup
import CollapsibleMenu
import Calendar
import PortalTab

# Cell modifiers
import CellStyler
import CellSizer
import CellHider

# Portal Styles
import AreaColor
import AreaShape
import PortalBoxColor
import PortalBoxShape
import FontColor
import FontShape
import PaletteColor
import PaletteBorder
import CollapsibleMenuStyle
import CalendarStyle
import PortalTabStyle
import FormStyle
import BoxCorners

this_module = sys.modules[__name__]

tools = (PortalThemesTool, )

portalthemeClasses = (
    PortalTheme.PortalTheme,
    ThemePage.ThemePage,
    ThemeFolder.ThemeFolder,
)

pageblockClasses = (
    PageBlock.PageBlock,
    CellBlock.CellBlock,
)

templetClasses = (
    SearchBox.SearchBox,
    MainContent.MainContent,
    ActionBox.ActionBox,
    TextBox.TextBox,
    ImageBox.ImageBox,
    FlashBox.FlashBox,
    PortalBox.PortalBox,
    PortletBox.PortletBox,
    DocumentInfo.DocumentInfo,
    ThemeChooser.ThemeChooser,
    Language.Language,
    Breadcrumbs.Breadcrumbs,
    PortalBoxGroup.PortalBoxGroup,
    CollapsibleMenu.CollapsibleMenu,
    Calendar.Calendar,
    PortalTab.PortalTab,
)

cellmodifierClasses = (
    CellStyler.CellStyler,
    CellSizer.CellSizer,
    CellHider.CellHider,
)

styleClasses = (
    AreaColor.AreaColor,
    AreaShape.AreaShape,
    PortalBoxColor.PortalBoxColor,
    PortalBoxShape.PortalBoxShape,
    FontColor.FontColor,
    FontShape.FontShape,
    CollapsibleMenuStyle.CollapsibleMenuStyle,
    CalendarStyle.CalendarStyle,
    PortalTabStyle.PortalTabStyle,
    FormStyle.FormStyle,
    BoxCorners.BoxCorners,
)

paletteClasses = (
    PaletteColor.PaletteColor,
    PaletteBorder.PaletteBorder,
)

contentConstructors = (
    PortalTheme.addPortalTheme,
    ThemePage.addThemePage,
    PageBlock.addPageBlock,
    CellBlock.addCellBlock,
    MainContent.addMainContent,
    SearchBox.addSearchBox,
    ActionBox.addActionBox,
    TextBox.addTextBox,
    ImageBox.addImageBox,
    FlashBox.addFlashBox,
    PortalBox.addPortalBox,
    PortletBox.addPortletBox,
    Language.addLanguage,
    DocumentInfo.addDocumentInfo,
    ThemeChooser.addThemeChooser,
    Breadcrumbs.addBreadcrumbs,
    PortalBoxGroup.addPortalBoxGroup,
    PortalTab.addPortalTab,
    CollapsibleMenu.addCollapsibleMenu,
    CollapsibleMenuStyle.addCollapsibleMenuStyle,
    CellStyler.addCellStyler,
    CellSizer.addCellSizer,
    CellHider.addCellHider,
    AreaColor.addAreaColor,
    AreaShape.addAreaShape,
    PortalBoxColor.addPortalBoxColor,
    PortalBoxShape.addPortalBoxShape,
    FontColor.addFontColor,
    FontShape.addFontShape,
    PaletteColor.addPaletteColor,
    PaletteBorder.addPaletteBorder,
    ThemeFolder.addThemeFolder,
    Calendar.addCalendar,
    CalendarStyle.addCalendarStyle,
    PortalTabStyle.addPortalTabStyle,
    FormStyle.addFormStyle,
    BoxCorners.addBoxCorners,
)

fti = (
    PortalTheme.factory_type_information +
    ThemePage.factory_type_information +
    PageBlock.factory_type_information +
    CellBlock.factory_type_information +
    MainContent.factory_type_information +
    SearchBox.factory_type_information +
    ActionBox.factory_type_information +
    TextBox.factory_type_information +
    ImageBox.factory_type_information +
    FlashBox.factory_type_information +
    PortalBox.factory_type_information +
    PortletBox.factory_type_information +
    DocumentInfo.factory_type_information +
    ThemeChooser.factory_type_information +
    Language.factory_type_information +
    Breadcrumbs.factory_type_information +
    PortalBoxGroup.factory_type_information +
    PortalTab.factory_type_information +
    CellStyler.factory_type_information +
    CellSizer.factory_type_information +
    CellHider.factory_type_information +
    AreaColor.factory_type_information +
    AreaShape.factory_type_information +
    PortalBoxColor.factory_type_information +
    PortalBoxShape.factory_type_information +
    FontShape.factory_type_information +
    FontColor.factory_type_information +
    PaletteColor.factory_type_information +
    PaletteBorder.factory_type_information +
    ThemeFolder.factory_type_information +
    CollapsibleMenu.factory_type_information +
    CollapsibleMenuStyle.factory_type_information +
    Calendar.factory_type_information +
    CalendarStyle.factory_type_information +
    PortalTabStyle.factory_type_information +
    FormStyle.factory_type_information +
    BoxCorners.factory_type_information +
    ())

contentClasses = portalthemeClasses + \
                 pageblockClasses + \
                 templetClasses + \
                 cellmodifierClasses + \
                 styleClasses + \
                 paletteClasses

bases = contentClasses

this_module = sys.modules[__name__]
z_bases = utils.initializeBasesPhase1(bases, this_module)
z_tool_bases = utils.initializeBasesPhase1(tools, this_module)

for path in (
    'icons',
    'skins/CPSSkins',
    'skins/cpsskins_cmf',
    'skins/cpsskins_cps2',
    'skins/cpsskins_cps3',
    'skins/cpsskins_plone',
    'skins/cpsskins_plone2') :
    registerDirectory(path, globals())

def initialize(registrar):
    registrar.registerClass(
        CPSSkinsInstaller.Installer,
        constructors=(manage_addInstaller,
                      CPSSkinsInstaller.manage_addCPSSkins,),
        )

    utils.initializeBasesPhase2(z_bases, registrar)
    utils.initializeBasesPhase2(z_tool_bases, registrar)

    utils.ToolInit(
        'Portal Themes Tool',
        tools=tools,
        product_name='CPSSkins',
        icon='draw.png',
    ).initialize(registrar)

    utils.ContentInit(
        'CPSSkins Content',
        content_types = contentClasses,
        permission = AddPortalContent,
        extra_constructors = contentConstructors,
        fti = fti,
        ).initialize(registrar)

    for classname, icon in (
        (PortalTheme.PortalTheme, 'portaltheme.png'),
        (ThemePage.ThemePage, 'themepage.png'),
        (ThemeFolder.ThemeFolder, 'themefolder.png'),
        (PageBlock.PageBlock, 'pageblock.png'),
        (CellBlock.CellBlock, 'cellblock.png'),
        (MainContent.MainContent, 'maincontent_templet.png'),
        (TextBox.TextBox, 'textbox_templet.png'),
        (ImageBox.ImageBox, 'imagebox_templet.png'),
        (FlashBox.FlashBox, 'flashbox_templet.png'),
        (Language.Language, 'language_templet.png'),
        (SearchBox.SearchBox, 'searchbox_templet.png'),
        (ActionBox.ActionBox, 'actionbox_templet.png'),
        (Breadcrumbs.Breadcrumbs, 'breadcrumbs_templet.png'),
        (DocumentInfo.DocumentInfo, 'documentinfo_templet.png'),
        (ThemeChooser.ThemeChooser, 'documentinfo_templet.png'),
        (PortalBoxGroup.PortalBoxGroup, 'portalboxgroup_templet.png'),
        (PortalBox.PortalBox, 'portalbox_templet.png'),
        (PortletBox.PortletBox, 'portletbox_templet.png'),
        (CollapsibleMenu.CollapsibleMenu, 'collapsiblemenu_templet.png'),
        (Calendar.Calendar, 'calendar_templet.png'),
        (PortalTab.PortalTab, 'portaltab_templet.png'),
        (CellStyler.CellStyler, 'cell_styler.png'),
        (CellSizer.CellSizer, 'cell_sizer.png'),
        (CellHider.CellHider, 'cell_hider.png'),
        (AreaColor.AreaColor, 'area_color.png'),
        (AreaShape.AreaShape, 'area_shape.png'),
        (PortalBoxColor.PortalBoxColor, 'box_color.png'),
        (PortalBoxShape.PortalBoxShape, 'box_shape.png'),
        (BoxCorners.BoxCorners, 'box_corners.png'),
        (FontColor.FontColor, 'fontcolor.png'),
        (FontShape.FontShape, 'fontshape.png'),
        (CollapsibleMenuStyle.CollapsibleMenuStyle, 'collapsiblemenu_style.png'),
        (CalendarStyle.CalendarStyle, 'calendar_style.png'),
        (PortalTabStyle.PortalTabStyle, 'portaltab_style.png'),
        (FormStyle.FormStyle, 'form_style.png'),
        (PaletteColor.PaletteColor, 'palette_color.png'),
        (PaletteBorder.PaletteBorder, 'palette_border.png'),
    ):
        utils.registerIcon(classname, 'icons/%s' % icon, globals())

