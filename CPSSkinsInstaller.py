# Copyright (c) 2003-2004 Chalmers University of Technology
# Authors : Jean-Marc Orliaguet <jmo@ita.chalmers.se>
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

"""
  CPSSkins Installer
"""

import Globals

from Globals import DTMLFile
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from OFS.SimpleItem import SimpleItem

manage_addInstaller = DTMLFile('zmi/addInstallerForm', globals())

class Installer(SimpleItem):
    meta_type = 'CPSSkins Installer'

Globals.InitializeClass(Installer)

def manage_addCPSSkins(dispatcher, id,
                       SourceSkin=None,
                       Target=None,
                       ReinstallDefaultThemes=None,
                       REQUEST=None):
    """CPSSkins Installer"""

    log = []
    pr = log.append
    portal = getattr(dispatcher.Destination(), id)

    # CPSSkins installer
    method = 'cpsskinsinstall'
    if method in portal.objectIds():
        portal._delObject(method)

    pr('Creating cpsskinsinstall External Method')
    cpsskinsinstall = ExternalMethod(
        method,
       'CPSSkins Installer',
       'CPSSkins.Install',
       'install'
    )
    portal._setObject(method, cpsskinsinstall)

    # Creating redirection
    site_url = dispatcher.DestinationURL()
    redirect_url = site_url + '/cpsskins_themes_reconfig_form?no_referer=1'
    pr('<blockquote style="border: 1px solid Gray; background-color: #f0f0f0;"><ul>')
    pr('<li><a href="%s" target="_new">Go to the portal</a></li>' % site_url)
    pr('<li><a href="%s" target="_new">Go to the theme configuration page</a></li>' \
                            % redirect_url)
    pr('</ul></blockquote>')

    pr(portal.cpsskinsinstall(
        SourceSkin=SourceSkin,
        Target=Target,
        ReinstallDefaultThemes=ReinstallDefaultThemes)
    )
    if 'cpsskinsinstall' in portal.objectIds():
        pr("Removing cpsskinsinstall")
        portal._delObject('cpsskinsinstall')

    pr('Done')
    if REQUEST is not None:
        REQUEST.RESPONSE.setHeader('Content-Type', 'text/html')
    return '<br>'.join(log)
