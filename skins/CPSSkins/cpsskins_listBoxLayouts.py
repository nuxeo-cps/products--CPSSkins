##parameters=boxtype=None

layouts_dict = {
'PortalBox':  ['standard', 
               'plain',
               'one_frame', 
               'notitle', 
               'no_frames', 
               'notitle_noframe',
               'drawer',
               'drawer_notitle',
               'rounded_box',
               'rounded_box_notitle',
               'horizontal_menu',
              ],
'PortletBox': ['standard', 
               'plain',
               'one_frame', 
               'notitle', 
               'no_frames', 
               'notitle_noframe',
               'rounded_box',
               'rounded_box_notitle',
               'horizontal_menu',
              ]
}
return layouts_dict[boxtype]
