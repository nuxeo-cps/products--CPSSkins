##parameters=cat=None

fields = []
for propid in context.propertyIds():
    field = {}
    prop_map = context.propertyMap()
    for obj in prop_map:
        if obj['id'] == propid:
            category = obj.get('category', 'general')
            visibility = obj.get('visible', '')
            break

    if cat is None:
        cat = 'general'
    if category != cat or category == 'none':
        continue 

    field['visible'] = 1
    if visibility is not None:
        if hasattr(context, visibility):
           visible_meth = getattr(context, visibility)
           try:
              is_visible = apply(visible_meth, ())
           except:
              is_visible = 0
           field['visible'] = is_visible

    for obj in prop_map:
        if obj['id'] == propid:
            field['description'] = obj.get('label', None)
            field['palette'] = obj.get('palette', None)
            field['image'] = obj.get('image', None)
            field['style'] =  obj.get('style', None)
            field['slot'] = obj.get('slot', None)
            field['i18n'] = obj.get('i18n', None)
            field['i18n_prefix'] = obj.get('i18n_prefix', '_')
            field['i18n_suffix'] = obj.get('i18n_suffix', '_')
            field['i18n_transform'] = obj.get('i18n_transform', None)
            field['i18n_default_domain'] = obj.get('i18n_default_domain', None)
            break
                  
    if hasattr(context, propid):
        prop = getattr(context, propid)
    else:
        prop = None
           
    value = prop
    field['id'] = propid
    field['title'] = '_prop_%s_' % propid
    type = context.getPropertyType(propid)
    rows = None
    cols = None

    ftype = ''
    options = ''

    if type == 'boolean':
        ftype = 'checkbox'

    elif type == 'text':
        ftype = 'areatext'
        rows = 10 
        cols = 45 

    elif type == 'lines':
        ftype = 'lines'
        value = ''
        if prop is None:
           continue
        for i in prop:
            value = value + '\n' + i
        rows = 2 
        cols = 20

    elif type == 'string':
        ftype = 'text'

    elif type == 'int':
        ftype = 'text'

    elif type == 'multiple selection':
        ftype = 'multiple'

    elif type == 'selection':
        ftype = 'select'

    if type in ['selection', 'multiple selection']:
        for obj in prop_map:
            if obj['id'] == propid:
                select_variable = obj['select_variable']
                field['select_variable'] = select_variable
                list = []
                if hasattr(context, select_variable):
                    select_list = getattr(context, select_variable)
                    list = select_list
                    try:
                        list = apply(select_list, ())
                    except:
                        pass

                options = []
                for select in list:
                    option = {}
                    option['id'] = select
                    option['title'] = select
                    options.append(option)
                break

    if options != '' : 
        field['options'] = options

    field['type'] = ftype
    field['value'] = value

    if rows is not None:
        field['rows'] = rows

    if cols is not None:
        field['cols'] = cols

    fields.append(field)

return fields
