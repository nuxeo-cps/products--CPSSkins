##parameters=import_file_name=None, plugin='', REQUEST=None

import_class = 'CPSSkinsImporter'
import_template = getattr(context, 'cpsskins_theme_manage_form')

if not import_file_name and REQUEST is not None:
    return import_template(portal_status_message='cpsio_err_missing_filename')

options = [option_name for option_name, option_set in REQUEST.form.items()
           if option_set == 'on']

tmtool = context.portal_themes
psm = tmtool.manage_xmlImport(
    file=import_file_name,
    options=options,
    plugin=plugin)

if REQUEST is not None:
    return import_template(portal_status_message=psm)
