##parameters=import_file_name=None, REQUEST=None

import_class = 'CPSSkinsImporter'
import_template = getattr(context, 'cpsskins_theme_manage_form')

if not import_file_name and REQUEST is not None:
    return import_template(portal_status_message='cpsio_err_missing_filename')

io_tool = context.portal_io
importer = io_tool.getImportPlugin(
    import_class,
    context.portal_url.getPortalObject())

options = [option_name for option_name, option_set in REQUEST.form.items()
           if option_set == 'on']

try:
    importer.setOptions(import_file_name, options=options)
    importer.importFile()
    importer.finalize()
    psm = 'cpsio_psm_import_successful'
except (ValueError, IOError), err:
    psm = err

if REQUEST is not None:
    return import_template(portal_status_message=psm)
