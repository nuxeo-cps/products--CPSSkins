##parameters=object_rurl=None

if object_rurl is None:
    return

tmtool = context.portal_themes

# XXX rename 'setViewMode' to something else
tmtool.setViewMode(clipboard=object_rurl)
