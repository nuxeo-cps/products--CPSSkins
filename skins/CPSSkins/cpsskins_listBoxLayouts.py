##parameters=boxtype=None

layouts_dict = {
'PortalBox':  ['standard', 
               'one_frame', 
               'notitle', 
               'no_frames', 
               'notitle_noframe',
               'drawer',
               'drawer_notitle'
              ],
'PortletBox': ['standard', 
               'one_frame', 
               'notitle', 
               'no_frames', 
               'notitle_noframe'
              ]
}
return layouts_dict[boxtype]
