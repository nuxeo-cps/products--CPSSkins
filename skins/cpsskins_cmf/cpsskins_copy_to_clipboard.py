##parameters=object_rurl=None

from types import ListType

if object_rurl is None:
    return

if isinstance(object_rurl, ListType):
    object_rurl = object_rurl[0]

tmtool = context.portal_themes
# XXX rename 'setViewMode' to something else
tmtool.setViewMode(clipboard=object_rurl, reload=1)
