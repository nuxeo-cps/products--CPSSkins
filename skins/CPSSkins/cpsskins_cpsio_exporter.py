##parameters=export_file_name=None, REQUEST=None

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
tmtool = context.portal_themes
current_theme = tmtool.getRequestedThemeName(REQUEST=REQUEST)
options.append('theme_%s' % current_theme)

try:
    exporter.setOptions(export_file_name, options=options)
    exporter.export()
    psm = 'cpsio_psm_export_successful'

except (ValueError, IOError), err:
    psm = err

if REQUEST is not None:
    return export_template(portal_status_message=psm)
