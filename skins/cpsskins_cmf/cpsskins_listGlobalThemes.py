tmtool = context.portal_themes

themes = tmtool.getThemes()

list = [theme.getId() for theme in themes]

return list
