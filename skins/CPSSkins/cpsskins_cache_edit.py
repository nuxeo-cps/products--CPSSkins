##parameters=REQUEST=None, theme=None, **kw

from types import ListType

tmtool = context.portal_themes
mcat = tmtool.getTranslationService()

if REQUEST is not None:
    kw.update(REQUEST.form)

paths = kw.get('paths', [])
cacheable_templets = kw.get('cache', [])
cache_lifetimes = kw.get('cache_lifetimes', [])

if paths:
    idx = 0
    if not isinstance(paths, ListType):
        paths = [paths]
    for path in paths:
        templet = tmtool.restrictedTraverse(path)
        if templet.getId() in cacheable_templets:
            cacheable = 1
        else:
            cacheable = 0
        prop_dict = {'cacheable': cacheable,
                     'cache_lifetime': cache_lifetimes[idx]
                    }
        templet.manage_changeProperties(**prop_dict)
        templet.expireCache()
        idx += 1

if REQUEST is not None:
    url = REQUEST['HTTP_REFERER']
    REQUEST.RESPONSE.redirect(url)
