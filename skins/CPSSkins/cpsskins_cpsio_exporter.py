##parameters=export_file_name=None, theme=None, REQUEST=None

export_class = 'CPSSkinsExporter'
export_template = getattr(context, 'cpsskins_theme_manage_form')

if not export_file_name and REQUEST is not None:
    return export_template(portal_status_message='cpsio_err_missing_filename')

io_tool = context.portal_io
exporter = io_tool.getExportPlugin(
    export_class,
    context.portal_url.getPortalObject())

options = [o['id'] for o in io_tool.getExportOptionsTable(export_class)]

# append the current theme name to the list of options as 'theme_...'
options.append('theme_%s' % theme)

tmtool = context.portal_themes
theme_container = tmtool.getThemeContainer(theme)
if theme_container is not None:
    theme_container.rebuild()

try:
    exporter.setOptions(export_file_name, options=options)
    exporter.export()
    psm = 'cpsio_psm_export_successful'

except (ValueError, IOError), err:
    psm = err

if REQUEST is not None:
    return export_template(portal_status_message=psm)
