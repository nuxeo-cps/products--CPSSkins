portal_properties = getattr(context, 'portal_properties', None)

charset = 'utf-8'
if portal_properties is not None:
    site_properties = getattr(portal_properties.aq_inner.aq_explicit,
                              'site_properties', None)
    if site_properties is not None:
        site_charset = getattr(site_properties, 'default_charset', '')
        if site_charset:
            charset = site_charset
return charset
